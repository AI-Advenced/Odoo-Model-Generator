# -*- coding: utf-8 -*-
"""
Configuration par défaut pour Odoo Model Generator
"""

# Champs par défaut ajoutés automatiquement à chaque modèle
DEFAULT_FIELDS = [
    {
        'name': 'active',
        'type': 'boolean',
        'label': 'Actif',
        'default': True,
        'help_text': 'Décochez pour archiver cet enregistrement'
    }
]

# Dépendances par défaut pour les modules
DEFAULT_DEPENDS = ['base', 'mail']

# Configuration par défaut du module
DEFAULT_MODULE_CONFIG = {
    'version': '17.0.1.0.0',
    'category': 'Custom',
    'author': 'Odoo Model Generator',
    'website': 'https://github.com',
    'license': 'LGPL-3',
    'is_application': True,
    'sequence': 100
}

# Groupes de sécurité par défaut
DEFAULT_SECURITY_GROUPS = ['base.group_user']

# Templates par défaut pour différents types de modules
MODULE_TEMPLATES = {
    'basic': {
        'description': 'Module basique avec modèle simple',
        'depends': ['base'],
        'category': 'Custom'
    },
    'crm': {
        'description': 'Module CRM personnalisé',
        'depends': ['base', 'mail', 'crm'],
        'category': 'Sales/CRM'
    },
    'inventory': {
        'description': 'Module de gestion des stocks',
        'depends': ['base', 'mail', 'stock'],
        'category': 'Inventory/Inventory'
    },
    'hr': {
        'description': 'Module de ressources humaines',
        'depends': ['base', 'mail', 'hr'],
        'category': 'Human Resources'
    },
    'accounting': {
        'description': 'Module de comptabilité',
        'depends': ['base', 'mail', 'account'],
        'category': 'Accounting/Accounting'
    }
}

# Types de vues supportées
SUPPORTED_VIEW_TYPES = [
    'tree',
    'form', 
    'kanban',
    'calendar',
    'graph',
    'pivot',
    'search'
]

# Widgets par type de champ
FIELD_WIDGETS = {
    'char': ['char', 'email', 'url', 'phone'],
    'text': ['text', 'html'],
    'integer': ['integer', 'progressbar'],
    'float': ['float', 'monetary', 'percentage'],
    'boolean': ['boolean', 'toggle'],
    'date': ['date'],
    'datetime': ['datetime'],
    'binary': ['image', 'pdf_viewer'],
    'many2one': ['many2one', 'selection'],
    'one2many': ['one2many'],
    'many2many': ['many2many', 'many2many_tags'],
    'selection': ['selection', 'radio']
}