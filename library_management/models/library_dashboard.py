

from odoo import models, fields, api


class LibraryDashboard(models.Model):
    _name = 'library.dashboard'
    _description = 'Tableau de bord Bibliothèque'

    name = fields.Char(string='Nom', default='Tableau de bord')
    
    # Statistiques des livres
    total_books = fields.Integer(string='Total Livres', compute='_compute_book_stats')
    available_books = fields.Integer(string='Livres Disponibles', compute='_compute_book_stats')
    borrowed_books = fields.Integer(string='Livres Empruntés', compute='_compute_book_stats')
    reserved_books = fields.Integer(string='Livres Réservés', compute='_compute_book_stats')
    lost_books = fields.Integer(string='Livres Perdus', compute='_compute_book_stats')
    occupation_rate = fields.Float(string='Taux d\'occupation (%)', compute='_compute_book_stats')
    
    # Statistiques des emprunts
    total_borrowings = fields.Integer(string='Total Emprunts', compute='_compute_borrowing_stats')
    active_borrowings = fields.Integer(string='Emprunts Actifs', compute='_compute_borrowing_stats')
    late_borrowings = fields.Integer(string='Emprunts en Retard', compute='_compute_borrowing_stats')
    returned_borrowings = fields.Integer(string='Emprunts Retournés', compute='_compute_borrowing_stats')
    late_rate = fields.Float(string='Taux de retard (%)', compute='_compute_borrowing_stats')
    
    # Statistiques des membres
    total_members = fields.Integer(string='Total Adhérents', compute='_compute_member_stats')
    active_members = fields.Integer(string='Adhérents Actifs', compute='_compute_member_stats')
    expired_members = fields.Integer(string='Adhérents Expirés', compute='_compute_member_stats')
    suspended_members = fields.Integer(string='Adhérents Suspendus', compute='_compute_member_stats')
    
    # Statistiques générales
    total_authors = fields.Integer(string='Total Auteurs', compute='_compute_general_stats')
    total_categories = fields.Integer(string='Total Catégories', compute='_compute_general_stats')
    
    @api.depends()
    def _compute_book_stats(self):
        for record in self:
            total = self.env['library.book'].search_count([])
            available = self.env['library.book'].search_count([('state', '=', 'available')])
            borrowed = self.env['library.book'].search_count([('state', '=', 'borrowed')])
            reserved = self.env['library.book'].search_count([('state', '=', 'reserved')])
            lost = self.env['library.book'].search_count([('state', '=', 'lost')])
            
            record.total_books = total
            record.available_books = available
            record.borrowed_books = borrowed
            record.reserved_books = reserved
            record.lost_books = lost
            record.occupation_rate = (borrowed / total * 100) if total > 0 else 0
    
    @api.depends()
    def _compute_borrowing_stats(self):
        for record in self:
            total = self.env['library.borrowing'].search_count([])
            active = self.env['library.borrowing'].search_count([('state', '=', 'borrowed')])
            late = self.env['library.borrowing'].search_count([('state', '=', 'late')])
            returned = self.env['library.borrowing'].search_count([('state', '=', 'returned')])
            
            record.total_borrowings = total
            record.active_borrowings = active
            record.late_borrowings = late
            record.returned_borrowings = returned
            record.late_rate = (late / total * 100) if total > 0 else 0
    
    @api.depends()
    def _compute_member_stats(self):
        for record in self:
            record.total_members = self.env['library.member'].search_count([])
            record.active_members = self.env['library.member'].search_count([('state', '=', 'active')])
            record.expired_members = self.env['library.member'].search_count([('state', '=', 'expired')])
            record.suspended_members = self.env['library.member'].search_count([('state', '=', 'suspended')])
    
    @api.depends()
    def _compute_general_stats(self):
        for record in self:
            record.total_authors = self.env['library.author'].search_count([])
            record.total_categories = self.env['library.category'].search_count([])

