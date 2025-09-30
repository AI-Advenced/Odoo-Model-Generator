# -*- coding: utf-8 -*-
"""
Générateur de modules complets pour Odoo
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict
from jinja2 import Template
from ..config.field_types import ModelConfig, ModuleConfig

class ModuleBuilder:
    """Construit la structure complète d'un module Odoo"""
    
    def __init__(self):
        self.manifest_template = Template('''# -*- coding: utf-8 -*-
{
    'name': '{{ module_name }}',
    'version': '{{ version }}',
    'category': '{{ category }}',
    'summary': '{{ summary }}',
    'description': """
{{ description }}

Généré automatiquement par Odoo Model Generator.

Fonctionnalités:
{% for feature in features %}
- {{ feature }}
{% endfor %}

Modèles inclus:
{% for model in models %}
- {{ model.description }} ({{ model.name }})
{% endfor %}
    """,
    'author': '{{ author }}',
    'website': '{{ website }}',
    'depends': {{ depends }},
    'data': {{ data_files }},
    'demo': {{ demo_files }},
    'qweb': {{ qweb_files }},
    'external_dependencies': {
        'python': {{ python_deps }},
        'bin': {{ bin_deps }},
    },
    'installable': True,
    'auto_install': False,
    'application': {{ is_application }},
    'sequence': {{ sequence }},
    'license': '{{ license }}',
}''')

        self.init_template = Template('''# -*- coding: utf-8 -*-
"""
{{ module_name }}
{{ description }}

Généré automatiquement par Odoo Model Generator
"""

from . import models
{% if has_controllers %}from . import controllers{% endif %}
{% if has_wizards %}from . import wizards{% endif %}
{% if has_reports %}from . import reports{% endif %}''')

        self.models_init_template = Template('''# -*- coding: utf-8 -*-
"""
Modèles pour {{ module_name }}
"""

{% for model_file in model_files %}
from . import {{ model_file }}
{% endfor %}''')

        self.readme_template = Template('''# {{ module_name }}

## Description

{{ description }}

## Fonctionnalités

{% for feature in features %}
- {{ feature }}
{% endfor %}

## Modèles

{% for model in models %}
### {{ model.description }} (`{{ model.name }}`)

{{ model.description }}

**Champs:**
{% for field in model.fields %}
- `{{ field.name }}` ({{ field.field_type.value }}): {{ field.label }}
{% endfor %}

{% endfor %}

## Installation

1. Copiez ce module dans votre dossier d'addons Odoo
2. Redémarrez le serveur Odoo
3. Activez le mode développeur
4. Allez dans Apps > Mettre à jour la liste des applications
5. Recherchez "{{ module_name }}" et installez-le

## Configuration

Après installation, vous trouverez les nouveaux menus dans l'interface Odoo.

## Support

Ce module a été généré automatiquement avec Odoo Model Generator.
Pour des modifications, utilisez l'outil de génération ou modifiez le code manuellement.

## Licence

{{ license }}
''')

    def create_module_structure(self, 
                              output_path: str,
                              module_name: str,
                              models: List[ModelConfig],
                              module_config: ModuleConfig = None) -> str:
        """Crée la structure complète du module"""
        
        module_config = module_config or ModuleConfig(name=module_name)
        module_path = Path(output_path) / module_name
        
        # Création des dossiers
        self._create_directory_structure(module_path)
        
        # Génération des fichiers
        self._generate_manifest(module_path, module_name, models, module_config)
        self._generate_init_files(module_path, module_name, models)
        self._generate_security_files(module_path, models)
        self._generate_demo_data(module_path, models)
        self._copy_static_files(module_path, module_config)
        self._generate_readme(module_path, module_name, models, module_config)
        
        return str(module_path)

    def _create_directory_structure(self, module_path: Path):
        """Crée la structure de dossiers du module"""
        folders = [
            'models',
            'views', 
            'security',
            'data',
            'demo',
            'controllers',
            'wizards',
            'reports',
            'static/description',
            'static/src/js',
            'static/src/css',
            'static/src/xml',
            'static/src/img'
        ]
        
        for folder in folders:
            (module_path / folder).mkdir(parents=True, exist_ok=True)

    def _generate_manifest(self, module_path: Path, module_name: str, 
                          models: List[ModelConfig], config: ModuleConfig):
        """Génère le fichier __manifest__.py"""
        
        # Collecte des fichiers de données
        data_files = []
        
        # Fichiers de sécurité
        data_files.append("'security/ir.model.access.csv'")
        
        # Fichiers de vues pour chaque modèle
        for model in models:
            model_underscore = model.name.replace('.', '_')
            if model.auto_create_views:
                data_files.append(f"'views/{model_underscore}_views.xml'")
            if model.auto_create_menu:
                data_files.append(f"'views/{model_underscore}_menu.xml'")
        
        # Fichier de menu global s'il y a plusieurs modèles
        if len(models) > 1:
            data_files.append("'views/menu_global.xml'")
        
        # Données de démonstration
        demo_files = []
        for model in models:
            demo_files.append(f"'demo/{model.name.replace('.', '_')}_demo.xml'")
        
        # Fonctionnalités du module
        features = [f"Gestion des {model.description}" for model in models]
        
        manifest_content = self.manifest_template.render(
            module_name=config.name,
            version=config.version,
            category=config.category,
            summary=config.summary,
            description=config.description,
            author=config.author,
            website=config.website,
            depends=config.depends,
            data_files=data_files,
            demo_files=demo_files,
            qweb_files=[],
            python_deps=[],
            bin_deps=[],
            is_application=config.is_application,
            sequence=config.sequence,
            license=config.license,
            features=features,
            models=models
        )
        
        with open(module_path / '__manifest__.py', 'w', encoding='utf-8') as f:
            f.write(manifest_content)

    def _generate_init_files(self, module_path: Path, module_name: str, models: List[ModelConfig]):
        """Génère les fichiers __init__.py"""
        
        # __init__.py principal du module
        init_content = self.init_template.render(
            module_name=module_name,
            description=f'Module {module_name}',
            has_controllers=False,  # Peut être étendu plus tard
            has_wizards=False,
            has_reports=False
        )
        
        with open(module_path / '__init__.py', 'w', encoding='utf-8') as f:
            f.write(init_content)
        
        # models/__init__.py
        model_files = [model.name.replace('.', '_') for model in models]
        models_init_content = self.models_init_template.render(
            module_name=module_name,
            model_files=model_files
        )
        
        with open(module_path / 'models' / '__init__.py', 'w', encoding='utf-8') as f:
            f.write(models_init_content)
        
        # __init__.py vides pour les autres dossiers
        empty_dirs = ['controllers', 'wizards', 'reports']
        for dir_name in empty_dirs:
            init_file = module_path / dir_name / '__init__.py'
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write('# -*- coding: utf-8 -*-\n')

    def _generate_security_files(self, module_path: Path, models: List[ModelConfig]):
        """Génère les fichiers de sécurité"""
        
        # ir.model.access.csv
        access_content = ['id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n']
        
        for model in models:
            model_underscore = model.name.replace('.', '_')
            model_id = f'model_{model_underscore}'
            
            # Accès pour chaque groupe de sécurité
            for group in model.security_groups:
                group_suffix = group.split('.')[-1] if '.' in group else group
                access_id = f'access_{model_underscore}_{group_suffix}'
                
                # Permissions par défaut : lecture/écriture/création/suppression
                perms = '1,1,1,1'
                if 'user' in group_suffix.lower():
                    perms = '1,1,1,0'  # Pas de suppression pour les utilisateurs simples
                
                access_content.append(
                    f'{access_id},{model.description} {group_suffix.title()},'
                    f'{model_id},{group},{perms}\n'
                )
        
        with open(module_path / 'security' / 'ir.model.access.csv', 'w', encoding='utf-8') as f:
            f.writelines(access_content)

    def _generate_demo_data(self, module_path: Path, models: List[ModelConfig]):
        """Génère des données de démonstration"""
        
        for model in models:
            model_underscore = model.name.replace('.', '_')
            demo_file = module_path / 'demo' / f'{model_underscore}_demo.xml'
            
            demo_content = self._create_demo_records(model)
            
            with open(demo_file, 'w', encoding='utf-8') as f:
                f.write(demo_content)

    def _create_demo_records(self, model: ModelConfig) -> str:
        """Crée des enregistrements de démonstration pour un modèle"""
        model_underscore = model.name.replace('.', '_')
        
        demo_template = Template('''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- Données de démonstration pour {{ model_name }} -->
        {% for record in demo_records %}
        <record id="{{ model_underscore }}_demo_{{ loop.index }}" model="{{ model_name }}">
            {% for field, value in record.items() %}
            <field name="{{ field }}">{{ value }}</field>
            {% endfor %}
        </record>
        {% endfor %}
    </data>
</odoo>''')
        
        # Génération d'enregistrements de démonstration
        demo_records = []
        for i in range(3):  # 3 enregistrements de démo
            record = {}
            
            for field in model.fields:
                if field.name == 'active':
                    record[field.name] = True
                elif field.field_type.value == 'char':
                    if 'name' in field.name.lower():
                        record[field.name] = f"{model.description} Demo {i+1}"
                    elif 'email' in field.name.lower():
                        record[field.name] = f"demo{i+1}@example.com"
                    else:
                        record[field.name] = f"Valeur démo {i+1}"
                elif field.field_type.value == 'text':
                    record[field.name] = f"Description de démonstration pour l'enregistrement {i+1}"
                elif field.field_type.value == 'integer':
                    record[field.name] = (i + 1) * 10
                elif field.field_type.value == 'float':
                    record[field.name] = (i + 1) * 10.5
                elif field.field_type.value == 'boolean':
                    record[field.name] = i % 2 == 0
                elif field.field_type.value == 'selection' and field.extra_attrs.get('selection'):
                    selection = field.extra_attrs['selection']
                    if selection:
                        record[field.name] = selection[i % len(selection)][0]
        
            if record:  # Seulement si des champs ont été remplis
                demo_records.append(record)
        
        return demo_template.render(
            model_name=model.name,
            model_underscore=model_underscore,
            demo_records=demo_records
        )

    def _copy_static_files(self, module_path: Path, config: ModuleConfig):
        """Copie les fichiers statiques du module"""
        
        # Icône du module
        icon_path = getattr(config, 'icon_path', None)
        if icon_path and os.path.exists(icon_path):
            shutil.copy2(icon_path, module_path / 'static' / 'description' / 'icon.png')
        else:
            # Créer une icône par défaut
            self._create_default_icon(module_path / 'static' / 'description' / 'icon.png')
        
        # Description HTML du module
        self._create_module_description_html(module_path, config)
        
        # Fichier CSS personnalisé
        self._create_default_css(module_path / 'static' / 'src' / 'css' / 'module.css')
        
        # Fichier JS personnalisé
        self._create_default_js(module_path / 'static' / 'src' / 'js' / 'module.js')

    def _create_default_icon(self, icon_path: Path):
        """Crée une icône par défaut pour le module"""
        # SVG simple comme icône par défaut
        svg_content = '''<svg width="128" height="128" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
  <rect width="128" height="128" fill="#875A7B"/>
  <text x="64" y="74" font-family="Arial" font-size="48" fill="white" text-anchor="middle">M</text>
</svg>'''
        
        icon_path.parent.mkdir(parents=True, exist_ok=True)
        with open(icon_path.with_suffix('.svg'), 'w') as f:
            f.write(svg_content)

    def _create_module_description_html(self, module_path: Path, config: ModuleConfig):
        """Crée le fichier de description HTML du module"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{config.name}</title>
    <style>
        body {{ font-family: 'Lucida Grande', sans-serif; margin: 0; padding: 20px; }}
        .oe_container {{ max-width: 1200px; margin: 0 auto; }}
        .oe_row {{ display: flex; flex-wrap: wrap; margin: -15px; }}
        .oe_span12 {{ flex: 1; padding: 15px; }}
        .oe_slogan {{ font-size: 2.5em; color: #875A7B; margin-bottom: 0.5em; }}
        .oe_mt32 {{ margin-top: 32px; }}
        .oe_mb32 {{ margin-bottom: 32px; }}
        h2 {{ color: #333; }}
        ul {{ list-style-type: none; padding: 0; }}
        li {{ padding: 8px 0; }}
        li:before {{ content: "✓ "; color: #875A7B; font-weight: bold; }}
    </style>
</head>
<body>
    <section class="oe_container">
        <div class="oe_row oe_spaced">
            <div class="oe_span12">
                <h2 class="oe_slogan">{config.name}</h2>
                <p class="oe_mt32">
                    {config.description}
                </p>
            </div>
        </div>
    </section>
    
    <section class="oe_container oe_dark">
        <div class="oe_row">
            <div class="oe_span12">
                <h2>Fonctionnalités</h2>
                <ul>
                    <li>Interface intuitive et moderne</li>
                    <li>Gestion complète des données</li>
                    <li>Rapports et analyses</li>
                    <li>Compatible avec Odoo 17.0+</li>
                </ul>
            </div>
        </div>
    </section>
    
    <section class="oe_container">
        <div class="oe_row">
            <div class="oe_span12">
                <h2>Installation</h2>
                <p>
                    Ce module a été généré automatiquement avec Odoo Model Generator.
                    Installez-le comme n'importe quel module Odoo standard.
                </p>
            </div>
        </div>
    </section>
</body>
</html>
        """
        
        description_file = module_path / 'static' / 'description' / 'index.html'
        with open(description_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _create_default_css(self, css_path: Path):
        """Crée un fichier CSS par défaut"""
        css_content = '''/* Styles personnalisés pour le module */

.o_module_custom {
    /* Vos styles personnalisés ici */
}

.o_form_view .o_module_custom .oe_title h1 {
    color: #875A7B;
}

.o_kanban_view .o_module_custom {
    border-left: 3px solid #875A7B;
}
'''
        
        css_path.parent.mkdir(parents=True, exist_ok=True)
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)

    def _create_default_js(self, js_path: Path):
        """Crée un fichier JS par défaut"""
        js_content = '''odoo.define('module.custom', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');

// Votre code JavaScript personnalisé ici

return {
    // Exportez vos fonctions/classes ici
};

});
'''
        
        js_path.parent.mkdir(parents=True, exist_ok=True)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

    def _generate_readme(self, module_path: Path, module_name: str, 
                        models: List[ModelConfig], config: ModuleConfig):
        """Génère le fichier README.md du module"""
        
        features = [
            f"Gestion complète des {model.description.lower()}s" for model in models
        ]
        features.extend([
            "Interface utilisateur intuitive",
            "Vues multiples (liste, formulaire, kanban)",
            "Système de permissions granulaires",
            "Données de démonstration incluses"
        ])
        
        readme_content = self.readme_template.render(
            module_name=config.name,
            description=config.description,
            features=features,
            models=models,
            license=config.license
        )
        
        with open(module_path / 'README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)

    def create_module_package(self, module_path: str, output_file: str = None) -> str:
        """Crée un package tar.gz du module"""
        import tarfile
        
        module_path = Path(module_path)
        if not output_file:
            output_file = f"{module_path.name}.tar.gz"
        
        output_path = module_path.parent / output_file
        
        with tarfile.open(output_path, 'w:gz') as tar:
            tar.add(module_path, arcname=module_path.name)
        
        return str(output_path)

    def validate_module_structure(self, module_path: str) -> Dict[str, bool]:
        """Valide la structure d'un module généré"""
        module_path = Path(module_path)
        
        required_files = [
            '__manifest__.py',
            '__init__.py',
            'models/__init__.py',
            'security/ir.model.access.csv',
            'README.md'
        ]
        
        validation_result = {}
        
        for file_path in required_files:
            full_path = module_path / file_path
            validation_result[file_path] = full_path.exists()
        
        # Validation de la structure des dossiers
        required_dirs = ['models', 'views', 'security', 'static/description']
        for dir_path in required_dirs:
            full_path = module_path / dir_path
            validation_result[f"dir_{dir_path}"] = full_path.is_dir()
        
        return validation_result