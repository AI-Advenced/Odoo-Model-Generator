# -*- coding: utf-8 -*-
{
    'name': 'Gestion d'Événements',
    'version': '17.0.1.0.0',
    'category': 'Events',
    'summary': 'Système de gestion d'événements et inscriptions',
    'description': """

Module complet de gestion d'événements avec:
- Création et gestion d'événements
- Système d'inscriptions
- Gestion des participants
- Suivi des paiements
- Rapports et analyses
            

Généré automatiquement par Odoo Model Generator.

Fonctionnalités:

- Gestion des Événement

- Gestion des Inscription à un Événement


Modèles inclus:

- Événement (event.custom)

- Inscription à un Événement (event.registration)

    """,
    'author': 'Demo Company',
    'website': 'https://demo-events.com',
    'depends': ['base', 'mail', 'website', 'payment'],
    'data': ["'security/ir.model.access.csv'", "'views/event_custom_views.xml'", "'views/event_custom_menu.xml'", "'views/event_registration_views.xml'", "'views/event_registration_menu.xml'", "'views/menu_global.xml'"],
    'demo': ["'demo/event_custom_demo.xml'", "'demo/event_registration_demo.xml'"],
    'qweb': [],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 100,
    'license': 'LGPL-3',
}