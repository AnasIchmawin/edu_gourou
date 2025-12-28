# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Livre de bibliothèque'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Titre', required=True, tracking=True)
    isbn = fields.Char(string='ISBN', size=13, tracking=True)
    author_id = fields.Many2one('library.author', string='Auteur', required=True, tracking=True)
    category_id = fields.Many2one('library.category', string='Catégorie', tracking=True)
    publisher = fields.Char(string='Éditeur')
    publication_date = fields.Date(string='Date de publication')
    pages = fields.Integer(string='Nombre de pages')
    description = fields.Text(string='Description')
    cover_image = fields.Binary(string='Image de couverture')
    
    state = fields.Selection([
        ('available', 'Disponible'),
        ('borrowed', 'Emprunté'),
        ('reserved', 'Réservé'),
        ('maintenance', 'En maintenance'),
        ('lost', 'Perdu'),
    ], string='État', default='available', required=True, tracking=True)
    
    borrowing_ids = fields.One2many('library.borrowing', 'book_id', string='Historique des emprunts')
    current_borrowing_id = fields.Many2one('library.borrowing', string='Emprunt en cours', 
                                           compute='_compute_current_borrowing', store=True)
    borrowing_count = fields.Integer(string='Nombre d\'emprunts', compute='_compute_borrowing_count')
    
    active = fields.Boolean(string='Actif', default=True)
    notes = fields.Text(string='Notes internes')

    _sql_constraints = [
        ('isbn_uniq', 'unique(isbn)', 'L\'ISBN doit être unique !')
    ]

    @api.depends('borrowing_ids', 'borrowing_ids.state')
    def _compute_current_borrowing(self):
        for book in self:
            current = book.borrowing_ids.filtered(lambda b: b.state == 'borrowed')
            book.current_borrowing_id = current[0] if current else False

    @api.depends('borrowing_ids')
    def _compute_borrowing_count(self):
        for book in self:
            book.borrowing_count = len(book.borrowing_ids)

    def action_set_available(self):
        self.write({'state': 'available'})

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})

    def action_set_lost(self):
        self.write({'state': 'lost'})

    def action_view_borrowings(self):
        return {
            'name': 'Emprunts',
            'type': 'ir.actions.act_window',
            'res_model': 'library.borrowing',
            'view_mode': 'tree,form',
            'domain': [('book_id', '=', self.id)],
            'context': {'default_book_id': self.id}
        }
