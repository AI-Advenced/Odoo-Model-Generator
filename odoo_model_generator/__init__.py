# -*- coding: utf-8 -*-
"""
Odoo Model Generator - Générateur automatique de modules Odoo

Ce package permet de générer automatiquement des modules Odoo complets
à partir de configurations YAML ou JSON.

Usage:
    from odoo_model_generator import OdooModelGenerator
    
    generator = OdooModelGenerator()
    module_path = generator.generate_from_file('config.yaml', './output', 'my_module')

CLI:
    omg generate -c config.yaml -n my_module -o ./output
    omg init-config -t basic -o config.yaml
"""

__version__ = '1.0.0'
__author__ = 'Odoo Model Generator Team'
__email__ = 'info@odoo-model-generator.com'

from .core.generator import OdooModelGenerator
from .config.field_types import FieldType, FieldConfig, ModelConfig, ModuleConfig

__all__ = [
    'OdooModelGenerator',
    'FieldType',
    'FieldConfig', 
    'ModelConfig',
    'ModuleConfig'
]