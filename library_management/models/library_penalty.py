# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LibraryPenalty(models.Model):
    _name = 'library.penalty'
    _description = 'Pénalité de retard'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, 
                       default='Nouveau')
    borrowing_id = fields.Many2one('library.borrowing', string='Emprunt', required=True, 
                                    tracking=True, ondelete='cascade')
    member_id = fields.Many2one('library.member', string='Adhérent', 
                                 related='borrowing_id.member_id', store=True)
    book_id = fields.Many2one('library.book', string='Livre', 
                               related='borrowing_id.book_id', store=True)
    
    late_days = fields.Integer(string='Jours de retard', required=True)
    daily_rate = fields.Float(string='Tarif par jour', default=1.0, required=True, 
                               digits=(10, 2))
    penalty_amount = fields.Monetary(string='Montant de la pénalité', 
                                      compute='_compute_penalty_amount', store=True, 
                                      currency_field='currency_id')
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('paid', 'Payée'),
        ('cancelled', 'Annulée'),
    ], string='État', default='draft', required=True, tracking=True)
    
    payment_date = fields.Date(string='Date de paiement', tracking=True)
    payment_amount = fields.Monetary(string='Montant payé', currency_field='currency_id', 
                                      tracking=True, digits=(10, 2))
    remaining_amount = fields.Monetary(string='Montant restant', 
                                        compute='_compute_remaining_amount', 
                                        store=True, currency_field='currency_id')
    
    currency_id = fields.Many2one('res.currency', string='Devise', 
                                   default=lambda self: self.env.company.currency_id)
    
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Actif', default=True)

    _sql_constraints = [
        ('borrowing_uniq', 'unique(borrowing_id)', 
         'Une pénalité existe déjà pour cet emprunt !')
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.penalty') or 'Nouveau'
        return super(LibraryPenalty, self).create(vals)

    @api.depends('late_days', 'daily_rate')
    def _compute_penalty_amount(self):
        for penalty in self:
            penalty.penalty_amount = penalty.late_days * penalty.daily_rate

    @api.depends('penalty_amount', 'payment_amount')
    def _compute_remaining_amount(self):
        for penalty in self:
            penalty.remaining_amount = penalty.penalty_amount - (penalty.payment_amount or 0)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_register_payment(self):
        self.ensure_one()
        return {
            'name': 'Enregistrer le paiement',
            'type': 'ir.actions.act_window',
            'res_model': 'library.penalty.payment.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_penalty_id': self.id,
                'default_amount': self.remaining_amount,
            }
        }

    def action_cancel(self):
        self.write({'state': 'cancelled'})
