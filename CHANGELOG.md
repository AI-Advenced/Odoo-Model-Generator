# Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/),
et ce projet adhère au [Semantic Versioning](https://semver.org/lang/fr/).

## [1.0.0] - 2024-01-XX

### 🎉 Première version stable

#### Ajouté
- **Générateur principal** : Génération automatique de modules Odoo complets
- **Support des types de champs** : Tous les types de champs Odoo (char, text, integer, float, boolean, date, datetime, selection, many2one, one2many, many2many, binary, html, monetary)
- **Générateur de modèles** : Création automatique des classes Python avec méthodes business
- **Générateur de vues** : Génération des vues XML (liste, formulaire, recherche, kanban)
- **Générateur de menus** : Création des menus et actions Odoo
- **Système de sécurité** : Génération automatique des permissions (ir.model.access.csv)
- **Données de démonstration** : Création automatique d'enregistrements de test
- **Interface CLI** : Commandes intuitives avec `omg`
- **Mode interactif** : Configuration guidée pas à pas
- **Templates prêts** : Templates pour basic, CRM, inventory, HR
- **Support YAML/JSON** : Configuration flexible en YAML ou JSON
- **Validation** : Validation complète des configurations avant génération
- **Documentation** : README complet avec exemples
- **Exemples** : Exemples d'utilisation basiques et avancés

#### Fonctionnalités CLI
- `omg generate` : Génération de modules
- `omg init-config` : Création de templates de configuration
- `omg validate` : Validation des fichiers de configuration
- `omg list-templates` : Liste des templates disponibles
- `omg list-fields` : Liste des types de champs supportés

#### Templates disponibles
- **basic** : Module basique avec modèle simple
- **crm** : Module CRM avec gestion des prospects
- **inventory** : Module de gestion des stocks
- **hr** : Module de ressources humaines

#### Utilitaires
- **Validateurs** : Validation des noms de modèles et champs
- **Formateurs** : Formatage automatique du code Python/XML
- **Gestionnaire de fichiers** : Gestion des opérations sur les fichiers

### 🔧 Technique

#### Architecture
- **Core** : Générateurs modulaires (model_builder, view_builder, menu_builder, module_builder)
- **Config** : Types de champs et configurations par défaut
- **Utils** : Utilitaires de validation, formatage et gestion de fichiers
- **CLI** : Interface en ligne de commande avec Click
- **Templates** : Système de templates Jinja2

#### Dépendances
- Python 3.8+
- Click 8.0+
- Jinja2 3.1+
- PyYAML 6.0+

#### Compatibilité
- Odoo 17.0+
- Linux, macOS, Windows
- Python 3.8, 3.9, 3.10, 3.11, 3.12

### 📝 Documentation

#### Ajouté
- README.md complet avec guide d'utilisation
- Exemples pratiques (basic_example.py, advanced_example.py)
- Fichiers de configuration d'exemple (YAML/JSON)
- Documentation des types de champs
- Guide de contribution
- Licence MIT

### 🧪 Tests et Qualité

#### Préparé pour
- Tests unitaires avec pytest
- Couverture de code avec coverage
- Formatage automatique avec black
- Vérification de style avec flake8
- Vérification de types avec mypy
- Pre-commit hooks

## [Unreleased] - Prochaines versions

### 🚧 Planifié pour v1.1.0
- [ ] Support des wizards (TransientModel)
- [ ] Génération de rapports QWeb
- [ ] Templates spécialisés par secteur
- [ ] Amélioration des vues kanban
- [ ] Support des champs calculés avancés

### 🚧 Planifié pour v1.2.0
- [ ] Interface web graphique
- [ ] API REST pour intégration
- [ ] Support d'Odoo 18.0
- [ ] Génération de tests automatiques
- [ ] Optimisation des performances

### 🚧 Planifié pour v2.0.0
- [ ] Refactoring complet de l'architecture
- [ ] Support des modules existants (modification)
- [ ] Système de plugins
- [ ] Interface collaborative
- [ ] Intégration cloud

## Notes de développement

### Structure des versions
- **Major** (x.0.0) : Changements incompatibles
- **Minor** (x.y.0) : Nouvelles fonctionnalités compatibles
- **Patch** (x.y.z) : Corrections de bugs

### Types de changements
- **Ajouté** : Nouvelles fonctionnalités
- **Modifié** : Changements dans des fonctionnalités existantes
- **Déprécié** : Fonctionnalités bientôt supprimées
- **Supprimé** : Fonctionnalités supprimées
- **Corrigé** : Corrections de bugs
- **Sécurité** : Corrections de vulnérabilités