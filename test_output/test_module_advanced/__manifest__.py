# -*- coding: utf-8 -*-
{
    'name': 'Test Module Avancé',
    'version': '17.0.1.0.0',
    'category': 'Test',
    'summary': 'Module Test Module Avancé',
    'description': """
Module de test avec relations

Généré automatiquement par Odoo Model Generator.

Fonctionnalités:

- Gestion des Catégorie de Test

- Gestion des Produit Avancé


Modèles inclus:

- Catégorie de Test (test.category)

- Produit Avancé (test.advanced.product)

    """,
    'author': 'Odoo Model Generator',
    'website': 'https://github.com',
    'depends': ['base', 'mail'],
    'data': ["'security/ir.model.access.csv'", "'views/test_category_views.xml'", "'views/test_category_menu.xml'", "'views/test_advanced_product_views.xml'", "'views/test_advanced_product_menu.xml'", "'views/menu_global.xml'"],
    'demo': ["'demo/test_category_demo.xml'", "'demo/test_advanced_product_demo.xml'"],
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