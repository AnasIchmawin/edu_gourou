# -*- coding: utf-8 -*-

from odoo import models, fields, api


class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Auteur de livre'
    _order = 'name'

    name = fields.Char(string='Nom complet', required=True)
    birth_date = fields.Date(string='Date de naissance')
    nationality = fields.Char(string='Nationalité')
    biography = fields.Text(string='Biographie')
    book_ids = fields.One2many('library.book', 'author_id', string='Livres')
    book_count = fields.Integer(string='Nombre de livres', compute='_compute_book_count')
    active = fields.Boolean(string='Actif', default=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        for author in self:
            author.book_count = len(author.book_ids)
