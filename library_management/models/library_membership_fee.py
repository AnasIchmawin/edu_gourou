# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class LibraryMembershipFee(models.Model):
    _name = 'library.membership.fee'
    _description = 'Frais d\'adhésion'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'payment_date desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, 
                       default='Nouveau')
    member_id = fields.Many2one('library.member', string='Adhérent', required=True, 
                                 tracking=True, ondelete='cascade')
    member_type = fields.Selection(related='member_id.member_type', string='Type d\'adhérent', 
                                    store=True)
    
    fee_amount = fields.Monetary(string='Montant de la cotisation', required=True, 
                                  currency_field='currency_id', digits=(10, 2), tracking=True)
    payment_date = fields.Date(string='Date de paiement', default=fields.Date.today, 
                                required=True, tracking=True)
    validity_start = fields.Date(string='Début de validité', default=fields.Date.today, 
                                  required=True, tracking=True)
    validity_end = fields.Date(string='Fin de validité', compute='_compute_validity_end', 
                                store=True, tracking=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('paid', 'Payé'),
        ('cancelled', 'Annulé'),
    ], string='État', default='draft', required=True, tracking=True)
    
    payment_method = fields.Selection([
        ('cash', 'Espèces'),
        ('card', 'Carte bancaire'),
        ('check', 'Chèque'),
        ('transfer', 'Virement'),
    ], string='Moyen de paiement', tracking=True)
    
    currency_id = fields.Many2one('res.currency', string='Devise', 
                                   default=lambda self: self.env.company.currency_id)
    
    notes = fields.Text(string='Notes')
    active = fields.Boolean(string='Actif', default=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.membership.fee') or 'Nouveau'
        return super(LibraryMembershipFee, self).create(vals)

    @api.depends('validity_start')
    def _compute_validity_end(self):
        for fee in self:
            if fee.validity_start:
                fee.validity_end = fee.validity_start + timedelta(days=365)
            else:
                fee.validity_end = False

    @api.onchange('member_id')
    def _onchange_member_id(self):
        if self.member_id:
            # Tarifs selon le type d'adhérent
            fees = {
                'student': 10.0,
                'teacher': 20.0,
                'staff': 15.0,
                'external': 30.0,
            }
            self.fee_amount = fees.get(self.member_id.member_type, 20.0)

    def action_confirm_payment(self):
        for fee in self:
            fee.write({'state': 'paid'})
            # Mettre à jour la date d'expiration de l'adhérent
            if fee.member_id:
                fee.member_id.write({
                    'expiration_date': fee.validity_end,
                    'state': 'active'
                })

    def action_cancel(self):
        self.write({'state': 'cancelled'})
