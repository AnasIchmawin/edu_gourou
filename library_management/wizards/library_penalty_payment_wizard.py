# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class LibraryPenaltyPaymentWizard(models.TransientModel):
    _name = 'library.penalty.payment.wizard'
    _description = 'Assistant de paiement de pénalité'

    penalty_id = fields.Many2one('library.penalty', string='Pénalité', required=True)
    amount = fields.Monetary(string='Montant à payer', required=True, 
                              currency_field='currency_id', digits=(10, 2))
    payment_date = fields.Date(string='Date de paiement', default=fields.Date.today, 
                                required=True)
    payment_method = fields.Selection([
        ('cash', 'Espèces'),
        ('card', 'Carte bancaire'),
        ('check', 'Chèque'),
        ('transfer', 'Virement'),
    ], string='Moyen de paiement', required=True, default='cash')
    
    currency_id = fields.Many2one('res.currency', string='Devise', 
                                   default=lambda self: self.env.company.currency_id)
    notes = fields.Text(string='Notes')

    def action_confirm_payment(self):
        self.ensure_one()
        
        if self.amount <= 0:
            raise exceptions.UserError('Le montant doit être supérieur à zéro !')
        
        if self.amount > self.penalty_id.remaining_amount:
            raise exceptions.UserError('Le montant ne peut pas dépasser le montant restant !')
        
        # Enregistrer le paiement
        new_payment = (self.penalty_id.payment_amount or 0) + self.amount
        self.penalty_id.write({
            'payment_amount': new_payment,
            'payment_date': self.payment_date,
        })
        
        # Si totalement payé, changer l'état
        if self.penalty_id.remaining_amount <= 0.01:  # Tolérance pour les arrondis
            self.penalty_id.write({'state': 'paid'})
        
        return {'type': 'ir.actions.act_window_close'}
