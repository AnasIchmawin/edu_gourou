# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Catégorie de livre'
    _order = 'name'

    name = fields.Char(string='Nom de la catégorie', required=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one('library.category', string='Catégorie parente', ondelete='cascade')
    child_ids = fields.One2many('library.category', 'parent_id', string='Sous-catégories')
    book_ids = fields.One2many('library.book', 'category_id', string='Livres')
    book_count = fields.Integer(string='Nombre de livres', compute='_compute_book_count')
    active = fields.Boolean(string='Active', default=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        for category in self:
            category.book_count = len(category.book_ids)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Le nom de la catégorie doit être unique !')
    ]
