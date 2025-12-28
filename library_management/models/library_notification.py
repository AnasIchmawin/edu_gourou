# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class LibraryNotificationSettings(models.Model):
    _name = 'library.notification.settings'
    _description = 'Paramètres de notifications'

    name = fields.Char(string='Nom', default='Paramètres de notifications', required=True)
    
    # Notifications pour emprunts
    enable_due_soon_notification = fields.Boolean(string='Rappel avant échéance', default=True)
    due_soon_days = fields.Integer(string='Nombre de jours avant échéance', default=2,
                                    help='Envoyer un rappel X jours avant la date de retour')
    
    enable_overdue_notification = fields.Boolean(string='Alerte retard', default=True)
    overdue_frequency_days = fields.Integer(string='Fréquence rappel retard (jours)', default=3,
                                             help='Envoyer un rappel tous les X jours pour les retards')
    
    # Notifications pour adhérents
    enable_membership_expiring = fields.Boolean(string='Adhésion expire bientôt', default=True)
    membership_expiring_days = fields.Integer(string='Jours avant expiration', default=7,
                                               help='Alerter X jours avant expiration de l\'adhésion')
    
    # Notifications pour livres
    enable_book_available_notification = fields.Boolean(string='Livre disponible', default=True,
                                                         help='Notifier quand un livre redevient disponible')
    
    # Paramètres généraux
    notification_method = fields.Selection([
        ('email', 'Email uniquement'),
        ('odoo', 'Notification Odoo uniquement'),
        ('both', 'Email et Odoo'),
    ], string='Méthode de notification', default='both', required=True)
    
    active = fields.Boolean(string='Actif', default=True)

    @api.model
    def get_settings(self):
        """Récupérer les paramètres actifs"""
        settings = self.search([('active', '=', True)], limit=1)
        if not settings:
            settings = self.create({'name': 'Paramètres de notifications'})
        return settings


class LibraryNotificationLog(models.Model):
    _name = 'library.notification.log'
    _description = 'Journal des notifications'
    _order = 'create_date desc'

    name = fields.Char(string='Référence', required=True, default='Nouveau')
    notification_type = fields.Selection([
        ('due_soon', 'Rappel échéance proche'),
        ('overdue', 'Alerte retard'),
        ('membership_expiring', 'Adhésion expire'),
        ('book_available', 'Livre disponible'),
    ], string='Type', required=True)
    
    recipient_id = fields.Many2one('library.member', string='Destinataire')
    recipient_email = fields.Char(string='Email destinataire')
    
    borrowing_id = fields.Many2one('library.borrowing', string='Emprunt')
    book_id = fields.Many2one('library.book', string='Livre')
    
    sent_date = fields.Datetime(string='Date d\'envoi', default=fields.Datetime.now)
    status = fields.Selection([
        ('sent', 'Envoyé'),
        ('failed', 'Échec'),
    ], string='État', default='sent', required=True)
    
    method = fields.Selection([
        ('email', 'Email'),
        ('odoo', 'Notification Odoo'),
    ], string='Méthode', required=True)
    
    error_message = fields.Text(string='Message d\'erreur')
    active = fields.Boolean(string='Actif', default=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.notification.log') or 'Nouveau'
        return super(LibraryNotificationLog, self).create(vals)


class LibraryBorrowing(models.Model):
    _inherit = 'library.borrowing'

    last_reminder_date = fields.Date(string='Dernier rappel envoyé')
    reminder_count = fields.Integer(string='Nombre de rappels', default=0)

    @api.model
    def _cron_send_due_soon_notifications(self):
        """Cron job: Envoyer rappels pour emprunts bientôt échus"""
        settings = self.env['library.notification.settings'].get_settings()
        
        if not settings.enable_due_soon_notification:
            return
        
        target_date = datetime.now().date() + timedelta(days=settings.due_soon_days)
        
        borrowings = self.search([
            ('state', '=', 'borrowed'),
            ('expected_return_date', '=', target_date),
            '|', ('last_reminder_date', '=', False),
            ('last_reminder_date', '<', fields.Date.today())
        ])
        
        for borrowing in borrowings:
            borrowing._send_notification('due_soon', settings)

    @api.model
    def _cron_send_overdue_notifications(self):
        """Cron job: Envoyer rappels pour emprunts en retard"""
        settings = self.env['library.notification.settings'].get_settings()
        
        if not settings.enable_overdue_notification:
            return
        
        borrowings = self.search([
            ('state', 'in', ['borrowed', 'late']),
            ('expected_return_date', '<', fields.Date.today()),
        ])
        
        for borrowing in borrowings:
            # Vérifier la fréquence des rappels
            if borrowing.last_reminder_date:
                days_since_last = (fields.Date.today() - borrowing.last_reminder_date).days
                if days_since_last < settings.overdue_frequency_days:
                    continue
            
            borrowing._send_notification('overdue', settings)

    def _send_notification(self, notification_type, settings=None):
        """Envoyer une notification pour cet emprunt"""
        self.ensure_one()
        
        if not settings:
            settings = self.env['library.notification.settings'].get_settings()
        
        if not self.member_id or not self.member_id.email:
            return False
        
        # Préparer le contexte pour le template
        context = {
            'borrowing': self,
            'member': self.member_id,
            'book': self.book_id,
            'due_date': self.expected_return_date,
        }
        
        success = False
        
        # Envoi email
        if settings.notification_method in ['email', 'both']:
            template_xmlid = f'library_management.email_template_{notification_type}'
            try:
                template = self.env.ref(template_xmlid)
                template.send_mail(self.id, force_send=True)
                self._log_notification(notification_type, 'email', 'sent')
                success = True
            except Exception as e:
                self._log_notification(notification_type, 'email', 'failed', str(e))
        
        # Notification Odoo
        if settings.notification_method in ['odoo', 'both']:
            try:
                message_dict = self._get_notification_message(notification_type)
                self.message_post(**message_dict)
                self._log_notification(notification_type, 'odoo', 'sent')
                success = True
            except Exception as e:
                self._log_notification(notification_type, 'odoo', 'failed', str(e))
        
        # Mettre à jour le compteur
        if success:
            self.write({
                'last_reminder_date': fields.Date.today(),
                'reminder_count': self.reminder_count + 1,
            })
        
        return success

    def _get_notification_message(self, notification_type):
        """Obtenir le message de notification"""
        messages = {
            'due_soon': {
                'subject': f'Rappel: Retour du livre "{self.book_id.name}"',
                'body': f'Bonjour {self.member_id.name},<br/><br/>'
                        f'Nous vous rappelons que le livre <b>{self.book_id.name}</b> doit être '
                        f'retourné le <b>{self.expected_return_date}</b>.<br/><br/>'
                        f'Merci de respecter cette date pour éviter toute pénalité.',
            },
            'overdue': {
                'subject': f'RETARD: Livre "{self.book_id.name}" non retourné',
                'body': f'Bonjour {self.member_id.name},<br/><br/>'
                        f'Le livre <b>{self.book_id.name}</b> devait être retourné le '
                        f'<b>{self.expected_return_date}</b>.<br/><br/>'
                        f'Votre emprunt est en retard de <b>{self.days_late} jours</b>. '
                        f'Merci de retourner le livre au plus vite pour éviter des pénalités supplémentaires.',
            },
        }
        return messages.get(notification_type, {})

    def _log_notification(self, notification_type, method, status, error_message=None):
        """Enregistrer la notification dans le journal"""
        self.env['library.notification.log'].create({
            'notification_type': notification_type,
            'recipient_id': self.member_id.id,
            'recipient_email': self.member_id.email,
            'borrowing_id': self.id,
            'book_id': self.book_id.id,
            'method': method,
            'status': status,
            'error_message': error_message,
        })


class LibraryMember(models.Model):
    _inherit = 'library.member'

    @api.model
    def _cron_send_membership_expiring_notifications(self):
        """Cron job: Alerter pour adhésions qui expirent bientôt"""
        settings = self.env['library.notification.settings'].get_settings()
        
        if not settings.enable_membership_expiring:
            return
        
        target_date = datetime.now().date() + timedelta(days=settings.membership_expiring_days)
        
        members = self.search([
            ('state', '=', 'active'),
            ('expiration_date', '=', target_date),
        ])
        
        for member in members:
            member._send_membership_notification(settings)

    def _send_membership_notification(self, settings=None):
        """Envoyer notification d'expiration d'adhésion"""
        self.ensure_one()
        
        if not settings:
            settings = self.env['library.notification.settings'].get_settings()
        
        if not self.email:
            return False
        
        # Notification Odoo
        if settings.notification_method in ['odoo', 'both']:
            try:
                self.message_post(
                    subject=f'Votre adhésion expire bientôt',
                    body=f'Bonjour {self.name},<br/><br/>'
                         f'Votre adhésion à la bibliothèque expire le <b>{self.expiration_date}</b>.<br/><br/>'
                         f'Pensez à la renouveler pour continuer à emprunter des livres.',
                )
                self._log_membership_notification('odoo', 'sent')
            except Exception as e:
                self._log_membership_notification('odoo', 'failed', str(e))
        
        # Email
        if settings.notification_method in ['email', 'both']:
            try:
                template = self.env.ref('library_management.email_template_membership_expiring')
                template.send_mail(self.id, force_send=True)
                self._log_membership_notification('email', 'sent')
            except Exception as e:
                self._log_membership_notification('email', 'failed', str(e))
        
        return True

    def _log_membership_notification(self, method, status, error_message=None):
        """Enregistrer la notification d'adhésion"""
        self.env['library.notification.log'].create({
            'notification_type': 'membership_expiring',
            'recipient_id': self.id,
            'recipient_email': self.email,
            'method': method,
            'status': status,
            'error_message': error_message,
        })
