# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import timedelta


class LibraryBorrowing(models.Model):
    _name = 'library.borrowing'
    _description = 'Emprunt de livre'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'borrowing_date desc'

    name = fields.Char(string='Référence', required=True, copy=False, readonly=True, 
                       default='Nouveau')
    book_id = fields.Many2one('library.book', string='Livre', required=True, tracking=True)
    member_id = fields.Many2one('library.member', string='Adhérent', tracking=True)
    borrower_name = fields.Char(string='Nom de l\'emprunteur', required=True, tracking=True)
    borrower_email = fields.Char(string='Email de l\'emprunteur')
    borrower_phone = fields.Char(string='Téléphone de l\'emprunteur')
    
    borrowing_date = fields.Date(string='Date d\'emprunt', required=True, 
                                  default=fields.Date.today, tracking=True)
    expected_return_date = fields.Date(string='Date de retour prévue', required=True, 
                                        tracking=True)
    actual_return_date = fields.Date(string='Date de retour effective', tracking=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('borrowed', 'Emprunté'),
        ('returned', 'Rendu'),
        ('late', 'En retard'),
        ('lost', 'Perdu'),
    ], string='État', default='draft', required=True, tracking=True)
    
    days_borrowed = fields.Integer(string='Jours d\'emprunt', compute='_compute_days_borrowed')
    is_late = fields.Boolean(string='En retard', compute='_compute_is_late')
    late_days = fields.Integer(string='Jours de retard', compute='_compute_late_days')
    
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouveau') == 'Nouveau':
            vals['name'] = self.env['ir.sequence'].next_by_code('library.borrowing') or 'Nouveau'
        return super(LibraryBorrowing, self).create(vals)

    @api.onchange('member_id')
    def _onchange_member_id(self):
        if self.member_id:
            self.borrower_name = self.member_id.name
            self.borrower_email = self.member_id.email
            self.borrower_phone = self.member_id.phone or self.member_id.mobile

    @api.onchange('borrowing_date')
    def _onchange_borrowing_date(self):
        if self.borrowing_date:
            self.expected_return_date = self.borrowing_date + timedelta(days=14)

    @api.depends('borrowing_date', 'actual_return_date')
    def _compute_days_borrowed(self):
        for borrowing in self:
            if borrowing.borrowing_date:
                if borrowing.actual_return_date:
                    delta = borrowing.actual_return_date - borrowing.borrowing_date
                else:
                    delta = fields.Date.today() - borrowing.borrowing_date
                borrowing.days_borrowed = delta.days
            else:
                borrowing.days_borrowed = 0

    @api.depends('expected_return_date', 'actual_return_date', 'state')
    def _compute_is_late(self):
        today = fields.Date.today()
        for borrowing in self:
            if borrowing.state == 'borrowed' and borrowing.expected_return_date:
                borrowing.is_late = today > borrowing.expected_return_date
            else:
                borrowing.is_late = False

    @api.depends('expected_return_date', 'actual_return_date', 'is_late')
    def _compute_late_days(self):
        today = fields.Date.today()
        for borrowing in self:
            if borrowing.is_late and borrowing.expected_return_date:
                borrowing.late_days = (today - borrowing.expected_return_date).days
            else:
                borrowing.late_days = 0

    def action_confirm_borrowing(self):
        for borrowing in self:
            if borrowing.book_id.state != 'available':
                raise exceptions.UserError('Le livre n\'est pas disponible pour l\'emprunt !')
            borrowing.write({'state': 'borrowed'})
            borrowing.book_id.write({'state': 'borrowed'})

    def action_return_book(self):
        for borrowing in self:
            borrowing.write({
                'state': 'returned',
                'actual_return_date': fields.Date.today()
            })
            borrowing.book_id.write({'state': 'available'})

    def action_mark_lost(self):
        for borrowing in self:
            borrowing.write({'state': 'lost'})
            borrowing.book_id.write({'state': 'lost'})

    def action_cancel(self):
        for borrowing in self:
            if borrowing.state == 'borrowed':
                borrowing.book_id.write({'state': 'available'})
            borrowing.write({'state': 'draft'})

    @api.model
    def _cron_check_late_borrowings(self):
        """Cron pour marquer les emprunts en retard"""
        today = fields.Date.today()
        late_borrowings = self.search([
            ('state', '=', 'borrowed'),
            ('expected_return_date', '<', today)
        ])
        late_borrowings.write({'state': 'late'})
