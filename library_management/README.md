# Module Gestion de Bibliothèque - Odoo 17

## Description

Module de gestion de bibliothèque pour Odoo 17, développé dans le cadre d'un projet universitaire. Ce module permet de gérer efficacement une bibliothèque avec la gestion des livres, auteurs, catégories et emprunts.

## Fonctionnalités

### 📚 Gestion des Livres
- Enregistrement complet des livres (ISBN, titre, auteur, catégorie, éditeur)
- Image de couverture
- États des livres : Disponible, Emprunté, Réservé, En maintenance, Perdu
- Historique des emprunts par livre
- Suivi du nombre de pages et date de publication

### ✍️ Gestion des Auteurs
- Fiche complète des auteurs
- Biographie, nationalité, date de naissance
- Liste des livres par auteur
- Compteur de livres

### 🗂️ Gestion des Catégories
- Catégories et sous-catégories hiérarchiques
- Description détaillée
- Organisation des livres par catégorie

### 📖 Gestion des Emprunts
- Création d'emprunts avec référence automatique
- Informations complètes de l'emprunteur
- Dates d'emprunt et de retour (prévue/effective)
- États : Brouillon, Emprunté, Rendu, En retard, Perdu
- Calcul automatique des jours d'emprunt et de retard
- Notifications et suivi automatique
- Tâche cron pour détecter les emprunts en retard

## Structure du Module

```
library_management/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── library_book.py
│   ├── library_author.py
│   ├── library_category.py
│   └── library_borrowing.py
├── views/
│   ├── library_book_views.xml
│   ├── library_author_views.xml
│   ├── library_category_views.xml
│   ├── library_borrowing_views.xml
│   └── library_menus.xml
├── security/
│   └── ir.model.access.csv
├── data/
│   └── library_data.xml
├── static/
│   └── description/
│       └── icon.png
└── README.md
```

## Installation

### Via Docker (Recommandé)

1. **Assurez-vous que le module est dans le répertoire des addons** :
   ```bash
   cd /chemin/vers/edu_gourou
   ```

2. **Redémarrez les conteneurs Docker** :
   ```bash
   docker-compose restart
   ```

3. **Activez le mode développeur dans Odoo** :
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
