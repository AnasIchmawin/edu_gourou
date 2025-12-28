# 📚 Module Gestion de Bibliothèque - Odoo 17

## 📋 Description

Module complet de gestion de bibliothèque pour Odoo 17, développé dans le cadre d'un projet universitaire. Ce module permet de gérer efficacement une bibliothèque avec la gestion des livres, auteurs, catégories, emprunts et un tableau de bord statistique moderne.

## ✨ Fonctionnalités

### 📊 Tableau de Bord (Nouveau!)
- **Statistiques en temps réel** :
  - Total des livres, disponibles, empruntés, perdus
  - Total des emprunts, actifs, en retard, retournés
  - Nombre d'auteurs et catégories
- **Boutons d'accès rapide** avec icônes vers les fonctionnalités principales
- **Design moderne** avec interface intuitive

### 📚 Gestion des Livres
- Enregistrement complet des livres (ISBN, titre, auteur, catégorie, éditeur)
- **Image de couverture** avec affichage optimisé
- **États des livres avec codes couleurs** :
  - 🟢 Disponible (vert)
  - 🟡 Emprunté (jaune)
  - 🔵 Réservé (bleu)
  - ⚫ En maintenance (gris)
  - 🔴 Perdu (rouge)
- Historique des emprunts par livre
- Suivi du nombre de pages et date de publication
- **Vue Kanban améliorée** avec grandes images et bordures colorées
- Compteur d'emprunts par livre
- Boutons d'actions : Marquer disponible, En maintenance, Perdu

### ✍️ Gestion des Auteurs
- Fiche complète des auteurs avec photo
- Biographie, nationalité, date de naissance
- Liste des livres par auteur
- C🎨 Améliorations Visuelles

### Design Moderne
- **CSS personnalisé** avec gradients et animations
- **Cartes Kanban stylées** avec :
  - Bordures colorées à gauche selon l'état
  - Grandes images de couverture (120x160px)
  - Effets de survol (hover)
  - Ombres et transitions fluides
- **Badges colorés** pour tous les états
- **Icônes Font Awesome** partout
- **Emojis** dans les menus et colonnes

### Interface Utilisateur
- **Tableau de bord central** avec statistiques visuelles
- **Vues multiples** : Formulaire, Liste, Kanban, Recherche
- **Filtres intelligents** et regroupements
- **Boutons d'action** contextuels avec icônes
- **Chatter** pour suivi des modifications (mail.thread)
- **Activités** planifiables (mail.activity.mixin)

## 📁 Structure du Module

```
library_management/
├── __init__.py                          # Initialisation du module
├── __manifest__.py                      # Déclaration du module
├── README.md                            # Documentation complète
├── models/                              # Modèles de données
│   ├── __init__.py
│   ├── library_book.py                  # Modèle Livre
│   ├── library_author.py                # Modèle Auteur
│   ├── library_category.py              # Modèle Catégorie
│   ├── library_borrowing.py             # Modèle Emprunt
│   └── library_dashboard.py             # Modèle Tableau de bord (NOUVEAU)
├── views/                               # Vues XML
│   ├── library_dashboard_views.xml      # Tableau de bord (NOUVEAU)
│   ├── library_book_views.xml           # Vues Livre (améliorées)
│   ├── library_author_views.xml         # Vues Auteur (améliorées)
│   ├── library_category_views.xml       # Vues Catégorie (améliorées)
│   ├── library_borrowing_views.xml      # Vues Emprunt (améliorées)
│   └── library_menus.xml                # Menus (avec tableau de bord)
├── security/                            # Droits d'accès
│   └── ir.model.access.csv              # Permissions par modèle
├── data/                                # Données de démonstration
│   └── library_data.xml                 # Catégories, auteurs, livres, séquence
├── static/                              # Ressources statiques
│   ├── description/
│   │   └── icon.png                     # Icône du module
│   └── src/
│       └── css/
│           └── library_style.css        # Styles personnalisés (NOUVEAU)
└── odoo.conf                            # Configuration Odoo (racine projet)n quotidienne** pour détecter les emprunts en retard
- Boutons d'actions : Confirmer, Retourner, Marquer perdu, Annuler

## Structure du Module
🚀 Installation

### Prérequis
- Docker et Docker Compose installés
- Ports 8069 (Odoo) et 5432 (PostgreSQL) disponibles

### Via Docker (Recommandé)

1. **Clonez ou placez le projet** :
   ```bash
   cd C:\Users\X1\Documents\edu_gourou
   ```

2. **Structure requise** :
   ```
   edu_gourou/
   ├── docker-compose.yml
   ├── library_management/          # Module Odoo
   └── odoo.conf (optionnel)
   ```

3. **Démarrez les conteneurs Docker** :
   ```bash
   docker-compose up -d
   ```
📖 Utilisation

### Menu Principal : 📚 Bibliothèque

#### 📊 Tableau de Bord (Page d'accueil)
- **Statistiques en temps réel** de toute la bibliothèque
- **Accès rapides** :
  - 📗 Voir Livres Disponibles
  - 📋 Emprunts en Cours
  - ⚠️ Emprunts en Retard

#### 📚 Livres
- **Tous les livres** : Vue complète (Kanban/Liste/Formulaire)
- **Livres disponibles** : Livres prêts à être empruntés (vue filtrée)
- **Livres empruntés** : Livres actuellement en prêt (vue filtrée)

**Actions disponibles** :
- Créer un nouveau livre
- Modifier les informations
- Changer l'état (disponible, maintenance, perdu)
- Voir l'historique des emprunts
- Archiver/Désarchiver

#### 📖 Emprunts
- **Tous les emprunts** : Historique complet
- **Emprunts en cours** : Emprunts actifs
- **Emprunts en retard** : Suivi des retards avec alertes

**Workflow d'emprunt** :
1. Créer un emprunt (état : Brouillon)
2. Confirmer l'emprunt → Livre devient "Emprunté"
3. Retourner le livre → Livre redevient "Disponible"
4. Ou marquer comme perdu

#### ⚙️ Configuration
- **Auteurs** : Gestion complète des auteurs
- **Catégories** : Organisation hiérarchique des catégories

### 🎯 Cas d'usage typiques

#### Ajouter un nouveau livre
1. Bibliothèque → Livres → Tous les livres
2. Cliquer sur "Créer"
3. Remplir : Titre, ISBN, Auteur, Catégorie, etc.
4. Ajouter une image de couverture
5. Sauvegarder

#### Créer un emprunt
1. Bibliothèque → Emprunts → Tous les emprunts
2. Cliquer sur "Créer"
3. Sélectionner le livre (doit être disponible)
4. Renseigner l'emprunteur
5. La date de retour est calculée automatiquement (14 jours)
6. Cliquer sur "Confirmer l'emprunt"

#### Retourner un livre
1. Bibliothèque → Emprunts → Emprunts en cours
2. Ouvrir l'emprunt concerné
3. Cliquer sur "Retourner le livre"
4. Le livre redevient automatiquement disponible
   - Cliquez sur "**Installer**"

### Mise à jour du module
🔧 Fonctionnalités Techniques

### Modèles de Données

#### library.book (Livre)
- **Champs** : name, isbn, author_id, category_id, publisher, publication_date, pages, description, cover_image, state
- **Héritage** : mail.thread, mail.activity.mixin (suivi et activités)
- **Relations** : Many2one vers Author et Category, One2many vers Borrowing
- **Contrainte** : ISBN unique

#### library.author (Auteur)
- **Champs** : name, birth_date, nationality, biography
- **Relations** : One2many vers Book
- **Champs calculés** : book_count

#### library.category (Catégorie)
- **Champs** : name, description, parent_id
- **Relations** : Many2one vers Category (hiérarchique), One2many vers Book
- **Champs calculés** : book_count
- **Contrainte** : Nom unique

#### library.borrowing (Emprunt)
- **Champs** : name, book_id, borrower_name, borrower_email, borrowing_date, expected_return_date, actual_return_date, state
- **Héritage** : mail.thread, mail.activity.mixin
- **Relations** : Many2one vers Book
- **Champs calculés** : days_borrowed, is_late, late_days
- **Séquence** : EMP00001, EMP00002...

###🔗 Intégration Odoo Standard

### Héritages Odoo
- **mail.thread** : Chatter pour suivi des modifications et messages
- **mail.activity.mixin** : Planification et suivi d'activités

### Contraintes SQL
- `isbn_uniq` : ISBN unique pour chaque livre
- `name_uniq` : Nom de catégorie unique

### Relations ORM
- **Many2one** : book → author, book → category, borrowing → book
- **One2many** : author → books, category → books, book → borrowings

### Types de Champs
- **Char** : Texte court (name, isbn, email, phone)
- **Text** : Texte long (description, biography, notes)
- **Date** : Dates (birth_date, borrowing_date, return_date)
- *🎓 Contexte Académique

### Objectifs Pédagogiques
Ce module a été développé dans le cadre d'un **projet universitaire** pour démontrer :

1. **Maîtrise du paramétrage Odoo 17** :
   - Configuration de modules
   - Création de modèles de données
   - Conception de vues XML
   - Relations entre objets

2. **Compétences techniques** :
   - Développement Python orienté objet
   - Framework Odoo (ORM, API)
   - Gestion de base de données relationnelle
   - Interface utilisateur moderne

3. **Concepts métier** :
   - Gestion de bibliothèque
   - Workflow d'emprunts
   - États et transitions
   - Statistiques et reporting

### Points Forts du Module
✅ **Structure professionnelle** respectant les standards Odoo  
✅ **Code propre et documenté** en français  
✅ **Interface moderne** avec design soigné  
✅ **Fonctionnalités complètes** et opérationnelles  
✅ **Données de démonstration** pour présentation  
✅ **Documentation complète** (README)  

### Évolutions Possibles
- 📱 Application mobile
- 📧 Notifications email automatiques
- 💰 Gestion des pénalités de retard
- 👥 Gestion des membres/adhérents
- 📊 Rapports et analyses avancées
- 🔒 Gestion des droits par rôle
- 📍 Localisation physique des livres (étagères)
- 🔄 Réservations de livres
- 📚 Gestion de plusieurs exemplaires
- 📈 Graphiques et tableaux de bord avancés

## 👨‍💻 Auteur

Développé par **Équipe Projet Universitaire**  
Dans le cadre d'un TP/Projet de gestion avec Odoo 17

## 📄 Licence

**LGPL-3** - Licence Publique Générale GNU (version 3)

Ce module est un logiciel libre. Vous pouvez le redistribuer et/ou le modifier selon les termes de la licence LGPL-3.

## 🆘 Support

### Pour les Questions
- Consultez cette documentation complète
- Vérifiez les logs Odoo : `docker-compose logs -f web`
- Mode debug Odoo : Paramètres → Activer le mode développeur

### Problèmes Courants

**Le module n'apparaît pas** :
```bash
# Redémarrer Docker
docker-compose restart

# Dans Odoo : Apps → Mettre à jour la liste des applications
```

**Erreur lors de l'installation** :
- Vérifiez les logs : `docker-compose logs web`
- Vérifiez les droits d'accès (security/ir.model.access.csv)
- Assurez-vous que tous les fichiers XML sont valides

**Le tableau de bord est vide** :
- Créez quelques livres et emprunts
- Les statistiques se calculent automatiquement

### Contact
Pour toute question ou assistance :
- Consultez votre **professeur**
- Contactez l'**équipe du projet**

## 🙏 Remerciements

Merci à :
- La communauté **Odoo** pour la documentation
- Les **enseignants** pour l'encadrement
- L'équipe **Docker** pour la conteneurisation

---

**Version** : 17.0.1.0.0  
**Date** : Décembre 2025  
**Statut** : ✅ Production Ready  

📚 **Bonne gestion de votre bibliothèque !** 🎉
- **statusbar** : Barre d'état workflow

### Décorateurs Python
- `@api.depends()` : Champs calculés avec dépendances
- `@api.onchange()` : Actions au changement de champ
- `@api.model` : Méthodes de classe
- `@api.constrains()` : Validations personnalisées (non utilisé ici)

### Tâche Cron (ir.cron)
- **Nom** : Vérifier les emprunts en retard
- **Modèle** : library.borrowing
- **Méthode** : _cron_check_late_borrowings()
- **Fréquence** : Quotidienne (1 jour)
- **Type** : Récurrent (-1 exécutions)

## 📦 Dépendances

### Modules Odoo Requis
- **base** : Module de base Odoo (obligatoire)
- **mail** : Système de messagerie et chatter

### Technologies
- **Odoo 17.0** : Framework ERP
- **Python 3.10+** : Langage de programmation
- **PostgreSQL 15** : Base de données
- **Docker** : Conteneurisation
- **XML** : Déclaration des vues
- **CSS3** : Styles personnalisés
- **JavaScript** : (via framework Odoo)

### Configuration Docker
```yaml
services:
  web:
    image: odoo:17.0
    ports: 8069:8069
    volumes:
      - ./library_management:/mnt/extra-addons/library_management
  db:
    image: postgres:15
```Python
- `action_confirm_borrowing()` : Confirme l'emprunt, change l'état du livre
- `action_return_book()` : Retourne le livre, met à jour la date
- `action_mark_lost()` : Marque livre et emprunt comme perdus
- `action_set_available/maintenance/lost()` : Change l'état du livre
- `_cron_check_late_borrowings()` : Détecte les retards quotidiennement

### Vues et Interfaces
- **Formulaire** : Saisie détaillée avec onglets (notebook)
- **Liste (Tree)** : Vue tabulaire avec décorations conditionnelles
- **Kanban** : Cartes visuelles avec images et bordures colorées
- **Recherche** : Filtres avancés, regroupements (group_by), domaines
- **Statusbar** : Barre d'état pour workflow visuel

### Droits d'Accès (ir.model.access.csv)
- Lecture, écriture, création, suppression pour tous les modèles
- Groupe : base.group_user (utilisateurs internes)
- Dashboard en lecture seule

### CSS et Assets
- **Fichier CSS personnalisé** : library_style.css
- **Badges colorés** avec classes Bootstrap
- **Effets hover** et transitions
- **Gradients** et ombres moderne
   - Connectez-vous à Odoo (http://localhost:8069)
   - Allez dans Paramètres → Général
   - Activez le mode développeur

4. **Installez le module** :
   - Allez dans Apps
   - Cliquez sur "Mettre à jour la liste des applications"
   - Recherchez "Gestion de Bibliothèque"
   - Cliquez sur "Installer"

## Utilisation

### Menu Principal : Bibliothèque

#### 📚 Livres
- **Tous les livres** : Vue complète de tous les livres
- **Livres disponibles** : Livres prêts à être empruntés
- **Livres empruntés** : Livres actuellement en prêt

#### 📖 Emprunts
- **Tous les emprunts** : Historique complet
- **Emprunts en cours** : Emprunts actifs
- **Emprunts en retard** : Suivi des retards

#### ⚙️ Configuration
- **Auteurs** : Gestion des auteurs
- **Catégories** : Organisation des catégories

## Données de Démonstration

Le module inclut des données de démonstration :

### Catégories
- Fiction (avec sous-catégories : Science-Fiction, Fantasy)
- Non-Fiction (avec sous-catégories : Sciences, Histoire, Technologie)

### Auteurs
- Victor Hugo
- Jules Verne
- Albert Camus

### Livres
- Les Misérables (Victor Hugo)
- Vingt mille lieues sous les mers (Jules Verne)
- L'Étranger (Albert Camus)

## Fonctionnalités Techniques

### Champs Calculés
- Nombre de livres par auteur
- Nombre de livres par catégorie
- Jours d'emprunt
- Jours de retard
- Emprunt en cours

### Actions Automatiques
- Séquence automatique pour les emprunts (EMP00001, EMP00002, etc.)
- Date de retour prévue calculée automatiquement (14 jours)
- Détection automatique des emprunts en retard (tâche cron quotidienne)
- Mise à jour automatique de l'état des livres

### Boutons d'Action
- Marquer un livre disponible / en maintenance / perdu
- Confirmer un emprunt
- Retourner un livre
- Marquer un livre comme perdu
- Annuler un emprunt

### Vues Disponibles
- **Formulaire** : Saisie détaillée
- **Liste** : Vue tabulaire
- **Kanban** : Vue carte (livres et emprunts)
- **Recherche** : Filtres et regroupements avancés

## Intégration Odoo

Le module utilise les fonctionnalités standard d'Odoo :
- **mail.thread** : Suivi des modifications (chatter)
- **mail.activity.mixin** : Planification d'activités
- **Contraintes SQL** : ISBN unique, catégories uniques
- **Relations** : Many2one, One2many
- **États** : Selection avec statusbar
- **Widgets** : Badge, Image, Email, Phone

## Prérequis

- Odoo 17.0
- Python 3.10+
- PostgreSQL 15
- Module base
- Module mail

## Auteur

Développé dans le cadre d'un projet universitaire pour la démonstration du paramétrage et de la configuration d'Odoo 17.

## Licence

LGPL-3

## Support

Pour toute question ou assistance, veuillez contacter votre professeur ou l'équipe du projet.
