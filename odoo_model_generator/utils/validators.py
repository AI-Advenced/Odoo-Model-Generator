# -*- coding: utf-8 -*-
"""
Validateurs pour la configuration
"""

import re
from typing import Dict, List, Any
from ..config.field_types import ModelConfig, FieldConfig, FieldType

class ConfigValidator:
    """Validateur de configuration pour les modèles Odoo"""
    
    # Patterns de validation
    MODEL_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9_.]*[a-z0-9]$')
    FIELD_NAME_PATTERN = re.compile(r'^[a-z][a-z0-9_]*$')
    PYTHON_IDENTIFIER_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    
    # Mots réservés Python et Odoo
    RESERVED_WORDS = {
        'class', 'def', 'if', 'else', 'elif', 'try', 'except', 'finally',
        'for', 'while', 'with', 'import', 'from', 'as', 'return', 'yield',
        'lambda', 'global', 'nonlocal', 'assert', 'break', 'continue',
        'pass', 'raise', 'del', 'and', 'or', 'not', 'is', 'in',
        # Mots réservés Odoo
        'id', 'create_date', 'create_uid', 'write_date', 'write_uid',
        '__last_update', 'display_name'
    }
    
    @classmethod
    def validate_model_name(cls, name: str) -> bool:
        """Valide le nom d'un modèle Odoo"""
        if not name:
            raise ValueError("Le nom du modèle ne peut pas être vide")
        
        if not cls.MODEL_NAME_PATTERN.match(name):
            raise ValueError(
                f"Nom de modèle invalide: {name}. "
                f"Doit commencer par une lettre minuscule et contenir seulement "
                f"des lettres, chiffres, points et underscores"
            )
        
        if len(name) > 63:  # Limite PostgreSQL pour les noms de tables
            raise ValueError(f"Nom de modèle trop long (max 63 caractères): {name}")
        
        return True
    
    @classmethod
    def validate_field_name(cls, name: str, model_name: str = None) -> bool:
        """Valide le nom d'un champ"""
        if not name:
            raise ValueError("Le nom du champ ne peut pas être vide")
        
        if not cls.FIELD_NAME_PATTERN.match(name):
            raise ValueError(
                f"Nom de champ invalide: {name}. "
                f"Doit commencer par une lettre minuscule et contenir seulement "
                f"des lettres, chiffres et underscores"
            )
        
        if name in cls.RESERVED_WORDS:
            raise ValueError(f"Nom de champ réservé: {name}")
        
        if len(name) > 63:
            raise ValueError(f"Nom de champ trop long (max 63 caractères): {name}")
        
        # Validation spécifique à Odoo
        if name.startswith('_'):
            raise ValueError(f"Les noms de champs ne peuvent pas commencer par underscore: {name}")
        
        if name.endswith('_id') and len(name) > 3:
            # Probablement un champ relationnel
            base_name = name[:-3]
            if not cls.PYTHON_IDENTIFIER_PATTERN.match(base_name):
                raise ValueError(f"Nom de champ relationnel invalide: {name}")
        
        return True
    
    @classmethod
    def validate_field_config(cls, field: FieldConfig) -> bool:
        """Valide la configuration d'un champ"""
        cls.validate_field_name(field.name)
        
        # Validation selon le type de champ
        if field.field_type == FieldType.CHAR:
            size = field.extra_attrs.get('size', 255)
            if not isinstance(size, int) or size <= 0:
                raise ValueError(f"Taille invalide pour le champ char {field.name}: {size}")
            if size > 65535:
                raise ValueError(f"Taille trop grande pour le champ char {field.name}: {size}")
        
        elif field.field_type == FieldType.SELECTION:
            selection = field.extra_attrs.get('selection', [])
            if not selection:
                raise ValueError(f"Selection vide pour le champ {field.name}")
            
            for item in selection:
                if not isinstance(item, (list, tuple)) or len(item) != 2:
                    raise ValueError(f"Format de selection invalide pour {field.name}: {item}")
        
        elif field.field_type in [FieldType.MANY2ONE, FieldType.ONE2MANY, FieldType.MANY2MANY]:
            comodel = field.extra_attrs.get('comodel_name')
            if not comodel:
                raise ValueError(f"comodel_name requis pour le champ relationnel {field.name}")
            
            cls.validate_model_name(comodel)
        
        elif field.field_type == FieldType.ONE2MANY:
            inverse_name = field.extra_attrs.get('inverse_name')
            if inverse_name:
                cls.validate_field_name(inverse_name)
        
        return True
    
    @classmethod
    def validate_model_config(cls, model: ModelConfig) -> bool:
        """Valide la configuration d'un modèle"""
        cls.validate_model_name(model.name)
        
        if not model.fields:
            raise ValueError(f"Le modèle {model.name} doit avoir au moins un champ")
        
        # Validation des noms de champs uniques
        field_names = [field.name for field in model.fields]
        duplicates = [name for name in set(field_names) if field_names.count(name) > 1]
        if duplicates:
            raise ValueError(f"Champs dupliqués dans {model.name}: {duplicates}")
        
        # Validation de chaque champ
        for field in model.fields:
            cls.validate_field_config(field)
        
        # Validation de l'héritage
        for inherit_model in model.inherit:
            cls.validate_model_name(inherit_model)
        
        # Validation du nom de table personnalisé
        if model.table_name:
            if not re.match(r'^[a-z][a-z0-9_]*$', model.table_name):
                raise ValueError(f"Nom de table invalide: {model.table_name}")
        
        return True
    
    @classmethod
    def validate_models_consistency(cls, models: List[ModelConfig]) -> bool:
        """Valide la cohérence entre plusieurs modèles"""
        model_names = [model.name for model in models]
        
        # Vérification des noms de modèles uniques
        duplicates = [name for name in set(model_names) if model_names.count(name) > 1]
        if duplicates:
            raise ValueError(f"Noms de modèles dupliqués: {duplicates}")
        
        # Validation des références entre modèles
        for model in models:
            for field in model.fields:
                if field.field_type in [FieldType.MANY2ONE, FieldType.ONE2MANY, FieldType.MANY2MANY]:
                    comodel = field.extra_attrs.get('comodel_name')
                    if comodel and comodel in model_names:
                        # Référence vers un modèle du même module - OK
                        continue
                    elif comodel and not comodel.startswith('res.') and not comodel.startswith('ir.'):
                        # Référence vers un modèle externe - avertissement
                        print(f"Avertissement: Référence vers un modèle externe: {comodel}")
        
        return True
    
    @classmethod
    def validate_module_structure(cls, config_data: Dict) -> bool:
        """Valide la structure complète de la configuration du module"""
        
        # Validation de la section module
        module_config = config_data.get('module', {})
        if not module_config.get('name'):
            raise ValueError("Le nom du module est requis")
        
        # Validation de la section models
        models_data = config_data.get('models', [])
        if not models_data:
            raise ValueError("Au moins un modèle est requis")
        
        return True
    
    @classmethod
    def get_validation_suggestions(cls, field_name: str) -> List[str]:
        """Retourne des suggestions pour corriger un nom de champ invalide"""
        suggestions = []
        
        # Correction des caractères invalides
        cleaned = re.sub(r'[^a-z0-9_]', '_', field_name.lower())
        if cleaned != field_name:
            suggestions.append(f"Utiliser: {cleaned}")
        
        # Correction du début par chiffre
        if field_name and field_name[0].isdigit():
            suggestions.append(f"Utiliser: field_{field_name}")
        
        # Correction des mots réservés
        if field_name in cls.RESERVED_WORDS:
            suggestions.append(f"Utiliser: {field_name}_field")
            suggestions.append(f"Utiliser: custom_{field_name}")
        
        return suggestions