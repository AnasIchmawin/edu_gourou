# 📚 Module Gestion de Bibliothèque - Odoo 17

## � Table des Matières

1. [Description](#-description)
2. [Démarrage Rapide](#-démarrage-rapide)
3. [Fonctionnalités Principales](#-fonctionnalités-principales)
4. [Structure du Module](#-structure-du-module)
5. [Installation](#-installation)
6. [Utilisation](#-utilisation)
7. [Fonctionnalités Techniques](#-fonctionnalités-techniques)
8. [Contexte Académique](#-contexte-académique)
9. [Support et Dépannage](#-support)

---

## 📋 Description

**Module professionnel de gestion de bibliothèque** pour Odoo 17, développé dans le cadre d'un projet universitaire. 

Ce module complet permet de gérer efficacement tous les aspects d'une bibliothèque moderne :
- 📚 Catalogue de livres avec images et métadonnées
- 👥 Gestion des adhérents avec suivi des adhésions
- 📖 Emprunts avec workflow automatisé
- 💰 Gestion financière (pénalités et cotisations)
- 🔔 Système de notifications automatiques
- 📊 Tableau de bord et rapports analytiques
- 📥 Import/Export de données

**Version :** 17.0.1.0.0  
**Licence :** LGPL-3  
**Langue :** Français

---

## ⚡ Démarrage Rapide

```bash
# 1. Cloner/télécharger le projet
cd C:\Users\X1\Documents\edu_gourou

# 2. Démarrer Docker
docker-compose up -d

# 3. Accéder à Odoo
# Navigateur → http://localhost:8069

# 4. Installer le module
# Apps → Rechercher "Gestion de Bibliothèque" → Installer
```

---

## ✨ Fonctionnalités Principales

### 📊 Tableau de Bord et Rapports (Catégorie 5)
- **Statistiques en temps réel** :
  - Total des livres, disponibles, empruntés, perdus
  - Total des emprunts, actifs, en retard, retournés
  - Statistiques des adhérents (actifs, expirés, suspendus)
- **Boutons d'accès rapide** avec icônes vers les fonctionnalités principales
- **Vues analytiques** :
  - Graphiques en barres (emprunts par mois)
  - Graphiques en camembert (livres par catégorie/état)
  - Tableaux croisés dynamiques (Pivot)
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
- Compteur de livres par auteur

### 👥 Gestion des Membres/Adhérents (Catégorie 1)
- **Fiches complètes des adhérents** :
  - Numéro de carte unique (ADH00001, ADH00002...)
  - Types : Étudiant, Enseignant, Personnel, Externe
  - Dates d'inscription et d'expiration
  - Photo et coordonnées complètes
- **États automatiques** :
  - 🟢 Actif : Adhésion valide
  - 🟡 Expiré : Adhésion périmée
  - 🔴 Suspendu : Compte bloqué
- **Statistiques en temps réel** :
  - Total emprunts, emprunts en cours, en retard
  - Total pénalités, pénalités payées, impayées
- **Smart buttons** : Accès rapide aux emprunts et pénalités
- **Actions** : Renouveler, Suspendre, Activer
- **Vue Kanban** avec photos et statistiques

### 💰 Gestion Financière Simple (Catégorie 3)

#### Pénalités de Retard
- **Calcul automatique** : Jours de retard × Tarif par jour
- **Workflow complet** : Brouillon → Confirmée → Payée
- **Paiements partiels** : Enregistrer des paiements progressifs
- **Assistant de paiement** : Wizard avec moyens de paiement
- **Suivi** : Montant total, payé, restant
- **Lien avec emprunts** : Création automatique pour les retards

#### Frais d'Adhésion
- **Tarifs par type** :
  - Étudiant : 10€
  - Enseignant : 20€
  - Personnel : 15€
  - Externe : 30€
- **Validité d'1 an** calculée automatiquement
- **Renouvellement** : Met à jour l'expiration de l'adhérent
- **Moyens de paiement** : Espèces, Carte, Chèque, Virement
- **Historique complet** sur la fiche adhérent

### 🔔 Notifications et Alertes (Catégorie 6)

#### Notifications Automatiques
- **Rappel échéance proche** : X jours avant la date de retour (configurable)
- **Alerte retard** : Rappels périodiques pour emprunts en retard
- **Adhésion expire** : Notification avant expiration de l'adhésion
- **Livre disponible** : Alerte quand un livre redevient disponible

#### Système Configurable
- **Méthodes** : Email, Notification Odoo, ou les deux
- **Paramètres personnalisables** :
  - Nombre de jours avant échéance pour rappel (défaut: 2)
  - Fréquence des rappels de retard (défaut: tous les 3 jours)
  - Nombre de jours avant expiration adhésion (défaut: 7)
- **Activation/désactivation** par type de notification
- **Templates d'emails** professionnels avec design moderne

#### Journal des Notifications
- **Historique complet** de toutes les notifications envoyées
- **Suivi des échecs** avec messages d'erreur détaillés
- **Filtres intelligents** : Par type, état, destinataire
- **Vue dédiée** pour les notifications échouées
- **Statistiques** : Taux de succès, échecs par type

#### Cron Jobs Automatiques
- ⏰ **Vérification quotidienne** des échéances proches
- ⏰ **Vérification quotidienne** des retards
- ⏰ **Vérification quotidienne** des adhésions expirant

### 📥 Import/Export et Intégration (Catégorie 11)

#### Import de Catalogue CSV
- **Assistant d'import** avec interface intuitive
- **3 modes d'import** :
  - Créer de nouveaux livres uniquement
  - Mettre à jour les livres existants (par ISBN)
  - Créer et mettre à jour (mode mixte)
- **Téléchargement de template** CSV avec exemples
- **Création automatique** :
  - Auteurs manquants créés automatiquement
  - Catégories manquantes créées automatiquement
- **Format CSV simple** :
  ```csv
  isbn,title,author,category,publisher,pages
  9782070360024,L'Étranger,Albert Camus,Fiction,Gallimard,186
  ```
- **Rapport d'import détaillé** :
  - Nombre de livres créés
  - Nombre de livres mis à jour
  - Liste des erreurs éventuelles

### � Système de Réservations (Catégorie 4)

#### Réserver des Livres
- **Réservation de livres empruntés** : Mettre un livre en attente
- **File d'attente automatique** : Gestion des priorités (premier arrivé, premier servi)
- **Limite de réservations** : Maximum 3 réservations par adhérent
- **Numérotation** : RES00001, RES00002...

#### États des Réservations
- 🟡 **En attente** : Livre pas encore disponible
- 🟢 **Disponible** : Livre prêt à être récupéré
- ✅ **Récupéré** : Emprunt créé automatiquement
- ⏰ **Expiré** : Délai de récupération dépassé (3 jours)
- ❌ **Annulé** : Réservation annulée

#### Notifications Automatiques
- **Email de confirmation** : Dès la création de la réservation
- **Notification de disponibilité** : Quand le livre est retourné
- **Délai de récupération** : 3 jours pour venir chercher le livre
- **Expiration automatique** : Si non récupéré dans les délais

#### Gestion Intelligente
- **Position dans la file** : Affichage de la priorité
- **Passage automatique** : Au suivant si expiration ou annulation
- **Smart buttons** : Sur livres et adhérents
- **Onglet dédié** : Historique des réservations par adhérent

#### Cron Jobs
- ⏰ **Vérification quotidienne** des réservations expirées
- ⏰ **Traitement horaire** de la file d'attente (livres retournés)

### �📖 Gestion des Emprunts
- **Workflow complet** : Brouillon → Emprunté → Retourné/En retard
- **Numérotation automatique** : EMP00001, EMP00002...
- **Calcul automatique** de la date de retour (14 jours)
- **Détection des retards** : Changement d'état automatique
- **Lien avec adhérents** : Auto-remplissage des informations
- **Historique** : Traçabilité complète de chaque emprunt
- **Cron job quotidien** pour détecter les emprunts en retard
- **Suivi des rappels** : Date et nombre de rappels envoyés
- **Boutons d'actions** : Confirmer, Retourner, Marquer perdu, Annuler

### 🗂️ Gestion des Catégories
- **Structure hiérarchique** : Catégories et sous-catégories
- **Arbre de navigation** : Vue parent/enfant
- **Compteur de livres** par catégorie
- **Descriptions** : Texte explicatif pour chaque catégorie
- **Catégories de démonstration** : 7 catégories pré-configurées

## 📁 Structure du Module

```
library_management/
├── __init__.py                          # Initialisation du module
├── __manifest__.py                      # Déclaration du module
├── README.md                            # Documentation complète
├── models/                              # Modèles de données (11 modèles)
│   ├── __init__.py
│   ├── library_book.py                  # Modèle Livre
│   ├── library_author.py                # Modèle Auteur
│   ├── library_category.py              # Modèle Catégorie
│   ├── library_member.py                # Modèle Adhérent
│   ├── library_borrowing.py             # Modèle Emprunt
│   ├── library_penalty.py               # Modèle Pénalité (NOUVEAU)
│   ├── library_membership_fee.py        # Modèle Frais adhésion (NOUVEAU)
│   ├── library_notification.py          # Modèle Notification (NOUVEAU)
│   └── library_dashboard.py             # Modèle Tableau de bord
├── wizards/                             # Assistants (NOUVEAU)
│   ├── __init__.py
│   ├── library_penalty_payment_wizard.py      # Assistant paiement pénalité
│   └── library_book_import_wizard.py          # Assistant import CSV
├── views/                               # Vues XML
│   ├── library_dashboard_views.xml      # Tableau de bord + Rapports
│   ├── library_book_views.xml           # Vues Livre (améliorées)
│   ├── library_author_views.xml         # Vues Auteur (améliorées)
│   ├── library_category_views.xml       # Vues Catégorie (améliorées)
│   ├── library_member_views.xml         # Vues Adhérent (NOUVEAU)
│   ├── library_borrowing_views.xml      # Vues Emprunt (améliorées)
│   ├── library_penalty_views.xml        # Vues Pénalité (NOUVEAU)
│   ├── library_membership_fee_views.xml # Vues Frais adhésion (NOUVEAU)
│   ├── library_notification_views.xml   # Vues Notification (NOUVEAU)
│   ├── library_wizards_views.xml        # Vues Assistants (NOUVEAU)
│   └── library_menus.xml                # Menus complets
├── security/                            # Droits d'accès
│   └── ir.model.access.csv              # Permissions pour tous les modèles
├── data/                                # Données et configuration
│   ├── library_data.xml                 # Données de démo + Séquences
│   └── library_notification_data.xml    # Templates email + Cron jobs (NOUVEAU)
├── static/                              # Ressources statiques
│   ├── description/
│   │   └── icon.png                     # Icône du module
│   └── src/
│       └── css/
│           └── library_style.css        # Styles personnalisés
└── docker-compose.yml                   # Configuration Docker (racine projet)
- **Activation/désactivation** par type de notification
- **Templates d'emails** professionnels avec design moderne

#### Journal des Notifications
- **Historique complet** de toutes les notifications envoyées
- **Suivi des échecs** avec messages d'erreur détaillés
- **Filtres intelligents** : Par type, état, destinataire
- **Vue dédiée** pour les notifications échouées
- **Statistiques** : Taux de succès, échecs par type

#### Cron Jobs Automatiques
- ⏰ **Vérification quotidienne** des échéances proches
- ⏰ **Vérification quotidienne** des retards
- ⏰ **Vérification quotidienne** des adhésions expirant

### 📥 Import/Export et Intégration (Catégorie 11)

#### Import de Catalogue CSV
- **Assistant d'import** avec interface intuitive
- **3 modes d'import** :
  - Créer de nouveaux livres uniquement
  - Mettre à jour les livres existants (par ISBN)
  - Créer et mettre à jour (mode mixte)
- **Téléchargement de template** CSV avec exemples
- **Création automatique** :
  - Auteurs manquants créés automatiquement
  - Catégories manquantes créées automatiquement
- **Format CSV simple** :
  ```csv
  isbn,title,author,category,publisher,pages
  9782070360024,L'Étranger,Albert Camus,Fiction,Gallimard,186
  ```
- **Rapport d'import détaillé** :
  - Nombre de livres créés
  - Nombre de livres mis à jour
  - Liste des erreurs éventuelles

### 🎨 Améliorations Visuelles

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

## Structure du Module## ⚡ Démarrage Rapide

```bash
# 1. Cloner/télécharger le projet
cd C:\Users\X1\Documents\edu_gourou

# 2. Démarrer Docker
docker-compose up -d

# 3. Accéder à Odoo
# Navigateur → http://localhost:8069

# 4. Installer le module
# Apps → Rechercher "Gestion de Bibliothèque" → Installer
```

---
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
   └KPIs clés** :
  - Livres : Total, Disponibles, Empruntés, Taux d'occupation
  - Emprunts : Total, Actifs, En retard, Taux de retard
  - Adhérents : Total, Actifs, Expirés, Suspendus
- **Accès rapides** :
  - 📗 Voir Livres Disponibles
  - 📋 Emprunts en Cours
  - ⚠️ Emprunts en Retard
  - 👥 Adhérents Actifs
- **Vues analytiques** :
  - 📊 Graphique emprunts par mois
  - 🥧 Graphique livres par catégorie
  - 📈 Tableau croisé dynamique

#### 📚 Livres
- **Tous les livres** : Vue complète (Kanban/Liste/Formulaire)
- **Livres disponibles** : Livres prêts à être empruntés (vue filtrée)
- **Livres empruntés** : Livres actuellement en prêt (vue filtrée)

**Actions disponibles** :
- Créer un nouveau livre
- 📥 **Importer des livres** (CSV)
- Modifier les informations
- Changer l'état (disponible, maintenance, perdu)
- Voir l'historique des emprunts
- Archiver/Désarchiver

#### 👥 Adhérents
- **Tous les adhérents** : Liste complète avec photos
- **Adhérents actifs** : Adhésions valides uniquement
- **Adhérents expirés** : À renouveler

**Fonctionnalités** :
- Fiche complète avec statistiques
- SmaInscrire un nouvel adhérent
1. Bibliothèque → Adhérents → Tous les adhérents
2. Cliquer sur "Créer"
3. Remplir : Nom, Type, Email, Téléphone
4. Ajouter une photo
5. Sauvegarder → Numéro de carte généré automatiquement (ADH00001)

#### Ajouter un nouveau livre
1. Bibliothèque → Livres → Tous les livres
2. Cliquer sur "Créer"
3. Remplir : Titre, ISBN, Auteur, Catégorie, etc.
4. Ajouter une image de couverture
5. Sauvegarder

#### Importer des livres en masse
1. Bibliothèque → Import/Export → Importer des livres
2. Télécharger le template CSV
3. Remplir le fichier avec vos livres
4. Uploader le fichier
5. Sélectionner le mode (Créer/Mettre à jour)
6. Lancer l'import → Rapport détaillé affiché

#### Créer un emprunt
1. Bibliothèque → Emprunts → Tous les emprunts
2. Cliquer sur "Créer"
3. Sélectionner le livre (doit être disponible)
4. Sélectionner l'adhérent → Auto-remplissage des infos
5. La date de retour est calculée automatiquement (14 jours)
6. Cliquer sur "Confirmer l'emprunt"

#### Retourner un livre
1. Bibliothèque → Emprunts → Emprunts en cours
2. Ouvrir l'emprunt concerné
3. Cliquer sur "Retourner le livre"
4. Le livre redevient automatiquement disponible
5. Si en retard → Pénalité créée automatiquement

#### Gérer une pénalité
1. Bibliothèque → Finances → Pénalités impayées
2. Ouvrir la pénalité
3. Cliquer sur "Confirmer" (si brouillon)
4. Cliquer sur "Enregistrer un paiement"
5. Saisir le montant et la méthode
6. Confirmer → État change en "Payée" si complet

#### Renouveler une adhésion
1. Bibliothèque → Adhérents → Adhérents expirés
2. Ouvrir la fiche adhérent
3. Aller dans l'onglet "Frais d'adhésion"
4. Créer un nouveau frais (montant calculé selon le type)
5. Confirmer le paiement
6. L'adhérent devient automatiquement "Actif" avec nouvelle date d'expiration

#### Configurer les notifications
1. Bibliothèque → Notifications → Paramètres
2. Choisir la méthode (Email / Odoo / Les deux)
3. Configurer les délais :
   - Rappel amember (Adhérent)
- **Champs** : name, member_number, member_type, email, phone, address, photo, registration_date, expiration_date, state
- **Héritage** : mail.thread, mail.activity.mixin
- **Relations** : One2many vers Borrowing, Penalty, MembershipFee
- **Champs calculés** : state (actif/expiré/suspendu), total_borrowings, current_borrowings, late_borrowings, total_penalties, unpaid_penalties
- **Séquence** : ADH00001, ADH00002...

#### library.borrowing (Emprunt)
- **Champs** : name, book_id, member_id, borrower_name, borrower_email, borrowing_date, expected_return_date, actual_return_date, state, last_reminder_date, reminder_count
- **Héritage** : mail.thread, mail.activity.mixin
- **Relations** : Many2one vers Book et Member
- **Champs calculés** : days_borrowed, is_late, late_days
- **Séquence** : EMP00001, EMP00002...
- **Méthodes** : _send_notification(), _get_notification_message()

#### library.penalty (Pénalité)
- **Champs** : name, borrowing_id, member_id, late_days, daily_rate, penalty_amount, payment_amount, remaining_amount, state
- **Héritage** : mail.thread, mail.activity.mixin
- **Relations** : Many2one vers Borrowing et Member
- **Champs calculés** : penalty_amount, remaining_amount
- **Séquence** : PEN00001, PEN00002...

#### library.membership.fee (Frais d'adhésion)
- **Champs** : name, member_id, fee_amount, payment_date, validity_start, validity_end, state, payment_method
- **Héritage** : mail.thread, mail.activity.mixin
- **Relations** : Many2one vers Member
- **Champs calculés** : validity_end (1 an après validity_start)
- **Séquence** : FEE00001, FEE00002...

#### library.notification.settings (Paramètres notifications)
- **Champs** : name, enable_due_soon_notification, due_soon_days, enable_overdue_notification, overdue_frequency_days, enable_membership_expiring, membership_expiring_days, notification_method
- **Singleton** : Un seul enregistrement actif

#### library.notification.log (Journal notifications)
- **Champs** : name, notification_type, recipient_id, recipient_email, borrowing_id, book_id, sent_date, status, method, error_message
- **Séquence** : NOT00001, NOT00002...

#### library.dashboard (Tableau de bord)
- **Champs calculés** : Tous les champs (statistiques en temps réel)
- **Pas de stockage** : Calculs à la volée
- **Frais d'adhésion** : Historique des paiements

**Actions financières** :
- Confirmer une pénalité
- Enregistrer un paiement (wizard)
- Confirmer un paiement d'adhésion
- Annuler une transaction

#### 📊 Rapports
- **Tableau de bord** : Vue d'ensemble
- **Emprunts par mois** : Graphique temporel
- **Analyse des livres** : Statistiques par catégorie

#### 🔔 Notifications
- **Paramètres** : Configuration du système
- **Journal** : Historique des notifications
- **Échecs** : Notifications en erreur

**Configuration** :
- Méthode : Email / Odoo / Les deux
- Rappel échéance : X jours avant (défaut: 2)
- Fréquence retard : Tous les X jours (défaut: 3)
- Adhésion expire : X jours avant (défaut: 7)

#### 📥 Import/Export
- **Importer des livres** : Assistant CSV
  - Télécharger le template
  - Uploader le fichier
  - Créer/Mettre à jour les livresble, maintenance, perdu)
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
6 catégories implémentées** :
   - ✅ Catégorie 1 : Gestion des Membres/Adhérents
   - ✅ Catégorie 3 : Gestion Financière Simple
   - ✅ Catégorie 5 : Rapports et Tableaux de Bord
   - ✅ Catégorie 6 : Notifications et Alertes
   - ✅ Catégorie 11 : Import/Export et Intégration
   - ✅ Fonctionnalités de base complètes
✅ **Système de notifications** automatique avec emails  
✅ **Import/Export CSV** pour catalogue  
✅ **Gestion financière** (pénalités + adhésions)  
✅ **Tableau de bord analytique** avec graphiques  
✅ **Données de démonstration** pour présentation  
✅ **Documentation complète** (README détaillé)  

### Fonctionnalités Implémentées

#### ✅ Complètement Opérationnelles
- 📚 Gestion des livres (CRUD, états, historique)
- ✍️ Gestion des auteurs et catégories
- 👥 Gestion complète des adhérents
- 📖 Gestion des emprunts avec workflow
- 💰 Pénalités de retard avec paiements
- 💳 Frais d'adhésion avec renouvellement
- 🔔 Notifications automatiques (email + Odoo)
- 📥 Import CSV de catalogue
- 📊 Tableau de bord avec KPIs
- 📈 Rapports et analyses (graphiques, pivot)
- ⏰ 3 Cron jobs pour automatisation

### Évolutions Possibles (Non implémentées)
- 📱 Application mobile
- 🔒 Gestion avancée des droits par rôle
- 📍 Localisation physique des livres (étagères, rayons)
- 🔄 Système de réservations de livres
- 📚 Gestion de plusieurs exemplaires par titre
- 📤 Export vers systèmes externes (MARC, bibliothèques numériques)
- 📊 Rapports avancés (utilisation par adhérent, popularité livres)
- 💬 Système de notation et commentaires de livres
- 🔍 Recherche avancée full-text
- 📆 Calendrier des événements (clubs de lecture, etc.)y, biography
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
- 📖 Consultez cette documentation complète
- 🔍 Vérifiez les logs Odoo : `docker-compose logs -f web`
- 🛠️ Mode debug Odoo : Paramètres → Activer le mode développeur
- 📧 Vérifiez le journal des notifications pour problèmes d'emails

### Problèmes Courants

#### Le module n'apparaît pas
```bash
# 1. Redémarrer Docker
docker-compose restart

# 2. Dans Odoo : Apps → Mettre à jour la liste des applications
```

#### Erreur lors de l'installation
1. Vérifiez les logs : `docker-compose logs web`
2. Vérifiez les droits d'accès dans `security/ir.model.access.csv`
3. Validez la syntaxe des fichiers XML
4. Assurez-vous que les dépendances (`base`, `mail`) sont installées

#### Les notifications ne fonctionnent pas
1. Vérifier les paramètres : **Notifications → Paramètres**
2. Vérifier la configuration email d'Odoo
3. Consulter : **Notifications → Échecs** pour voir les erreurs
4. Vérifier que les cron jobs sont actifs : **Paramètres → Tâches planifiées**

#### Import CSV échoue
1. Vérifier le format du fichier (UTF-8, virgules)
2. Télécharger et utiliser le template fourni
3. S'assurer que les colonnes sont correctes : `isbn,title,author,category,publisher,pages`
4. Vérifier les messages d'erreur dans le rapport d'import

#### Les pénalités ne se créent pas
1. Vérifier que le cron job "Vérifier retards" est actif
2. Forcer l'exécution : **Paramètres → Tâches planifiées → Bibliothèque: Vérifier retards → Exécuter**
3. Vérifier dans les logs s'il y a des erreurs

### Commandes Docker Utiles

```bash
# Voir les logs en temps réel
docker-compose logs -f web

# Redémarrer uniquement Odoo
docker-compose restart web

# Arrêter tous les services
docker-compose down

# Arrêter et supprimer les volumes (⚠️ Perte de données)
docker-compose down -v

# Reconstruire les conteneurs
docker-compose up -d --build
```

### Mode Développeur Odoo

Activer le mode développeur pour accéder aux fonctionnalités avancées :
1. **Paramètres → Activer le mode développeur**
2. Ou ajouter `?debug=1` à l'URL : `http://localhost:8069/web?debug=1`

**Fonctionnalités debug utiles** :
- Voir les noms techniques des champs
- Éditer les vues directement
- Voir les IDs des enregistrements
- Consulter les métadonnées des modèles

---

## 📝 Notes de Développement

### Conventions de Code
- **Langue** : Français pour les labels et la documentation
- **Style Python** : PEP 8
- **Nommage modèles** : `library_*` (ex: `library.book`)
- **Nommage fichiers** : snake_case
- **Séquences** : Préfixes en majuscules (EMP, ADH, PEN, FEE, NOT)

### Architecture
- **MVC** : Séparation modèles/vues/contrôleurs
- **ORM Odoo** : Utilisation des décorateurs `@api.depends`, `@api.onchange`
- **Héritage** : `mail.thread` et `mail.activity.mixin` pour traçabilité
- **Champs calculés** : `compute=`, `store=True` pour performance
- **Contraintes SQL** : Pour intégrité des données

### Tests Recommandés
1. ✅ Créer un adhérent et vérifier la génération du numéro
2. ✅ Créer un emprunt et confirmer le changement d'état du livre
3. ✅ Simuler un retard et vérifier la création de pénalité
4. ✅ Tester les notifications (modifier les dates pour forcer l'envoi)
5. ✅ Importer un fichier CSV et vérifier la création des livres
6. ✅ Tester les paiements de pénalités (complet et partiel)
7. ✅ Vérifier les statistiques du tableau de bord

---

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
