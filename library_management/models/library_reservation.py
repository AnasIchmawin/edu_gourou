# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta


class LibraryReservation(models.Model):
    _name = 'library.reservation'
    _description = 'Réservation de livre'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority, create_date'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True,
                       default='Nouveau')
    book_id = fields.Many2one('library.book', string='Livre', required=True,
                               tracking=True, ondelete='cascade')
    member_id = fields.Many2one('library.member', string='Adhérent', required=True,
                                 tracking=True, ondelete='cascade')
    
    # Informations du livre (pour faciliter l'accès)
    book_title = fields.Char(related='book_id.name', string='Titre du livre', store=True)
    book_author = fields.Char(related='book_id.author_id.name', string='Auteur', store=True)
    book_cover = fields.Binary(related='book_id.cover_image', string='Couverture')
    
    # Informations de l'adhérent
    member_name = fields.Char(related='member_id.name', string='Nom adhérent', store=True)
    member_email = fields.Char(related='member_id.email', string='Email adhérent', store=True)
    member_state = fields.Selection(related='member_id.state', string='État adhérent')
    
    # Dates
    reservation_date = fields.Datetime(string='Date de réservation', default=fields.Datetime.now,
                                        required=True, tracking=True)
    expiry_date = fields.Date(string='Date d\'expiration', compute='_compute_expiry_date',
                               store=True, tracking=True,
                               help='Date limite pour récupérer le livre (3 jours après disponibilité)')
    notified_date = fields.Datetime(string='Date de notification',
                                      help='Date à laquelle l\'adhérent a été notifié')
    pickup_date = fields.Datetime(string='Date de récupération', tracking=True)
    cancelled_date = fields.Datetime(string='Date d\'annulation')
    
    # Gestion de la file d'attente
    priority = fields.Integer(string='Position dans la file', default=0,
                               help='Plus petit = prioritaire')
    
    state = fields.Selection([
        ('pending', 'En attente'),
        ('available', 'Disponible'),
        ('picked_up', 'Récupéré'),
        ('expired', 'Expiré'),
        ('cancelled', 'Annulé'),
    ], string='État', default='pending', required=True, tracking=True)
    
    # Notes
    notes = fields.Text(string='Notes')
    cancellation_reason = fields.Text(string='Raison d\'annulation')
    
    active = fields.Boolean(string='Actif', default=True)
    
    _sql_constraints = [
        ('unique_pending_reservation',
         'unique(book_id, member_id, state)',
         'Vous avez déjà une réservation en attente pour ce livre !')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.reservation') or 'Nouveau'
        
        # Vérifier que l'adhérent est actif
        if vals.get('member_id'):
            member = self.env['library.member'].browse(vals['member_id'])
            if member.state != 'active':
                raise exceptions.UserError(
                    'Impossible de créer une réservation pour un adhérent non actif !'
                )
        
        # Vérifier le nombre maximum de réservations par adhérent
        if vals.get('member_id'):
            existing_reservations = self.search_count([
                ('member_id', '=', vals['member_id']),
                ('state', 'in', ['pending', 'available'])
            ])
            if existing_reservations >= 3:
                raise exceptions.UserError(
                    'Vous avez atteint le nombre maximum de réservations (3) !'
                )
        
        reservation = super(LibraryReservation, self).create(vals)
        
        # Calculer la priorité (position dans la file)
        reservation._compute_priority()
        
        # Envoyer notification de confirmation
        reservation._send_reservation_confirmation()
        
        return reservation

    @api.depends('notified_date')
    def _compute_expiry_date(self):
        for reservation in self:
            if reservation.notified_date:
                expiry_datetime = reservation.notified_date + timedelta(days=3)
                reservation.expiry_date = expiry_datetime.date()
            else:
                reservation.expiry_date = False

    def _compute_priority(self):
        """Calculer la position dans la file d'attente"""
        for reservation in self:
            if reservation.state == 'pending':
                # Compter les réservations en attente pour ce livre, créées avant
                earlier_reservations = self.search_count([
                    ('book_id', '=', reservation.book_id.id),
                    ('state', '=', 'pending'),
                    ('create_date', '<', reservation.create_date)
                ])
                reservation.priority = earlier_reservations + 1
            else:
                reservation.priority = 0

    def _send_reservation_confirmation(self):
        """Envoyer email de confirmation de réservation"""
        self.ensure_one()
        if not self.member_id.email:
            return False
        
        try:
            template = self.env.ref('library_management.email_template_reservation_confirmed')
            template.send_mail(self.id, force_send=True)
            self.message_post(
                subject='Réservation confirmée',
                body=f'Email de confirmation envoyé à {self.member_email}'
            )
            return True
        except Exception as e:
            self.message_post(
                subject='Erreur notification',
                body=f'Impossible d\'envoyer l\'email: {str(e)}'
            )
            return False

    def action_notify_available(self):
        """Notifier l'adhérent que le livre est disponible"""
        self.ensure_one()
        
        if self.state != 'pending':
            raise exceptions.UserError('Cette réservation n\'est plus en attente !')
        
        self.write({
            'state': 'available',
            'notified_date': fields.Datetime.now(),
        })
        
        # Envoyer notification
        if self.member_id.email:
            try:
                template = self.env.ref('library_management.email_template_reservation_available')
                template.send_mail(self.id, force_send=True)
                self.message_post(
                    subject='Livre disponible',
                    body=f'Notification envoyée à {self.member_email}. Délai de récupération: 3 jours.'
                )
            except Exception as e:
                self.message_post(
                    subject='Erreur notification',
                    body=f'Impossible d\'envoyer l\'email: {str(e)}'
                )
        
        # Log dans les notifications
        self.env['library.notification.log'].create({
            'notification_type': 'book_available',
            'recipient_id': self.member_id.id,
            'recipient_email': self.member_email,
            'book_id': self.book_id.id,
            'method': 'email',
            'status': 'sent',
        })

    def action_mark_picked_up(self):
        """Marquer comme récupéré (créer l'emprunt)"""
        self.ensure_one()
        
        if self.state != 'available':
            raise exceptions.UserError('Le livre n\'est pas encore disponible pour récupération !')
        
        # Vérifier que le livre est bien disponible
        if self.book_id.state != 'available':
            raise exceptions.UserError('Le livre n\'est plus disponible !')
        
        # Créer l'emprunt
        borrowing = self.env['library.borrowing'].create({
            'book_id': self.book_id.id,
            'member_id': self.member_id.id,
            'borrower_name': self.member_name,
            'borrower_email': self.member_email,
            'borrower_phone': self.member_id.phone,
        })
        
        # Confirmer l'emprunt
        borrowing.action_confirm()
        
        # Marquer la réservation comme récupérée
        self.write({
            'state': 'picked_up',
            'pickup_date': fields.Datetime.now(),
        })
        
        self.message_post(
            subject='Livre récupéré',
            body=f'Emprunt créé: {borrowing.name}'
        )
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Emprunt créé',
            'res_model': 'library.borrowing',
            'res_id': borrowing.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_cancel(self):
        """Annuler la réservation"""
        for reservation in self:
            reservation.write({
                'state': 'cancelled',
                'cancelled_date': fields.Datetime.now(),
            })
            
            # Si c'était en attente, mettre à jour les priorités suivantes
            if reservation.state == 'pending':
                reservation._update_queue_after_cancellation()

    def _update_queue_after_cancellation(self):
        """Mettre à jour la file d'attente après annulation"""
        self.ensure_one()
        # Recalculer les priorités pour ce livre
        pending_reservations = self.search([
            ('book_id', '=', self.book_id.id),
            ('state', '=', 'pending')
        ], order='create_date')
        
        for index, reservation in enumerate(pending_reservations):
            reservation.priority = index + 1

    @api.model
    def _cron_check_expired_reservations(self):
        """Cron job: Vérifier les réservations expirées"""
        today = fields.Date.today()
        
        expired_reservations = self.search([
            ('state', '=', 'available'),
            ('expiry_date', '<', today)
        ])
        
        for reservation in expired_reservations:
            reservation.write({
                'state': 'expired',
                'cancellation_reason': 'Délai de récupération dépassé (3 jours)',
            })
            
            reservation.message_post(
                subject='Réservation expirée',
                body='Le livre n\'a pas été récupéré dans les 3 jours.'
            )
            
            # Notifier le prochain dans la file
            reservation.book_id._check_and_notify_next_reservation()

    @api.model
    def _cron_process_queue_when_book_returned(self):
        """Cron job: Traiter la file d'attente pour les livres retournés"""
        # Trouver les livres disponibles avec des réservations en attente
        books_with_reservations = self.search([
            ('state', '=', 'pending')
        ]).mapped('book_id')
        
        available_books = books_with_reservations.filtered(lambda b: b.state == 'available')
        
        for book in available_books:
            book._check_and_notify_next_reservation()


class LibraryBook(models.Model):
    _inherit = 'library.book'

    reservation_ids = fields.One2many('library.reservation', 'book_id', string='Réservations')
    reservation_count = fields.Integer(string='Nombre de réservations',
                                        compute='_compute_reservation_count', store=True)
    has_pending_reservations = fields.Boolean(string='A des réservations en attente',
                                               compute='_compute_reservation_count', store=True)

    @api.depends('reservation_ids', 'reservation_ids.state')
    def _compute_reservation_count(self):
        for book in self:
            pending = book.reservation_ids.filtered(lambda r: r.state == 'pending')
            book.reservation_count = len(pending)
            book.has_pending_reservations = len(pending) > 0

    def action_view_reservations(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Réservations - {self.name}',
            'res_model': 'library.reservation',
            'view_mode': 'tree,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'default_book_id': self.id},
        }

    def _check_and_notify_next_reservation(self):
        """Vérifier et notifier la prochaine réservation en attente"""
        self.ensure_one()
        
        if self.state != 'available':
            return False
        
        # Trouver la prochaine réservation en attente (priorité la plus basse)
        next_reservation = self.env['library.reservation'].search([
            ('book_id', '=', self.id),
            ('state', '=', 'pending')
        ], order='priority', limit=1)
        
        if next_reservation:
            next_reservation.action_notify_available()
            return True
        
        return False


class LibraryMember(models.Model):
    _inherit = 'library.member'

    reservation_ids = fields.One2many('library.reservation', 'member_id', string='Réservations')
    reservation_count = fields.Integer(string='Nombre de réservations',
                                        compute='_compute_reservation_count', store=True)
    pending_reservations = fields.Integer(string='Réservations en attente',
                                           compute='_compute_reservation_count', store=True)

    @api.depends('reservation_ids', 'reservation_ids.state')
    def _compute_reservation_count(self):
        for member in self:
            all_reservations = member.reservation_ids.filtered(
                lambda r: r.state in ['pending', 'available']
            )
            member.reservation_count = len(all_reservations)
            member.pending_reservations = len(
                all_reservations.filtered(lambda r: r.state == 'pending')
            )

    def action_view_reservations(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Réservations - {self.name}',
            'res_model': 'library.reservation',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id},
        }


class LibraryBorrowing(models.Model):
    _inherit = 'library.borrowing'

    def action_return(self):
        """Override pour vérifier les réservations lors du retour"""
        result = super(LibraryBorrowing, self).action_return()
        
        # Vérifier s'il y a des réservations en attente pour ce livre
        for borrowing in self:
            if borrowing.book_id.has_pending_reservations:
                borrowing.book_id._check_and_notify_next_reservation()
        
        return result
