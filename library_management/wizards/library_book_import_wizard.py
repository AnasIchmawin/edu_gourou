# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import base64
import csv
import io


class LibraryBookImportWizard(models.TransientModel):
    _name = 'library.book.import.wizard'
    _description = 'Assistant d\'import de livres'

    file_data = fields.Binary(string='Fichier CSV/Excel', required=True)
    file_name = fields.Char(string='Nom du fichier')
    import_type = fields.Selection([
        ('create', 'Créer de nouveaux livres'),
        ('update', 'Mettre à jour les livres existants'),
        ('both', 'Créer et mettre à jour'),
    ], string='Type d\'import', default='create', required=True)
    
    def action_import_books(self):
        self.ensure_one()
        
        if not self.file_data:
            raise exceptions.UserError('Veuillez sélectionner un fichier !')
        
        # Décoder le fichier
        file_content = base64.b64decode(self.file_data)
        file_io = io.StringIO(file_content.decode('utf-8'))
        
        csv_reader = csv.DictReader(file_io, delimiter=',')
        
        created_count = 0
        updated_count = 0
        error_count = 0
        errors = []
        
        for row in csv_reader:
            try:
                isbn = row.get('isbn', '').strip()
                name = row.get('title', '').strip()
                author_name = row.get('author', '').strip()
                category_name = row.get('category', '').strip()
                publisher = row.get('publisher', '').strip()
                pages = row.get('pages', '0').strip()
                
                if not name or not isbn:
                    errors.append(f"Ligne ignorée: titre ou ISBN manquant")
                    error_count += 1
                    continue
                
                # Rechercher ou créer l'auteur
                author = self.env['library.author'].search([('name', '=', author_name)], limit=1)
                if not author and author_name:
                    author = self.env['library.author'].create({'name': author_name})
                
                # Rechercher ou créer la catégorie
                category = self.env['library.category'].search([('name', '=', category_name)], limit=1)
                if not category and category_name:
                    category = self.env['library.category'].create({'name': category_name})
                
                # Vérifier si le livre existe
                existing_book = self.env['library.book'].search([('isbn', '=', isbn)], limit=1)
                
                book_vals = {
                    'name': name,
                    'isbn': isbn,
                    'author_id': author.id if author else False,
                    'category_id': category.id if category else False,
                    'publisher': publisher,
                    'pages': int(pages) if pages.isdigit() else 0,
                }
                
                if existing_book and self.import_type in ['update', 'both']:
                    existing_book.write(book_vals)
                    updated_count += 1
                elif not existing_book and self.import_type in ['create', 'both']:
                    self.env['library.book'].create(book_vals)
                    created_count += 1
                    
            except Exception as e:
                errors.append(f"Erreur: {str(e)}")
                error_count += 1
        
        # Message de résultat
        message = f"Import terminé:\n"
        message += f"- {created_count} livres créés\n"
        message += f"- {updated_count} livres mis à jour\n"
        if error_count > 0:
            message += f"- {error_count} erreurs\n"
            message += "\n".join(errors[:10])  # Afficher les 10 premières erreurs
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Import de livres',
                'message': message,
                'type': 'success' if error_count == 0 else 'warning',
                'sticky': False,
            }
        }

    def action_download_template(self):
        """Télécharger un fichier template CSV"""
        csv_data = "isbn,title,author,category,publisher,pages\n"
        csv_data += "9782070360024,L'Étranger,Albert Camus,Fiction,Gallimard,186\n"
        csv_data += "9782253006329,Vingt mille lieues sous les mers,Jules Verne,Science-Fiction,Le Livre de Poche,592\n"
        
        attachment = self.env['ir.attachment'].create({
            'name': 'template_import_livres.csv',
            'type': 'binary',
            'datas': base64.b64encode(csv_data.encode('utf-8')),
            'mimetype': 'text/csv',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
