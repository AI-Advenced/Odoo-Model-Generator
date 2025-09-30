# Gestion d'Événements

## Description


Module complet de gestion d'événements avec:
- Création et gestion d'événements
- Système d'inscriptions
- Gestion des participants
- Suivi des paiements
- Rapports et analyses
            

## Fonctionnalités


- Gestion complète des événements

- Gestion complète des inscription à un événements

- Interface utilisateur intuitive

- Vues multiples (liste, formulaire, kanban)

- Système de permissions granulaires

- Données de démonstration incluses


## Modèles


### Événement (`event.custom`)

Événement

**Champs:**

- `name` (char): Nom de l'Événement

- `description` (html): Description

- `event_type` (selection): Type d'Événement

- `start_date` (datetime): Date de Début

- `end_date` (datetime): Date de Fin

- `location` (char): Lieu

- `max_participants` (integer): Nombre Maximum de Participants

- `price` (float): Prix d'Inscription

- `organizer_id` (many2one): Organisateur

- `registration_ids` (one2many): Inscriptions

- `status` (selection): Statut

- `image` (binary): Image de l'Événement

- `active` (boolean): Actif



### Inscription à un Événement (`event.registration`)

Inscription à un Événement

**Champs:**

- `name` (char): Nom du Participant

- `email` (char): Email

- `phone` (char): Téléphone

- `company` (char): Entreprise

- `event_id` (many2one): Événement

- `registration_date` (datetime): Date d'Inscription

- `state` (selection): État

- `payment_status` (selection): Statut Paiement

- `amount_paid` (float): Montant Payé

- `notes` (text): Notes

- `active` (boolean): Actif




## Installation

1. Copiez ce module dans votre dossier d'addons Odoo
2. Redémarrez le serveur Odoo
3. Activez le mode développeur
4. Allez dans Apps > Mettre à jour la liste des applications
5. Recherchez "Gestion d'Événements" et installez-le

## Configuration

Après installation, vous trouverez les nouveaux menus dans l'interface Odoo.

## Support

Ce module a été généré automatiquement avec Odoo Model Generator.
Pour des modifications, utilisez l'outil de génération ou modifiez le code manuellement.

## Licence

LGPL-3