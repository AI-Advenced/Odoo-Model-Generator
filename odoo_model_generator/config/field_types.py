# -*- coding: utf-8 -*-
"""
Types de champs et configurations pour Odoo Model Generator
"""

from enum import Enum
from typing import Dict, Any, List, Optional

class FieldType(Enum):
    """Types de champs supportés par Odoo"""
    CHAR = "char"
    TEXT = "text"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    SELECTION = "selection"
    MANY2ONE = "many2one"
    ONE2MANY = "one2many"
    MANY2MANY = "many2many"
    BINARY = "binary"
    HTML = "html"
    MONETARY = "monetary"

class FieldConfig:
    """Configuration d'un champ Odoo"""
    
    def __init__(self, 
                 name: str,
                 field_type: FieldType,
                 label: str = None,
                 required: bool = False,
                 readonly: bool = False,
                 help_text: str = None,
                 default_value: Any = None,
                 **kwargs):
        self.name = name
        self.field_type = field_type
        self.label = label or name.replace('_', ' ').title()
        self.required = required
        self.readonly = readonly
        self.help_text = help_text
        self.default_value = default_value
        self.extra_attrs = kwargs

    def __repr__(self):
        return f"FieldConfig(name='{self.name}', type='{self.field_type.value}')"

class ModelConfig:
    """Configuration d'un modèle Odoo"""
    
    def __init__(self,
                 name: str,
                 description: str = None,
                 table_name: str = None,
                 inherit: List[str] = None,
                 fields: List[FieldConfig] = None,
                 auto_create_views: bool = True,
                 auto_create_menu: bool = True,
                 menu_parent: str = None,
                 security_groups: List[str] = None):
        self.name = name
        self.description = description or name.replace('.', ' ').title()
        self.table_name = table_name
        self.inherit = inherit or []
        self.fields = fields or []
        self.auto_create_views = auto_create_views
        self.auto_create_menu = auto_create_menu
        self.menu_parent = menu_parent
        self.security_groups = security_groups or ['base.group_user']

    def add_field(self, field: FieldConfig):
        """Ajoute un champ au modèle"""
        self.fields.append(field)

    def get_field(self, name: str) -> Optional[FieldConfig]:
        """Récupère un champ par son nom"""
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def __repr__(self):
        return f"ModelConfig(name='{self.name}', fields={len(self.fields)})"

class ModuleConfig:
    """Configuration d'un module Odoo"""
    
    def __init__(self,
                 name: str,
                 version: str = "17.0.1.0.0",
                 category: str = "Custom",
                 summary: str = None,
                 description: str = None,
                 author: str = "Odoo Model Generator",
                 website: str = "https://github.com",
                 depends: List[str] = None,
                 license: str = "LGPL-3",
                 is_application: bool = True,
                 sequence: int = 100):
        self.name = name
        self.version = version
        self.category = category
        self.summary = summary or f"Module {name}"
        self.description = description or f"Module généré automatiquement: {name}"
        self.author = author
        self.website = website
        self.depends = depends or ['base', 'mail']
        self.license = license
        self.is_application = is_application
        self.sequence = sequence

    def __repr__(self):
        return f"ModuleConfig(name='{self.name}', version='{self.version}')"