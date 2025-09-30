# Test Module Avancé

## Description

Module de test avec relations

## Fonctionnalités


- Gestion complète des catégorie de tests

- Gestion complète des produit avancés

- Interface utilisateur intuitive

- Vues multiples (liste, formulaire, kanban)

- Système de permissions granulaires

- Données de démonstration incluses


## Modèles


### Catégorie de Test (`test.category`)

Catégorie de Test

**Champs:**

- `name` (char): Nom

- `code` (char): Code

- `active` (boolean): Actif



### Produit Avancé (`test.advanced.product`)

Produit Avancé

**Champs:**

- `name` (char): Nom

- `category_id` (many2one): Catégorie

- `tag_ids` (many2many): Étiquettes

- `status` (selection): Statut

- `active` (boolean): Actif




## Installation

1. Copiez ce module dans votre dossier d'addons Odoo
2. Redémarrez le serveur Odoo
3. Activez le mode développeur
4. Allez dans Apps > Mettre à jour la liste des applications
5. Recherchez "Test Module Avancé" et installez-le

## Configuration

Après installation, vous trouverez les nouveaux menus dans l'interface Odoo.

## Support

Ce module a été généré automatiquement avec Odoo Model Generator.
Pour des modifications, utilisez l'outil de génération ou modifiez le code manuellement.

## Licence

LGPL-3