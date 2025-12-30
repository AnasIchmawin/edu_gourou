# Rapport de Projet : Module de Gestion de Bibliothèque sous Odoo 17

---

## 1. Introduction

Le présent rapport s’inscrit dans le cadre du module __Gestion des Processus Métier et ERP__ et vise à présenter le travail de conception et de développement d’un module métier sous la plateforme **Odoo 17**. Ce projet a pour objectif de consolider la compréhension pratique des systèmes ERP et de mettre en évidence leur rôle central dans la digitalisation et l’optimisation des processus organisationnels.

Le domaine métier retenu concerne la gestion des livres. Initialement orienté vers une approche commerciale classique (achat, vente et gestion de stock), le périmètre du projet a évolué afin de mieux correspondre à un contexte d’usage réel, en l’occurrence la gestion d’une bibliothèque. Ce choix permet de modéliser et d’implémenter des processus métiers variés et complémentaires, tels que la gestion des ouvrages, des adhérents, des emprunts et retours, ainsi que certains aspects financiers et de notification.

Le module développé, intitulé « Gestion de Bibliothèque », constitue une solution fonctionnelle et opérationnelle intégrée à Odoo. Il illustre de manière concrète l’application des concepts théoriques abordés au cours, tout en mettant en pratique les mécanismes fondamentaux de développement de modules ERP.

---

## 2. Contexte pédagogique et objectifs du module

Ce projet s'inscrit dans le cadre d'un enseignement de cycle ingénieur visant à former les étudiants aux systèmes d'information d'entreprise et aux ERP. Les objectifs pédagogiques poursuivis sont les suivants :

- Comprendre l'architecture modulaire d'un ERP et les principes de conception d'applications métier.
- Maîtriser le framework Odoo : modèles de données (ORM), vues XML, workflows, et droits d'accès.
- Modéliser des processus métier et les implémenter sous forme de modules fonctionnels.
- Développer des compétences en programmation Python orientée objet appliquée aux ERP.
- Appréhender les aspects d'intégration de données, de reporting et de notifications automatiques.

Le projet permet ainsi de mettre en œuvre de manière concrète les connaissances théoriques relatives à la gestion des processus, à la modélisation relationnelle, et à l'utilisation d'outils professionnels tels qu'Odoo et Docker.

---

## 3. Présentation du domaine métier : gestion des livres

Le domaine choisi porte sur la gestion des livres, un secteur qui peut être abordé selon deux axes principaux :

1. **Axe commercial** : processus d'achat, de vente et de gestion de stock, typique d'une librairie ou d'un distributeur.
2. **Axe documentaire** : gestion d'une bibliothèque avec prêt, retour, gestion des adhérents et pénalités de retard.

Le projet a finalement adopté le second axe, jugé plus riche sur le plan métier et plus adapté à un contexte académique. Une bibliothèque implique en effet des processus variés :

- Catalogage des ouvrages avec métadonnées complètes (ISBN, auteur, catégorie, éditeur).
- Gestion des adhérents avec suivi des adhésions et des états (actif, expiré, suspendu).
- Workflow d'emprunt et de retour avec calcul automatique des dates et détection des retards.
- Gestion financière simplifiée (pénalités de retard, frais d'adhésion).
- Système de notifications automatiques par email ou via l'interface Odoo.
- Fonctionnalités de reporting et tableaux de bord analytiques.

Ce périmètre permet de couvrir des concepts clés des ERP : gestion de workflows, intégration de modules, automatisation, et suivi analytique.

---

## 4. Analyse des processus métier

Le module implémenté couvre plusieurs processus métier structurés autour de trois axes principaux.

### 4.1. Processus de gestion des emprunts et retours

Le processus central du module concerne le prêt et le retour d'ouvrages. Il se décompose en plusieurs étapes :

**Workflow d'emprunt**
1. Vérification de la disponibilité de l'ouvrage.
2. Vérification du statut de l'adhérent (actif, non suspendu, pas de retards en cours).
3. Création d'un enregistrement d'emprunt avec numérotation automatique (EMP00001, EMP00002, etc.).
4. Calcul automatique de la date de retour prévue (14 jours par défaut).
5. Changement automatique de l'état de l'ouvrage en "Emprunté".

**Workflow de retour**
1. Enregistrement de la date de retour effective.
2. Mise à jour de l'état de l'ouvrage en "Disponible".
3. Calcul des jours de retard éventuels.
4. Génération automatique d'une pénalité si retard constaté.

**Gestion des retards**
- Un cron job quotidien détecte automatiquement les emprunts en retard.
- Le statut de l'emprunt passe à "En retard".
- Des notifications de rappel sont envoyées selon une fréquence configurable.

### 4.2. Processus de gestion des adhérents

La gestion des adhérents constitue le deuxième processus clé.

**Inscription**
- Création d'une fiche adhérent avec attribution d'un numéro unique (ADH00001, ADH00002, etc.).
- Enregistrement des informations personnelles (nom, email, téléphone, adresse, photo).
- Sélection du type d'adhérent (Étudiant, Enseignant, Personnel, Externe).
- Calcul automatique de la date d'expiration de l'adhésion (1 an).

**Suivi du statut**
- Actif : adhésion valide et aucune suspension.
- Expiré : adhésion dépassée.
- Suspendu : compte bloqué (retards répétés, pénalités impayées, etc.).

**Renouvellement**
- Enregistrement d'un nouveau frais d'adhésion.
- Mise à jour automatique de la date d'expiration.
- Passage du statut à "Actif".

### 4.3. Processus de gestion financière

Le module intègre une gestion financière simplifiée mais fonctionnelle.

**Pénalités de retard**
- Calcul automatique : nombre de jours de retard × tarif journalier.
- Workflow : Brouillon → Confirmée → Payée.
- Possibilité de paiements partiels avec suivi du montant restant.
- Assistant de paiement (wizard) avec sélection du moyen de paiement (Espèces, Carte, Chèque, Virement).

**Frais d'adhésion**
- Tarification différenciée selon le type d'adhérent.
- Enregistrement du paiement avec méthode et date.
- Mise à jour automatique de la validité de l'adhésion.

### 4.4. Processus de notification automatique

Un système de notifications automatiques assure le suivi proactif des échéances.

**Types de notifications**
- Rappel d'échéance proche : envoyé X jours avant la date de retour prévue.
- Alerte de retard : envoyée périodiquement pour les emprunts en retard.
- Expiration d'adhésion : notification préventive avant l'expiration.

**Mécanisme technique**
- Configuration centralisée des paramètres (délais, fréquence, méthodes).
- Trois cron jobs quotidiens pour vérifier les échéances, retards et expirations.
- Journal complet des notifications avec suivi des succès et échecs.

---

## 5. Présentation de la solution ERP Odoo

### 5.1. Justification du choix d'Odoo

Odoo est un ERP open source modulaire, largement utilisé en entreprise et particulièrement adapté à un contexte pédagogique pour les raisons suivantes :

- **Architecture modulaire** : chaque module est autonome tout en s'intégrant avec les autres.
- **Framework complet** : ORM robuste, moteur de vues XML, gestion des workflows et des droits.
- **Communauté active** : documentation riche, forums, modules contributifs.
- **Déploiement simplifié** : compatibilité Docker, facilitant l'installation et la portabilité.
- **Gratuité** : version Community accessible sans contrainte de licence.

### 5.2. Avantages pour le projet

Dans le cadre de ce projet, Odoo offre plusieurs bénéfices concrets :

- Gain de temps sur l'infrastructure technique (base de données, interface web, authentification).
- Héritage de fonctionnalités standards (messagerie, activités, logs de modifications).
- Capacité à développer des modules métier complexes avec un code relativement concis.
- Expérience réelle d'un outil professionnel utilisé en entreprise.

---

## 6. Conception et développement du module Odoo

### 6.1. Modélisation des données

Le module repose sur onze modèles de données interconnectés, respectant les bonnes pratiques de modélisation relationnelle.

**Modèles principaux**

| Modèle | Description | Relations clés |
|--------|-------------|----------------|
| `library.book` | Ouvrage (ISBN, titre, auteur, catégorie, état) | Many2one vers Author et Category |
| `library.author` | Auteur (nom, biographie, photo, nationalité) | One2many vers Book |
| `library.category` | Catégorie (hiérarchique, avec parent/enfants) | One2many vers Book |
| `library.member` | Adhérent (numéro, type, email, dates, statut) | One2many vers Borrowing, Penalty, MembershipFee |
| `library.borrowing` | Emprunt (livre, adhérent, dates, état) | Many2one vers Book et Member |
| `library.penalty` | Pénalité (montant, paiements, état) | Many2one vers Borrowing et Member |
| `library.membership.fee` | Frais d'adhésion (montant, dates, méthode) | Many2one vers Member |
| `library.reservation` | Réservation (livre, adhérent, file d'attente) | Many2one vers Book et Member |
| `library.notification.settings` | Paramètres des notifications (singleton) | - |
| `library.notification.log` | Journal des notifications | Many2one vers Member et Borrowing |
| `library.dashboard` | Tableau de bord (champs calculés) | - |

**Contraintes d'intégrité**
- ISBN unique pour chaque livre.
- Nom de catégorie unique.
- Numérotation séquentielle automatique pour emprunts, adhérents, pénalités, etc.

**Champs calculés**
- Nombre de livres par auteur et par catégorie.
- Jours d'emprunt, jours de retard, montant restant d'une pénalité.
- Statut d'adhérent (actif/expiré/suspendu) calculé dynamiquement.
- Statistiques du tableau de bord calculées en temps réel.

### 6.2. Fonctionnalités développées

Le module couvre un large éventail de fonctionnalités opérationnelles.

**Gestion du catalogue**
- CRUD complet sur les livres, auteurs et catégories.
- Affichage d'images de couverture avec vue Kanban optimisée.
- États des livres avec codes couleurs (Disponible, Emprunté, Réservé, En maintenance, Perdu).
- Historique des emprunts par livre.
- Import CSV en masse avec assistant dédié (trois modes : créer, mettre à jour, mixte).

**Gestion des adhérents**
- Fiches complètes avec photo, type, coordonnées.
- Génération automatique de numéros de carte (ADH00001, etc.).
- Calcul dynamique du statut (actif, expiré, suspendu).
- Smart buttons pour accès rapide aux emprunts et pénalités.
- Actions : renouveler, suspendre, activer.

**Gestion des emprunts**
- Workflow : Brouillon → Emprunté → Retourné / En retard.
- Calcul automatique de la date de retour (14 jours).
- Détection automatique des retards par cron job.
- Boutons d'action : confirmer, retourner, marquer perdu, annuler.

**Système de réservations**
- Réservation de livres empruntés avec file d'attente.
- Limite de trois réservations par adhérent.
- États : En attente, Disponible, Récupéré, Expiré, Annulé.
- Notification automatique lors de la disponibilité du livre.
- Expiration automatique si non récupéré dans les 3 jours.

**Gestion financière**
- Pénalités calculées automatiquement (jours de retard × tarif).
- Workflow : Brouillon → Confirmée → Payée.
- Assistant de paiement avec paiements partiels.
- Frais d'adhésion différenciés par type (Étudiant : 10€, Enseignant : 20€, etc.).
- Historique complet des transactions.

**Notifications automatiques**
- Rappels d'échéance, alertes de retard, expiration d'adhésion.
- Configuration centralisée (méthodes, délais, fréquences).
- Templates d'emails professionnels.
- Journal exhaustif avec suivi des échecs.
- Trois cron jobs pour vérifications quotidiennes.

**Reporting et tableaux de bord**
- Tableau de bord avec KPIs en temps réel (livres, emprunts, adhérents).
- Graphiques en barres (emprunts par mois).
- Graphiques en camembert (livres par catégorie, par état).
- Tableaux croisés dynamiques (Pivot).
- Boutons d'accès rapide aux vues filtrées.

### 6.3. Workflow métier implémenté

Le workflow général du module peut être synthétisé ainsi :

```
1. Catalogage des livres (manuel ou import CSV)
2. Inscription des adhérents
3. Paiement des frais d'adhésion
4. Création d'un emprunt (si livre disponible et adhérent actif)
5. Confirmation de l'emprunt (changement d'état du livre)
6. Notifications automatiques de rappel
7. Retour du livre (mise à jour des états)
8. Génération automatique de pénalité si retard
9. Paiement de la pénalité
10. Renouvellement de l'adhésion si expiré
```

Ce workflow illustre la cohérence fonctionnelle du module et l'enchaînement logique des processus métier.

### 6.4. Installation et démarrage du module

#### 6.4.1. Prérequis techniques

L'installation du module nécessite les éléments suivants :

- Docker et Docker Compose installés et fonctionnels
- Ports 8069 (Odoo) et 5432 (PostgreSQL) disponibles sur la machine hôte
- Système d'exploitation compatible (Windows, Linux, macOS)

#### 6.4.2. Structure du projet

Le projet doit être organisé selon la structure suivante :

```
edu_gourou/
├── docker-compose.yml
└── library_management/          # Module Odoo
    ├── __init__.py
    ├── __manifest__.py
    ├── models/
    ├── views/
    ├── wizards/
    ├── security/
    ├── data/
    └── static/
```

#### 6.4.3. Procédure de démarrage

**Étape 1 : Cloner ou placer le projet**

```bash
cd C:\Users\X1\Documents\edu_gourou
```

**Étape 2 : Démarrer les conteneurs Docker**

```bash
docker-compose up -d
```

Cette commande lance deux conteneurs :
- Un conteneur Odoo (version 17.0) exposé sur le port 8069
- Un conteneur PostgreSQL (version 15) pour la base de données

**Étape 3 : Vérifier le démarrage des services**

```bash
docker-compose ps
```

Les deux services doivent être à l'état "Up".

**Étape 4 : Accéder à l'interface Odoo**

Ouvrir un navigateur et accéder à : `http://localhost:8069`

Lors de la première connexion, Odoo demande la création d'une base de données.

**Étape 5 : Activer le mode développeur**

Une fois connecté à Odoo :
1. Aller dans Paramètres → Général
2. Activer le mode développeur

**Étape 6 : Installer le module**

1. Aller dans le menu Applications
2. Cliquer sur "Mettre à jour la liste des applications"
3. Rechercher "Gestion de Bibliothèque"
4. Cliquer sur "Installer"

L'installation prend quelques secondes et crée automatiquement :
- Les tables de base de données pour tous les modèles
- Les vues et menus
- Les données de démonstration (catégories, auteurs, livres)
- Les cron jobs de notification
- Les séquences de numérotation

### 6.4.4. Commandes Docker utiles

**Consulter les logs en temps réel**

```bash
docker-compose logs -f web
```

**Redémarrer uniquement le service Odoo**

```bash
docker-compose restart web
```

**Arrêter tous les services**

```bash
docker-compose down
```

**Arrêter et supprimer les volumes (attention : perte de données)**

```bash
docker-compose down -v
```

**Reconstruire les conteneurs après modification**

```bash
docker-compose up -d --build
```

#### 6.4.5. Vérification de l'installation

Après installation, vérifier que :
- Le menu "Bibliothèque" apparaît dans la barre de navigation principale
- Le tableau de bord s'affiche avec les statistiques
- Les données de démonstration sont présentes (3 livres, 3 auteurs, 7 catégories)
- Les cron jobs sont actifs dans Paramètres → Technique → Tâches planifiées

En cas de problème, consulter les logs Docker pour identifier l'origine de l'erreur.

---

## 7. Résultats et illustration de l'application

Cette section présente les principales interfaces développées, illustrant les fonctionnalités opérationnelles du module.

### 7.1. Tableau de bord et reporting

Le tableau de bord constitue le point d'entrée principal du module, offrant une vue d'ensemble en temps réel.

Figure : Tableau de bord principal avec statistiques et accès rapides  
![Tableau de bord principal](images/dashboard.png)

Le tableau affiche les indicateurs clés de performance (livres disponibles, emprunts actifs, adhérents) ainsi que des boutons d'accès rapide vers les vues filtrées.

Figure : Graphique d'analyse des emprunts par mois  
![Graphique des emprunts par mois](images/graph_emprunts.png)

Ce graphique permet de suivre l'évolution temporelle de l'activité de prêt.

### 7.2. Gestion du catalogue de livres

La vue Kanban des livres offre une interface visuelle et intuitive pour parcourir le catalogue.

Figure : Vue Kanban des livres avec images et codes couleurs  
![Vue Kanban des livres](images/livres_kanban.png)

Chaque carte affiche l'image de couverture, le titre, l'auteur, la catégorie et l'état du livre, avec des bordures colorées selon le statut.

Figure : Formulaire détaillé d'un livre  
![Formulaire de livre](images/livre_form.png)

Le formulaire permet de saisir l'ensemble des métadonnées et d'accéder à l'historique des emprunts via un onglet dédié.

### 7.3. Gestion des adhérents

La fiche adhérent centralise toutes les informations et statistiques liées au membre.

Figure : Fiche complète d'un adhérent avec smart buttons  
![Fiche adhérent](images/adherent_form.png)

Les smart buttons offrent un accès rapide aux emprunts en cours, aux pénalités et à l'historique des frais d'adhésion.

### 7.4. Gestion des emprunts

La vue des emprunts permet de suivre l'état de chaque prêt et de gérer les retours.

Figure : Liste des emprunts avec code couleur selon l'état  
![Liste des emprunts](images/emprunts_liste.png)

Les emprunts en retard sont affichés en rouge, facilitant leur identification.

Figure : Formulaire d'emprunt avec workflow  
![Formulaire d'emprunt](images/emprunt_form.png)

Le formulaire inclut une barre d'état (statusbar) et des boutons d'action contextuels.

### 7.5. Système de réservations

Le module permet aux adhérents de réserver des livres empruntés.

Figure : Vue des réservations avec file d'attente  
![Vue des réservations](images/reservations_liste.png)

La position dans la file d'attente est indiquée, et le statut évolue automatiquement lors du retour du livre.

### 7.6. Gestion financière

Le module gère les pénalités de retard et les frais d'adhésion de manière structurée.

Figure : Liste des pénalités avec montants et états  
![Liste des pénalités](images/penalites_liste.png)

Figure : Assistant de paiement d'une pénalité  
![Assistant de paiement](images/paiement_wizard.png)

L'assistant permet d'enregistrer des paiements partiels ou complets, avec sélection du moyen de paiement.

### 7.7. Notifications automatiques

Le journal des notifications offre une traçabilité complète des envois.

Figure : Journal des notifications avec suivi des succès et échecs  
![Journal des notifications](images/notifications_log.png)

Figure : Paramètres de configuration des notifications  
![Paramètres des notifications](images/notifications_settings.png)

Les paramètres permettent de configurer les délais, fréquences et méthodes d'envoi (email, Odoo, ou les deux).

### 7.8. Import de catalogue CSV

Un assistant dédié facilite l'import en masse de livres.

Figure : Assistant d'import CSV avec téléchargement de template  
![Assistant d'import CSV](images/import_csv_wizard.png)

L'import crée automatiquement les auteurs et catégories manquants et génère un rapport détaillé.

---

## 8. Limites du projet et perspectives d'amélioration

### 8.1. Limites identifiées

Plusieurs aspects du module pourraient être améliorés ou complétés :

**Limites fonctionnelles**
- Absence de gestion multi-exemplaires : un seul exemplaire par titre.
- Pas de localisation physique des ouvrages (étagère, rayon).
- Absence de système de notation ou de commentaires par les adhérents.
- Pas de recherche full-text avancée.

**Limites techniques**
- Gestion des droits d'accès non différenciée par rôle (bibliothécaire, adhérent, administrateur).
- Absence d'application mobile native.
- Export limité aux formats standards Odoo (pas d'export MARC pour interopérabilité bibliothécaire).
- Pas d'intégration avec des systèmes externes (systèmes de paiement en ligne, catalogues partagés).

**Limites ergonomiques**
- Interface optimisée pour desktop, moins adaptée aux tablettes et smartphones.
- Certaines vues nécessitent plusieurs clics pour des actions courantes.

### 8.2. Perspectives d'amélioration

**Évolutions fonctionnelles**
- Gestion de plusieurs exemplaires par titre avec suivi individuel.
- Système de recommandations basé sur l'historique d'emprunts.
- Calendrier d'événements (clubs de lecture, rencontres d'auteurs).
- Gestion des documents numériques (e-books, PDF).

**Évolutions techniques**
- Développement d'une API REST pour intégration externe.
- Application mobile (iOS/Android) pour consultation du catalogue et gestion des emprunts.
- Intégration de systèmes de paiement en ligne pour les pénalités et adhésions.
- Export au format MARC pour compatibilité avec d'autres systèmes de gestion bibliothécaire.

**Évolutions analytiques**
- Rapports avancés : popularité des ouvrages, taux d'occupation, profil des lecteurs.
- Tableaux de bord personnalisés par rôle.
- Indicateurs de performance (KPI) pour pilotage stratégique.

---

## 9. Conclusion

Le projet de développement d'un module de gestion de bibliothèque sous **Odoo 17** a permis d'atteindre les objectifs pédagogiques fixés, tout en produisant une solution fonctionnelle et complète.

### 9.1. Bilan du travail réalisé

Le module développé couvre l'ensemble du périmètre fonctionnel d'une bibliothèque moderne :

- Gestion complète du catalogue (livres, auteurs, catégories).
- Workflow d'emprunt et de retour avec gestion des retards.
- Gestion des adhérents avec suivi des adhésions.
- Système de réservations avec file d'attente automatique.
- Gestion financière (pénalités et frais d'adhésion).
- Notifications automatiques par email et via l'interface Odoo.
- Tableau de bord analytique avec graphiques et KPIs.
- Import CSV pour alimentation rapide du catalogue.

L'architecture du module respecte les standards Odoo, avec une séparation claire entre modèles, vues, wizards, et données. Le code est documenté, structuré, et utilise les mécanismes avancés du framework (champs calculés, workflows, cron jobs, héritage de modèles).

### 9.2. Compétences acquises

Ce projet a permis de développer un ensemble de compétences techniques et méthodologiques :

**Compétences ERP et Odoo**
- Maîtrise de l'architecture modulaire d'Odoo.
- Développement de modèles de données avec l'ORM Odoo.
- Conception de vues XML (formulaires, listes, Kanban, graphiques, pivot).
- Implémentation de workflows métier avec gestion d'états.
- Gestion des droits d'accès et sécurité.
- Utilisation des mécanismes avancés (champs calculés, contraintes, wizards, cron jobs).

**Compétences en modélisation et conception**
- Analyse des processus métier et traduction en spécifications fonctionnelles.
- Modélisation relationnelle avec contraintes d'intégrité.
- Conception de workflows et gestion des états.
- Définition d'indicateurs de performance et reporting.

**Compétences techniques**
- Programmation Python orientée objet.
- Développement avec le framework Odoo (API, décorateurs, héritage).
- Intégration de données (import CSV).
- Gestion de base de données PostgreSQL.
- Déploiement avec Docker et Docker Compose.
- Versionnement de code et documentation.

**Compétences transversales**
- Gestion de projet informatique.
- Documentation technique et rédaction de rapports.
- Démarche qualité et tests fonctionnels.

### 9.3. Ouverture

Ce projet constitue une base solide pour des développements futurs. Les perspectives d'évolution identifiées (gestion multi-exemplaires, application mobile, intégration externe) pourraient faire l'objet de projets ultérieurs, illustrant ainsi la démarche d'amélioration continue caractéristique des systèmes ERP en environnement professionnel.

L'expérience acquise sur Odoo est directement transposable en entreprise, Odoo étant largement utilisé dans divers secteurs (commerce, industrie, services). La compréhension des mécanismes de modélisation, de workflow et d'intégration est applicable à d'autres ERP (SAP, Microsoft Dynamics, etc.) ou plus largement à tout système d'information d'entreprise.

En définitive, ce projet a permis de passer de la théorie à la pratique, en produisant une solution concrète, fonctionnelle et professionnelle, démontrant ainsi la maîtrise des concepts enseignés dans le module Gestion des Processus Métier et ERP.

---

**Fin du rapport**