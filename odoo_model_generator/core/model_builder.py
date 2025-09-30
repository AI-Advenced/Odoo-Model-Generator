# -*- coding: utf-8 -*-
"""
Générateur de modèles Odoo
"""

from typing import List, Dict
from jinja2 import Template
from ..config.field_types import ModelConfig, FieldConfig, FieldType

class ModelBuilder:
    """Construit les modèles Python pour Odoo"""
    
    def __init__(self):
        self.model_template = Template('''# -*- coding: utf-8 -*-
"""
{{ description }}
Généré automatiquement par Odoo Model Generator
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class {{ class_name }}(models.Model):
    """{{ description }}"""
    
    _name = '{{ model_name }}'
    {% if table_name %}_table = '{{ table_name }}'{% endif %}
    _description = '{{ description }}'
    {% if inherit %}_inherit = {{ inherit }}{% endif %}
    _order = '{{ default_order }}'
    {% if rec_name %}_rec_name = '{{ rec_name }}'{% endif %}
    
    # ============ CHAMPS ============
    {% for field in fields %}
    {{ field.definition }}
    {% endfor %}
    
    # ============ MÉTHODES CALCULÉES ============
    {% for computed_field in computed_fields %}
    {{ computed_field.method }}
    {% endfor %}
    
    # ============ CONTRAINTES ============
    {% for constraint in constraints %}
    {{ constraint }}
    {% endfor %}
    
    # ============ MÉTHODES BUSINESS ============
    def name_get(self):
        """Personnalisation de l'affichage du nom"""
        result = []
        for record in self:
            {% if rec_name %}
            name = record.{{ rec_name }} or f"#{record.id}"
            {% else %}
            name = f"#{record.id}"
            {% endif %}
            result.append((record.id, name))
        return result
    
    @api.model
    def create(self, vals):
        """Méthode de création personnalisée"""
        # Ajoutez ici votre logique de création
        return super().create(vals)
    
    def write(self, vals):
        """Méthode de modification personnalisée"""
        # Ajoutez ici votre logique de modification
        return super().write(vals)
    
    def unlink(self):
        """Méthode de suppression personnalisée"""
        # Ajoutez ici votre logique de suppression
        return super().unlink()
    
    {% for method in business_methods %}
    {{ method }}
    {% endfor %}
''')

    def build_field_definition(self, field_config: FieldConfig) -> str:
        """Génère la définition d'un champ Odoo"""
        field_type = field_config.field_type
        attrs = []
        
        # Attributs de base
        if field_config.label:
            attrs.append(f"string='{field_config.label}'")
        if field_config.required:
            attrs.append("required=True")
        if field_config.readonly:
            attrs.append("readonly=True")
        if field_config.help_text:
            attrs.append(f"help='{field_config.help_text}'")
        if field_config.default_value is not None:
            if isinstance(field_config.default_value, str) and field_config.default_value.startswith('fields.'):
                attrs.append(f"default={field_config.default_value}")
            else:
                attrs.append(f"default={repr(field_config.default_value)}")
            
        # Attributs spécifiques par type
        if field_type == FieldType.CHAR:
            size = field_config.extra_attrs.get('size', 255)
            attrs.append(f"size={size}")
        elif field_type == FieldType.SELECTION:
            selection = field_config.extra_attrs.get('selection', [])
            attrs.append(f"selection={selection}")
        elif field_type in [FieldType.MANY2ONE, FieldType.ONE2MANY, FieldType.MANY2MANY]:
            comodel = field_config.extra_attrs.get('comodel_name')
            if comodel:
                attrs.append(f"comodel_name='{comodel}'")
            if field_type == FieldType.ONE2MANY:
                inverse_name = field_config.extra_attrs.get('inverse_name')
                if inverse_name:
                    attrs.append(f"inverse_name='{inverse_name}'")
            elif field_type == FieldType.MANY2MANY:
                relation = field_config.extra_attrs.get('relation')
                column1 = field_config.extra_attrs.get('column1')
                column2 = field_config.extra_attrs.get('column2')
                if relation:
                    attrs.append(f"relation='{relation}'")
                if column1:
                    attrs.append(f"column1='{column1}'")
                if column2:
                    attrs.append(f"column2='{column2}'")
        elif field_type == FieldType.MONETARY:
            currency_field = field_config.extra_attrs.get('currency_field', 'currency_id')
            attrs.append(f"currency_field='{currency_field}'")
        
        # Ajout d'attributs supplémentaires
        for key, value in field_config.extra_attrs.items():
            if key not in ['size', 'selection', 'comodel_name', 'inverse_name', 
                          'relation', 'column1', 'column2', 'currency_field']:
                if isinstance(value, str):
                    attrs.append(f"{key}='{value}'")
                else:
                    attrs.append(f"{key}={value}")
        
        attrs_str = ', '.join(attrs)
        return f"{field_config.name} = fields.{field_type.value.title()}({attrs_str})"

    def generate_model(self, config: ModelConfig) -> str:
        """Génère le code complet du modèle"""
        class_name = ''.join(word.capitalize() for word in config.name.split('.'))
        
        # Génération des définitions de champs
        field_definitions = []
        for field in config.fields:
            field_def = self.build_field_definition(field)
            field_definitions.append({
                'definition': field_def,
                'name': field.name,
                'type': field.field_type
            })
        
        # Ordre par défaut (premier champ char ou name)
        default_order = 'id desc'
        rec_name = None
        for field in config.fields:
            if field.name in ['name', 'title'] or field.field_type == FieldType.CHAR:
                default_order = f"{field.name}"
                rec_name = field.name
                break
        
        # Génération des contraintes
        constraints = self._generate_constraints(config)
        
        # Génération des champs calculés
        computed_fields = self._generate_computed_fields(config)
        
        # Génération des méthodes business
        business_methods = self._generate_business_methods(config)
        
        return self.model_template.render(
            class_name=class_name,
            model_name=config.name,
            table_name=config.table_name,
            description=config.description,
            inherit=config.inherit,
            fields=field_definitions,
            default_order=default_order,
            rec_name=rec_name,
            computed_fields=computed_fields,
            constraints=constraints,
            business_methods=business_methods
        )

    def _generate_constraints(self, config: ModelConfig) -> List[str]:
        """Génère les contraintes du modèle"""
        constraints = []
        
        # Contrainte d'unicité pour les champs uniques
        for field in config.fields:
            if field.extra_attrs.get('unique'):
                constraint = f'''
    _sql_constraints = [
        ('{field.name}_unique', 'UNIQUE({field.name})', 'Le champ {field.label} doit être unique!')
    ]'''
                constraints.append(constraint)
        
        return constraints

    def _generate_computed_fields(self, config: ModelConfig) -> List[Dict]:
        """Génère les champs calculés"""
        computed_fields = []
        
        # Exemple : champ calculé pour le nombre total
        if any(field.field_type == FieldType.ONE2MANY for field in config.fields):
            for field in config.fields:
                if field.field_type == FieldType.ONE2MANY:
                    computed_field = {
                        'name': f"{field.name}_count",
                        'method': f'''
    {field.name}_count = fields.Integer(
        string='Nombre de {field.label}',
        compute='_compute_{field.name}_count'
    )
    
    @api.depends('{field.name}')
    def _compute_{field.name}_count(self):
        """Calcule le nombre d'éléments liés"""
        for record in self:
            record.{field.name}_count = len(record.{field.name})'''
                    }
                    computed_fields.append(computed_field)
        
        return computed_fields

    def _generate_business_methods(self, config: ModelConfig) -> List[str]:
        """Génère les méthodes métier"""
        methods = []
        
        # Méthode d'activation/désactivation si le champ active existe
        if any(field.name == 'active' for field in config.fields):
            method = '''
    def toggle_active(self):
        """Bascule l'état actif/inactif"""
        for record in self:
            record.active = not record.active
        return True
    
    def archive(self):
        """Archive les enregistrements"""
        return self.write({'active': False})
    
    def unarchive(self):
        """Désarchive les enregistrements"""
        return self.write({'active': True})'''
            methods.append(method)
        
        return methods

    def get_field_type_mapping(self) -> Dict[str, str]:
        """Retourne le mapping entre les types de champs et les classes Odoo"""
        return {
            'char': 'fields.Char',
            'text': 'fields.Text',
            'integer': 'fields.Integer',
            'float': 'fields.Float',
            'boolean': 'fields.Boolean',
            'date': 'fields.Date',
            'datetime': 'fields.Datetime',
            'selection': 'fields.Selection',
            'many2one': 'fields.Many2one',
            'one2many': 'fields.One2many',
            'many2many': 'fields.Many2many',
            'binary': 'fields.Binary',
            'html': 'fields.Html',
            'monetary': 'fields.Monetary'
        }