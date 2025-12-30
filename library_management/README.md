# **Rapport de Projet : Module de Gestion de Bibliothèque sous Odoo 17**
## 9. Conclusion

Le développement de ce module de gestion de bibliothèque sous **Odoo 17** a permis d’atteindre tous les objectifs fixés, tout en créant une solution complète et facile à utiliser.

### 9.1. Bilan du travail

Le module couvre tout ce qu’on attend d’une bibliothèque moderne :

- Gestion du catalogue (livres, auteurs, catégories)
- Workflow d’emprunt et de retour avec gestion des retards
- Gestion des membres et de leurs adhésions
- Système de réservations avec file d’attente
- Gestion financière (pénalités, frais d’adhésion)
- Notifications automatiques (email et Odoo)
- Tableau de bord avec graphiques et indicateurs
- Import rapide du catalogue par CSV

L’architecture respecte les standards Odoo, avec une séparation claire entre modèles, vues, assistants et données. Le code est bien structuré, documenté, et utilise les fonctions avancées du framework (champs calculés, workflows, tâches automatiques, héritage de modèles).


### 9.2. Compétences acquises

Ce projet, réalisé en groupe de trois personnes, nous a permis de développer de nombreuses compétences :

**Sur Odoo et les ERP :**
- Comprendre l’architecture modulaire d’Odoo
- Créer des modèles de données avec l’ORM
- Concevoir des vues (formulaires, listes, Kanban, graphiques…)
- Mettre en place des workflows métier
- Gérer la sécurité et les droits d’accès
- Utiliser les fonctions avancées (champs calculés, assistants, tâches automatiques)

**En modélisation et conception :**
- Analyser les besoins métier et les transformer en spécifications
- Modéliser les données et les relations
- Concevoir des workflows et des indicateurs de performance

**Techniquement :**
- Programmer en Python orienté objet
- Utiliser le framework Odoo (API, décorateurs, héritage)
- Gérer l’import de données (CSV)
- Administrer une base PostgreSQL
- Déployer avec Docker et Docker Compose
- Versionner le code et documenter

**Transversalement :**
- Gérer un projet informatique en équipe
- Rédiger une documentation claire
- Adopter une démarche qualité et tester les fonctionnalités

### 9.3. Ouverture

Ce module est une base solide pour aller plus loin. Les idées d’évolution (multi-exemplaires, appli mobile, intégration externe…) pourraient faire l’objet de futurs projets, dans une logique d’amélioration continue.

> *En résumé, ce projet nous a permis, en tant que groupe, de passer de la théorie à la pratique, en créant une solution concrète, utile et professionnelle, tout en maîtrisant les concepts clés de la gestion des processus métier et des ERP.*

### 4.1. Gestion des emprunts et retours

Le cœur du module, c’est le prêt et le retour des livres. Voici comment ça se passe :

**Pour emprunter un livre :**
1. On vérifie si le livre est disponible.
2. On vérifie que le membre est *actif* (pas suspendu, pas de retard).
3. On crée un emprunt avec un numéro automatique (ex : EMP00001).
4. La date de retour prévue est calculée automatiquement (14 jours par défaut).
5. Le livre passe à l’état *Emprunté*.

**Pour rendre un livre :**
1. On enregistre la date de retour réelle.
2. Le livre redevient *Disponible*.
3. On calcule s’il y a du retard.
4. Si oui, une pénalité est créée automatiquement.

**Gestion des retards :**
- Un programme automatique (cron job) détecte chaque jour les retards.
- Le statut de l’emprunt passe à *En retard*.
- Des rappels sont envoyés automatiquement.

### 4.2. Gestion des membres (adhérents)

**Inscription :**
- Création d’une fiche membre avec un numéro unique (ex : ADH00001).
- Saisie des infos (nom, email, téléphone, adresse, photo).
- Choix du type de membre (Étudiant, Enseignant, etc.).
- Date d’expiration calculée automatiquement (1 an).

**Suivi du statut :**
- *Actif* : adhésion valide, pas de suspension.
- *Expiré* : adhésion dépassée.
- *Suspendu* : compte bloqué (retards répétés, pénalités impayées, etc.).

**Renouvellement :**
- Nouveau paiement d’adhésion.
- Date d’expiration mise à jour.
- Statut repasse à *Actif*.
## 6. Conception et développement du module Odoo

### 6.1. Modélisation des données

Le module s’appuie sur **11 modèles de données** qui sont reliés entre eux, comme dans une vraie base de données relationnelle.

**Principaux modèles utilisés :**

| Modèle | À quoi il sert ? | Liens principaux |
|--------|------------------|-----------------|
| `library.book` | Livre (ISBN, titre, auteur, catégorie, état) | Lien vers auteur et catégorie |
| `library.author` | Auteur (nom, bio, photo, nationalité) | Liste de ses livres |
| `library.category` | Catégorie (arborescence possible) | Liste des livres de la catégorie |
| `library.member` | Membre (numéro, type, email, dates, statut) | Emprunts, pénalités, frais d’adhésion |
| `library.borrowing` | Emprunt (livre, membre, dates, état) | Lien vers livre et membre |
| `library.penalty` | Pénalité (montant, paiements, état) | Lien vers emprunt et membre |
| `library.membership.fee` | Frais d’adhésion (montant, dates, méthode) | Lien vers membre |
| `library.reservation` | Réservation (livre, membre, file d’attente) | Lien vers livre et membre |
| `library.notification.settings` | Paramètres des notifications | - |
| `library.notification.log` | Journal des notifications | Lien vers membre et emprunt |
| `library.dashboard` | Tableau de bord (statistiques) | - |

**Contraintes et règles :**
- ISBN unique pour chaque livre
- Nom de catégorie unique
- Numérotation automatique pour les emprunts, membres, pénalités, etc.

**Champs calculés automatiquement :**
- Nombre de livres par auteur ou catégorie
- Jours d’emprunt, jours de retard, montant restant d’une pénalité
- Statut du membre (actif, expiré, suspendu)
- Statistiques du tableau de bord en temps réel

### 6.2. Fonctionnalités développées

Le module propose de nombreuses fonctionnalités pratiques :

**Pour le catalogue :**
- Ajouter, modifier, supprimer des livres, auteurs, catégories
- Afficher les couvertures en mode Kanban (vue imagée)
- Couleurs selon l’état du livre (disponible, emprunté, réservé, etc.)
- Historique des emprunts pour chaque livre
- Importer un catalogue en masse via un assistant CSV (création, mise à jour, mixte)

**Pour les membres :**
- Fiches complètes avec photo, type, coordonnées
- Numéro de carte généré automatiquement (ex : ADH00001)
- Statut calculé dynamiquement (actif, expiré, suspendu)
- Boutons rapides pour voir les emprunts et pénalités
- Actions : renouveler, suspendre, activer

**Pour les emprunts :**
- Suivi du workflow (brouillon → emprunté → retourné/en retard)
- Calcul automatique de la date de retour
- Détection automatique des retards
- Boutons d’action : confirmer, retourner, marquer perdu, annuler

**Pour les réservations :**
- Réserver un livre déjà emprunté (file d’attente)
- Limite de 3 réservations par membre
- États : en attente, disponible, récupéré, expiré, annulé
- Notification automatique quand le livre est disponible
- Expiration automatique si non récupéré sous 3 jours

**Pour la gestion financière :**
- Calcul automatique des pénalités (jours de retard × tarif)
- Suivi du paiement (brouillon → confirmé → payé)
- Assistant de paiement pour gérer les paiements partiels
- Frais d’adhésion différents selon le type de membre
- Historique complet des transactions

**Pour les notifications :**
- Rappels d’échéance, alertes de retard, expiration d’adhésion
- Paramétrage centralisé (méthodes, délais, fréquences)
- Modèles d’emails professionnels
- Journal détaillé des notifications
- Trois programmes automatiques (cron jobs) pour tout vérifier chaque jour

**Pour le reporting :**
- Tableau de bord avec indicateurs en temps réel (livres, emprunts, membres)
- Graphiques (barres, camembert) pour analyser l’activité
- Tableaux croisés dynamiques (Pivot)
- Boutons d’accès rapide aux vues filtrées

### 6.3. Workflow métier simplifié

Voici le parcours type dans le module :

```
1. Ajouter les livres (à la main ou par import CSV)
2. Inscrire les membres
3. Enregistrer le paiement d’adhésion
4. Créer un emprunt (si livre dispo et membre actif)
5. Confirmer l’emprunt (le livre passe à l’état emprunté)
6. Notifications automatiques de rappel
7. Retour du livre (mise à jour des états)
8. Génération automatique d’une pénalité si retard
9. Paiement de la pénalité
10. Renouvellement de l’adhésion si besoin
```

Ce workflow montre la logique et la cohérence du module.

### 6.4. Installation et démarrage du module

#### 6.4.1. Prérequis techniques

Pour installer le module, il faut :
- Docker et Docker Compose installés
- Les ports 8069 (Odoo) et 5432 (PostgreSQL) libres
- Un système compatible (Windows, Linux, macOS)

#### 6.4.2. Structure du projet

Le projet doit être organisé ainsi :

```
edu_gourou/
├── docker-compose.yml
└── library_management/   # Le module Odoo
    ├── __init__.py
    ...
    └── static/
```

#### 6.4.3. Démarrage rapide

**1. Placer le projet dans le bon dossier**

```bash
cd C:\Users\X1\Documents\edu_gourou
```

**2. Lancer les conteneurs Docker**

```bash
docker-compose up -d
```

Cette commande lance deux conteneurs :
- Odoo (version 17.0) sur le port 8069
- PostgreSQL (version 15) pour la base de données

**3. Vérifier que tout démarre bien**

```bash
docker-compose ps
```

Les deux services doivent être "Up".

**4. Accéder à Odoo**

Ouvrir un navigateur et aller sur : `http://localhost:8069`

À la première connexion, Odoo demande de créer une base de données.

**5. Activer le mode développeur**

Dans Odoo :
1. Aller dans Paramètres → Général
2. Activer le mode développeur

**6. Installer le module**

1. Aller dans Applications
2. Cliquer sur "Mettre à jour la liste des applications"
3. Chercher "Gestion de Bibliothèque"
4. Cliquer sur "Installer"

L’installation crée automatiquement :
- Les tables pour tous les modèles
- Les vues et menus
- Les données de démonstration (catégories, auteurs, livres)
- Les programmes automatiques (cron jobs)
- Les séquences de numérotation

### 6.4.4. Commandes Docker utiles

**Voir les logs en temps réel**

```bash
docker-compose logs -f web
```

**Redémarrer Odoo uniquement**

```bash
docker-compose restart web
```

**Arrêter tous les services**

```bash
docker-compose down
```

**Tout supprimer (y compris les données !)**

```bash
docker-compose down -v
```

**Reconstruire les conteneurs après modification**

```bash
docker-compose up -d --build
```

#### 6.4.5. Vérification de l’installation

Après installation, vérifier que :
- Le menu "Bibliothèque" apparaît
- Le tableau de bord affiche les statistiques
- Les données de démo sont présentes (3 livres, 3 auteurs, 7 catégories)
- Les programmes automatiques (cron jobs) sont actifs (Paramètres → Technique → Tâches planifiées)

En cas de souci, consulter les logs Docker pour trouver l’erreur.

---
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

Voici un aperçu visuel des principales interfaces du module, pour mieux comprendre son fonctionnement.

### 7.1. Tableau de bord et reporting

Le **tableau de bord** est le point d’entrée du module. Il donne une vue d’ensemble en temps réel sur l’activité de la bibliothèque.

![Tableau de bord principal](images/dashboard.png)

On y retrouve les chiffres clés (livres disponibles, emprunts en cours, membres actifs) et des boutons pour accéder rapidement aux différentes vues.

![Graphique des emprunts par mois](images/graph_emprunts.png)

Ce graphique permet de voir l’évolution des emprunts au fil des mois.

### 7.2. Gestion du catalogue de livres

La **vue Kanban** des livres est très visuelle et pratique pour parcourir le catalogue.

![Vue Kanban des livres](images/livres_kanban.png)

Chaque carte montre la couverture, le titre, l’auteur, la catégorie et l’état du livre (avec des couleurs différentes selon le statut).

![Formulaire de livre](images/livre_form.png)

Le formulaire d’un livre permet de saisir toutes les infos et de voir l’historique des emprunts.

### 7.3. Gestion des membres

La fiche membre regroupe toutes les infos et statistiques sur un adhérent.

![Fiche adhérent](images/adherent_form.png)

Des boutons rapides permettent d’accéder à ses emprunts, pénalités et paiements d’adhésion.

### 7.4. Gestion des emprunts

La liste des emprunts permet de suivre l’état de chaque prêt et de gérer les retours.

![Liste des emprunts](images/emprunts_liste.png)

Les emprunts en retard sont affichés en rouge pour être repérés facilement.

![Formulaire d'emprunt](images/emprunt_form.png)

Le formulaire d’emprunt affiche une barre d’état et des boutons d’action selon le contexte.

### 7.5. Système de réservations

Les membres peuvent réserver des livres déjà empruntés.

![Vue des réservations](images/reservations_liste.png)

On voit la position dans la file d’attente, et le statut change automatiquement quand le livre redevient disponible.

### 7.6. Gestion financière

Le module gère les pénalités de retard et les frais d’adhésion de façon claire.

![Liste des pénalités](images/penalites_liste.png)

![Assistant de paiement](images/paiement_wizard.png)

L’assistant de paiement permet d’enregistrer un paiement partiel ou total, en choisissant le moyen de paiement.

### 7.7. Notifications automatiques

Un journal garde la trace de toutes les notifications envoyées.

![Journal des notifications](images/notifications_log.png)

![Paramètres des notifications](images/notifications_settings.png)

On peut configurer les délais, fréquences et méthodes d’envoi (email, Odoo, ou les deux).

### 7.8. Import de catalogue CSV

Un assistant facilite l’import en masse de livres.

![Assistant d'import CSV](images/import_csv_wizard.png)

L’import crée automatiquement les auteurs et catégories manquants, et génère un rapport détaillé.

---

## 8. Limites du projet et perspectives d'amélioration

Même si le module est complet, il reste des points à améliorer ou à ajouter.

### 8.1. Limites actuelles

**Fonctionnalités non présentes :**
- Un seul exemplaire par livre (pas de gestion multi-exemplaires)
- Pas d’indication de l’emplacement physique du livre (étagère, rayon…)
- Pas de système de notes ou de commentaires par les membres
- Pas de recherche avancée sur le texte des livres

**Limites techniques :**
- Les droits d’accès ne sont pas différenciés selon le rôle (bibliothécaire, membre, admin)
- Pas d’application mobile dédiée
- Export limité aux formats Odoo standards (pas d’export MARC)
- Pas d’intégration avec des systèmes externes (paiement en ligne, catalogues partagés)

**Limites ergonomiques :**
- Interface pensée pour ordinateur, moins adaptée aux tablettes et smartphones
- Certaines actions demandent plusieurs clics

### 8.2. Idées d’amélioration

**Fonctionnalités à ajouter :**
- Gérer plusieurs exemplaires d’un même livre
- Système de recommandations selon l’historique d’emprunts
- Calendrier d’événements (clubs de lecture, rencontres d’auteurs…)
- Gestion de documents numériques (e-books, PDF)

**Améliorations techniques :**
- Développer une API REST pour connecter d’autres applications
- Créer une application mobile (iOS/Android)
- Intégrer le paiement en ligne pour les pénalités et adhésions
- Exporter au format MARC pour être compatible avec d’autres systèmes

**Pour l’analyse et le pilotage :**
- Rapports avancés (livres les plus empruntés, taux d’occupation…)
- Tableaux de bord personnalisés selon le rôle
- Nouveaux indicateurs de performance (KPI)

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