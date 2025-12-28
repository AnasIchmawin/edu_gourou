# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Adhérent de bibliothèque'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom complet', required=True, tracking=True)
    member_number = fields.Char(string='Numéro de carte', required=True, copy=False, 
                                 readonly=True, default='Nouveau')
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Téléphone', tracking=True)
    mobile = fields.Char(string='Mobile')
    address = fields.Text(string='Adresse')
    photo = fields.Binary(string='Photo')
    
    member_type = fields.Selection([
        ('student', 'Étudiant'),
        ('teacher', 'Professeur'),
        ('staff', 'Personnel'),
        ('external', 'Externe'),
    ], string='Type d\'adhérent', required=True, default='student', tracking=True)
    
    registration_date = fields.Date(string='Date d\'adhésion', default=fields.Date.today, 
                                     required=True, tracking=True)
    expiration_date = fields.Date(string='Date d\'expiration', compute='_compute_expiration_date', 
                                   store=True, tracking=True)
    
    state = fields.Selection([
        ('active', 'Actif'),
        ('suspended', 'Suspendu'),
        ('expired', 'Expiré'),
    ], string='Statut', default='active', compute='_compute_state', store=True, tracking=True)
    
    # Statistiques
    borrowing_ids = fields.One2many('library.borrowing', 'member_id', string='Emprunts')
    penalty_ids = fields.One2many('library.penalty', 'member_id', string='Pénalités')
    membership_fee_ids = fields.One2many('library.membership.fee', 'member_id', 
                                          string='Frais d\'adhésion')
    
    total_borrowings = fields.Integer(string='Total emprunts', compute='_compute_borrowing_stats', store=True)
    current_borrowings = fields.Integer(string='Emprunts en cours', compute='_compute_borrowing_stats', store=True)
    late_borrowings = fields.Integer(string='Emprunts en retard', compute='_compute_borrowing_stats', store=True)
    returned_borrowings = fields.Integer(string='Emprunts retournés', compute='_compute_borrowing_stats', store=True)
    
    total_penalties = fields.Monetary(string='Total pénalités', compute='_compute_financial_stats',
                                       store=True, currency_field='currency_id')
    paid_penalties = fields.Monetary(string='Pénalités payées', compute='_compute_financial_stats',
                                      store=True, currency_field='currency_id')
    unpaid_penalties = fields.Monetary(string='Pénalités impayées', compute='_compute_financial_stats',
                                        store=True, currency_field='currency_id')
    
    currency_id = fields.Many2one('res.currency', string='Devise', 
                                   default=lambda self: self.env.company.currency_id)
    
    active = fields.Boolean(string='Actif', default=True)
    notes = fields.Text(string='Notes')

    _sql_constraints = [
        ('member_number_uniq', 'unique(member_number)', 
         'Le numéro de carte doit être unique !')
    ]

    @api.model
    def create(self, vals):
        if vals.get('member_number', 'Nouveau') == 'Nouveau':
            vals['member_number'] = self.env['ir.sequence'].next_by_code('library.member') or 'Nouveau'
        return super(LibraryMember, self).create(vals)

    @api.depends('registration_date')
    def _compute_expiration_date(self):
        for member in self:
            if member.registration_date:
                member.expiration_date = member.registration_date + timedelta(days=365)
            else:
                member.expiration_date = False

    @api.depends('expiration_date')
    def _compute_state(self):
        today = fields.Date.today()
        for member in self:
            if member.expiration_date:
                if member.expiration_date < today:
                    member.state = 'expired'
                else:
                    member.state = 'active'
            else:
                member.state = 'active'

    @api.depends('borrowing_ids', 'borrowing_ids.state')
    def _compute_borrowing_stats(self):
        for member in self:
            all_borrowings = member.borrowing_ids
            member.total_borrowings = len(all_borrowings)
            member.current_borrowings = len(all_borrowings.filtered(lambda b: b.state == 'borrowed'))
            member.late_borrowings = len(all_borrowings.filtered(lambda b: b.state == 'late'))
            member.returned_borrowings = len(all_borrowings.filtered(lambda b: b.state == 'returned'))

    @api.depends('penalty_ids', 'penalty_ids.state', 'penalty_ids.penalty_amount', 
                 'penalty_ids.payment_amount')
    def _compute_financial_stats(self):
        for member in self:
            all_penalties = member.penalty_ids.filtered(lambda p: p.state != 'cancelled')
            member.total_penalties = sum(all_penalties.mapped('penalty_amount'))
            member.paid_penalties = sum(all_penalties.mapped('payment_amount'))
            member.unpaid_penalties = member.total_penalties - member.paid_penalties

    def action_view_borrowings(self):
        return {
            'name': 'Emprunts',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrowing',
            'view_mode': 'tree,form',
            'domain': [('member_id', '=', self.id)],
            'context': {'default_member_id': self.id}
        }

    def action_renew_membership(self):
        """Renouveler l'adhésion pour 1 an"""
        for member in self:
            if member.expiration_date:
                new_expiration = member.expiration_date + timedelta(days=365)
            else:
                new_expiration = fields.Date.today() + timedelta(days=365)
            member.write({
                'expiration_date': new_expiration,
                'state': 'active'
            })

    def action_suspend(self):
        self.write({'state': 'suspended'})

    def action_activate(self):
        self.write({'state': 'active'})
