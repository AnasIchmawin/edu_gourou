# -*- coding: utf-8 -*-
{
    'name': 'Gestion de Bibliothèque',
    'version': '17.0.1.0.0',
    'category': 'Services',
    'summary': 'Module de gestion de bibliothèque - Livres, Auteurs, Emprunts',
    'description': """
        Module de Gestion de Bibliothèque
        ==================================
        
        Fonctionnalités principales :
        * Gestion des livres (ISBN, titre, auteur, catégorie, état)
        * Gestion des auteurs
        * Gestion des catégories de livres
        * Gestion des emprunts et retours
        * Suivi de l'état des livres (disponible, emprunté, perdu, etc.)
        
        Projet académique - Odoo 17
    """,
    'author': 'Équipe Projet Universitaire',
    'website': 'https://www.example.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/library_data.xml',
        'views/library_book_views.xml',
        'views/library_author_views.xml',
        'views/library_category_views.xml',
        'views/library_member_views.xml',
        'views/library_borrowing_views.xml',
        'views/library_penalty_views.xml',
        'views/library_membership_fee_views.xml',
        'views/library_wizards_views.xml',
        'views/library_dashboard_views.xml',
        'views/library_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
