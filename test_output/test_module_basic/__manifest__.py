# -*- coding: utf-8 -*-
{
    'name': 'Test Module Basique',
    'version': '17.0.1.0.0',
    'category': 'Test',
    'summary': 'Module Test Module Basique',
    'description': """
Module de test généré automatiquement

Généré automatiquement par Odoo Model Generator.

Fonctionnalités:

- Gestion des Produit de Test


Modèles inclus:

- Produit de Test (test.product)

    """,
    'author': 'Test Author',
    'website': 'https://github.com',
    'depends': ['base', 'mail'],
    'data': ["'security/ir.model.access.csv'", "'views/test_product_views.xml'", "'views/test_product_menu.xml'"],
    'demo': ["'demo/test_product_demo.xml'"],
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