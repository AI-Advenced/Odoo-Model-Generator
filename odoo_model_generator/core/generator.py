# -*- coding: utf-8 -*-
"""
Générateur principal pour Odoo Model Generator
"""

from typing import Dict, List, Optional
from pathlib import Path
import json
import yaml
import logging

from .model_builder import ModelBuilder
from .view_builder import ViewBuilder  
from .menu_builder import MenuBuilder
from .module_builder import ModuleBuilder
from ..config.field_types import ModelConfig, FieldConfig, FieldType, ModuleConfig
from ..config.default_config import DEFAULT_FIELDS, DEFAULT_MODULE_CONFIG

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OdooModelGenerator:
    """Générateur principal de modules Odoo"""
    
    def __init__(self):
        self.model_builder = ModelBuilder()
        self.view_builder = ViewBuilder()
        self.menu_builder = MenuBuilder()
        self.module_builder = ModuleBuilder()
        self.logger = logger

    def generate_module(self, 
                       config_data: Dict,
                       output_path: str,
                       module_name: str,
                       options: Dict = None) -> str:
        """
        Génère un module Odoo complet
        
        Args:
            config_data: Configuration des modèles et du module
            output_path: Chemin de sortie pour le module
            module_name: Nom du module à créer
            options: Options supplémentaires de génération
            
        Returns:
            Chemin vers le module généré
        """
        options = options or {}
        
        try:
            self.logger.info(f"Démarrage de la génération du module '{module_name}'")
            
            # 1. Parse de la configuration
            models = self._parse_models_config(config_data.get('models', []))
            module_config = self._parse_module_config(config_data.get('module', {}), module_name)
            
            self.logger.info(f"Configuration parsée: {len(models)} modèle(s) trouvé(s)")
            
            # 2. Validation de la configuration
            self._validate_configuration(models, module_config)
            
            # 3. Création de la structure du module
            self.logger.info("Création de la structure du module...")
            module_path = self.module_builder.create_module_structure(
                output_path=output_path,
                module_name=module_name,
                models=models,
                module_config=module_config
            )
            
            # 4. Génération des fichiers pour chaque modèle
            for i, model in enumerate(models):
                self.logger.info(f"Génération du modèle {i+1}/{len(models)}: {model.name}")
                self._generate_model_files(model, module_path, options)
            
            # 5. Génération du menu global si plusieurs modèles
            if len(models) > 1:
                self._generate_global_menu(models, module_path, config_data.get('global_menu', {}))
            
            # 6. Validation finale
            validation_result = self.module_builder.validate_module_structure(module_path)
            failed_validations = [k for k, v in validation_result.items() if not v]
            
            if failed_validations:
                self.logger.warning(f"Validations échouées: {failed_validations}")
            else:
                self.logger.info("✅ Module généré avec succès!")
            
            return module_path
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération: {str(e)}")
            raise

    def generate_from_file(self, 
                          config_file_path: str,
                          output_path: str,
                          module_name: str = None,
                          options: Dict = None) -> str:
        """
        Génère un module à partir d'un fichier de configuration
        
        Args:
            config_file_path: Chemin vers le fichier de configuration
            output_path: Chemin de sortie
            module_name: Nom du module (optionnel, déduit du fichier si absent)
            options: Options de génération
            
        Returns:
            Chemin vers le module généré
        """
        config_data = self._load_config_file(config_file_path)
        
        if not module_name:
            # Déduire le nom du module du fichier ou de la configuration
            config_path = Path(config_file_path)
            module_name = config_data.get('module', {}).get('name') or config_path.stem
        
        return self.generate_module(config_data, output_path, module_name, options)

    def _parse_models_config(self, models_data: List[Dict]) -> List[ModelConfig]:
        """Parse la configuration des modèles"""
        models = []
        
        for model_data in models_data:
            try:
                # Parse des champs
                fields = self._parse_fields_config(model_data.get('fields', []))
                
                # Ajout des champs par défaut si nécessaire
                if model_data.get('add_default_fields', True):
                    default_fields = self._create_default_fields()
                    # Éviter les doublons
                    existing_names = {f.name for f in fields}
                    for default_field in default_fields:
                        if default_field.name not in existing_names:
                            fields.append(default_field)
                
                # Création du modèle
                model = ModelConfig(
                    name=model_data['name'],
                    description=model_data.get('description'),
                    table_name=model_data.get('table_name'),
                    inherit=model_data.get('inherit', []),
                    fields=fields,
                    auto_create_views=model_data.get('auto_create_views', True),
                    auto_create_menu=model_data.get('auto_create_menu', True),
                    menu_parent=model_data.get('menu_parent'),
                    security_groups=model_data.get('security_groups', ['base.group_user'])
                )
                models.append(model)
                
            except Exception as e:
                self.logger.error(f"Erreur lors du parsing du modèle {model_data.get('name', 'inconnu')}: {e}")
                raise
        
        return models

    def _parse_fields_config(self, fields_data: List[Dict]) -> List[FieldConfig]:
        """Parse la configuration des champs"""
        fields = []
        
        for field_data in fields_data:
            try:
                field_type = FieldType(field_data['type'])
                
                # Extraction des attributs supplémentaires
                extra_attrs = {k: v for k, v in field_data.items() 
                             if k not in ['name', 'type', 'label', 'required', 'readonly', 'help_text', 'default']}
                
                field = FieldConfig(
                    name=field_data['name'],
                    field_type=field_type,
                    label=field_data.get('label'),
                    required=field_data.get('required', False),
                    readonly=field_data.get('readonly', False),
                    help_text=field_data.get('help_text'),
                    default_value=field_data.get('default'),
                    **extra_attrs
                )
                fields.append(field)
                
            except Exception as e:
                self.logger.error(f"Erreur lors du parsing du champ {field_data.get('name', 'inconnu')}: {e}")
                raise
        
        return fields

    def _parse_module_config(self, module_data: Dict, module_name: str) -> ModuleConfig:
        """Parse la configuration du module"""
        config = DEFAULT_MODULE_CONFIG.copy()
        config.update(module_data)
        
        return ModuleConfig(
            name=config.get('name', module_name.replace('_', ' ').title()),
            version=config.get('version', '17.0.1.0.0'),
            category=config.get('category', 'Custom'),
            summary=config.get('summary'),
            description=config.get('description'),
            author=config.get('author', 'Odoo Model Generator'),
            website=config.get('website', 'https://github.com'),
            depends=config.get('depends', ['base', 'mail']),
            license=config.get('license', 'LGPL-3'),
            is_application=config.get('is_application', True),
            sequence=config.get('sequence', 100)
        )

    def _create_default_fields(self) -> List[FieldConfig]:
        """Crée les champs par défaut"""
        default_fields = []
        
        for field_data in DEFAULT_FIELDS:
            field_type = FieldType(field_data['type'])
            field = FieldConfig(
                name=field_data['name'],
                field_type=field_type,
                label=field_data.get('label'),
                required=field_data.get('required', False),
                readonly=field_data.get('readonly', False),
                help_text=field_data.get('help_text'),
                default_value=field_data.get('default')
            )
            default_fields.append(field)
        
        return default_fields

    def _validate_configuration(self, models: List[ModelConfig], module_config: ModuleConfig):
        """Valide la configuration avant génération"""
        
        # Validation des noms de modèles
        model_names = [model.name for model in models]
        if len(model_names) != len(set(model_names)):
            raise ValueError("Noms de modèles dupliqués détectés")
        
        # Validation des noms de modèles (format Odoo)
        for model in models:
            if not model.name.replace('_', '').replace('.', '').isalnum():
                raise ValueError(f"Nom de modèle invalide: {model.name}")
        
        # Validation des champs
        for model in models:
            field_names = [field.name for field in model.fields]
            if len(field_names) != len(set(field_names)):
                raise ValueError(f"Champs dupliqués dans le modèle {model.name}")
            
            # Validation des noms de champs
            for field in model.fields:
                if not field.name.replace('_', '').isalnum():
                    raise ValueError(f"Nom de champ invalide: {field.name} dans {model.name}")
        
        self.logger.info("✅ Configuration validée avec succès")

    def _generate_model_files(self, model: ModelConfig, module_path: str, options: Dict):
        """Génère tous les fichiers pour un modèle"""
        module_path = Path(module_path)
        model_underscore = model.name.replace('.', '_')
        
        try:
            # 1. Génération du modèle Python
            self.logger.debug(f"Génération du modèle Python pour {model.name}")
            model_code = self.model_builder.generate_model(model)
            model_file = module_path / 'models' / f'{model_underscore}.py'
            
            with open(model_file, 'w', encoding='utf-8') as f:
                f.write(model_code)
            
            # 2. Génération des vues XML
            if model.auto_create_views:
                self.logger.debug(f"Génération des vues pour {model.name}")
                views_content = self.view_builder.generate_all_views(model)
                views_file = module_path / 'views' / f'{model_underscore}_views.xml'
                
                with open(views_file, 'w', encoding='utf-8') as f:
                    f.write(views_content)
            
            # 3. Génération des menus
            if model.auto_create_menu:
                self.logger.debug(f"Génération du menu pour {model.name}")
                menu_config = options.get('menu_config', {})
                menu_content = self.menu_builder.generate_menu(model, menu_config)
                menu_file = module_path / 'views' / f'{model_underscore}_menu.xml'
                
                with open(menu_file, 'w', encoding='utf-8') as f:
                    f.write(menu_content)
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération des fichiers pour {model.name}: {e}")
            raise

    def _generate_global_menu(self, models: List[ModelConfig], module_path: str, global_menu_config: Dict):
        """Génère un menu global pour plusieurs modèles"""
        try:
            self.logger.debug("Génération du menu global")
            
            global_menu_content = self.menu_builder.create_menu_structure(models, global_menu_config)
            global_menu_file = Path(module_path) / 'views' / 'menu_global.xml'
            
            with open(global_menu_file, 'w', encoding='utf-8') as f:
                f.write(global_menu_content)
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la génération du menu global: {e}")
            raise

    def _load_config_file(self, config_path: str) -> Dict:
        """Charge un fichier de configuration"""
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé: {config_path}")
        
        try:
            if path.suffix.lower() == '.json':
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            elif path.suffix.lower() in ['.yaml', '.yml']:
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            else:
                raise ValueError("Format de fichier non supporté. Utilisez JSON ou YAML.")
        except Exception as e:
            self.logger.error(f"Erreur lors du chargement du fichier de configuration: {e}")
            raise

    def create_config_template(self, template_type: str = 'basic', output_path: str = 'config.yaml') -> str:
        """
        Crée un template de configuration
        
        Args:
            template_type: Type de template (basic, crm, inventory, hr)
            output_path: Chemin de sortie du fichier de configuration
            
        Returns:
            Chemin vers le fichier créé
        """
        templates = {
            'basic': self._get_basic_template(),
            'crm': self._get_crm_template(),
            'inventory': self._get_inventory_template(),
            'hr': self._get_hr_template()
        }
        
        if template_type not in templates:
            raise ValueError(f"Template non supporté: {template_type}")
        
        config_content = templates[template_type]
        
        output_file = Path(output_path)
        
        if output_file.suffix.lower() == '.json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(config_content, f, indent=2, ensure_ascii=False)
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_content, f, default_flow_style=False, allow_unicode=True)
        
        self.logger.info(f"Template de configuration créé: {output_path}")
        return str(output_file)

    def _get_basic_template(self) -> Dict:
        """Template de configuration basique"""
        return {
            'module': {
                'name': 'Mon Module Personnalisé',
                'version': '17.0.1.0.0',
                'category': 'Custom',
                'description': 'Module généré automatiquement avec Odoo Model Generator',
                'author': 'Mon Entreprise',
                'depends': ['base', 'mail']
            },
            'models': [
                {
                    'name': 'x_my_model',
                    'description': 'Mon Modèle',
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'char',
                            'label': 'Nom',
                            'required': True,
                            'size': 100
                        },
                        {
                            'name': 'description',
                            'type': 'text',
                            'label': 'Description'
                        },
                        {
                            'name': 'date_creation',
                            'type': 'date',
                            'label': 'Date de Création',
                            'default': 'fields.Date.context_today'
                        }
                    ]
                }
            ]
        }

    def _get_crm_template(self) -> Dict:
        """Template pour module CRM"""
        return {
            'module': {
                'name': 'CRM Personnalisé',
                'category': 'Sales/CRM',
                'description': 'Module CRM avec fonctionnalités personnalisées',
                'depends': ['base', 'mail', 'crm']
            },
            'models': [
                {
                    'name': 'crm.lead.custom',
                    'description': 'Piste Personnalisée',
                    'inherit': ['crm.lead'],
                    'fields': [
                        {
                            'name': 'custom_source',
                            'type': 'selection',
                            'label': 'Source Personnalisée',
                            'selection': [
                                ['website', 'Site Web'],
                                ['social', 'Réseaux Sociaux'],
                                ['referral', 'Référence'],
                                ['other', 'Autre']
                            ]
                        },
                        {
                            'name': 'follow_up_date',
                            'type': 'date',
                            'label': 'Date de Relance'
                        }
                    ]
                }
            ]
        }

    def _get_inventory_template(self) -> Dict:
        """Template pour module de stock"""
        return {
            'module': {
                'name': 'Gestion de Stock Personnalisée',
                'category': 'Inventory/Inventory',
                'description': 'Module de gestion de stock avec fonctionnalités avancées',
                'depends': ['base', 'mail', 'stock']
            },
            'models': [
                {
                    'name': 'stock.custom.category',
                    'description': 'Catégorie Produit Personnalisée',
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'char',
                            'label': 'Nom de la Catégorie',
                            'required': True
                        },
                        {
                            'name': 'code',
                            'type': 'char',
                            'label': 'Code',
                            'size': 20
                        },
                        {
                            'name': 'description',
                            'type': 'text',
                            'label': 'Description'
                        }
                    ]
                }
            ]
        }

    def _get_hr_template(self) -> Dict:
        """Template pour module RH"""
        return {
            'module': {
                'name': 'Ressources Humaines Personnalisées',
                'category': 'Human Resources',
                'description': 'Module RH avec fonctionnalités étendues',
                'depends': ['base', 'mail', 'hr']
            },
            'models': [
                {
                    'name': 'hr.employee.skill',
                    'description': 'Compétence Employé',
                    'fields': [
                        {
                            'name': 'name',
                            'type': 'char',
                            'label': 'Nom de la Compétence',
                            'required': True
                        },
                        {
                            'name': 'employee_id',
                            'type': 'many2one',
                            'label': 'Employé',
                            'comodel_name': 'hr.employee',
                            'required': True
                        },
                        {
                            'name': 'level',
                            'type': 'selection',
                            'label': 'Niveau',
                            'selection': [
                                ['beginner', 'Débutant'],
                                ['intermediate', 'Intermédiaire'],
                                ['advanced', 'Avancé'],
                                ['expert', 'Expert']
                            ]
                        }
                    ]
                }
            ]
        }