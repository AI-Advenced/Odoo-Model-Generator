# -*- coding: utf-8 -*-
{
    'name': 'Mon Module Personnalisé',
    'version': '17.0.1.0.0',
    'category': 'Custom',
    'summary': 'Module Mon Module Personnalisé',
    'description': """
Module généré automatiquement avec Odoo Model Generator

Généré automatiquement par Odoo Model Generator.

Fonctionnalités:

- Gestion des Mon Modèle


Modèles inclus:

- Mon Modèle (x_my_model)

    """,
    'author': 'Mon Entreprise',
    'website': 'https://github.com',
    'depends': ['base', 'mail'],
    'data': ["'security/ir.model.access.csv'", "'views/x_my_model_views.xml'", "'views/x_my_model_menu.xml'"],
    'demo': ["'demo/x_my_model_demo.xml'"],
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