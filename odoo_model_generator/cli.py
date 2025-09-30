# -*- coding: utf-8 -*-
"""
Interface en ligne de commande pour Odoo Model Generator
"""

import click
import json
import yaml
import sys
from pathlib import Path
from typing import Dict, List

from .core.generator import OdooModelGenerator
from .config.field_types import FieldType

@click.group()
@click.version_option(version='1.0.0', prog_name='Odoo Model Generator')
def cli():
    """🚀 Odoo Model Generator - Générateur automatique de modules Odoo
    
    Génère automatiquement des modules Odoo complets à partir de configurations YAML/JSON.
    """
    pass

@cli.command()
@click.option('--config', '-c', type=click.Path(exists=True), 
              help='Fichier de configuration (JSON ou YAML)')
@click.option('--output', '-o', type=click.Path(), default='./output',
              help='Dossier de sortie (défaut: ./output)')
@click.option('--module-name', '-n', 
              help='Nom du module à générer')
@click.option('--interactive', '-i', is_flag=True,
              help='Mode interactif pour configurer le module')
@click.option('--validate-only', is_flag=True,
              help='Valider seulement la configuration sans générer')
@click.option('--verbose', '-v', is_flag=True,
              help='Affichage détaillé')
def generate(config, output, module_name, interactive, validate_only, verbose):
    """Génère un module Odoo complet"""
    
    if verbose:
        click.echo("🔧 Mode détaillé activé")
    
    try:
        # Obtention de la configuration
        if interactive:
            click.echo("🎯 Mode interactif sélectionné")
            config_data = _interactive_config()
            if not module_name:
                module_name = config_data.get('module', {}).get('name', 'custom_module')
        elif config:
            click.echo(f"📄 Chargement de la configuration: {config}")
            config_data = _load_config_file(config)
            if not module_name:
                module_name = config_data.get('module', {}).get('name') or Path(config).stem
        else:
            click.echo("❌ Erreur: Fichier de configuration requis ou utilisez --interactive")
            click.echo("💡 Conseil: Utilisez 'omg init-config' pour créer un template")
            sys.exit(1)
        
        # Validation uniquement
        if validate_only:
            click.echo("🔍 Validation de la configuration...")
            generator = OdooModelGenerator()
            try:
                models = generator._parse_models_config(config_data.get('models', []))
                module_config = generator._parse_module_config(config_data.get('module', {}), module_name)
                generator._validate_configuration(models, module_config)
                click.echo("✅ Configuration valide!")
                return
            except Exception as e:
                click.echo(f"❌ Erreur de validation: {str(e)}")
                sys.exit(1)
        
        # Nettoyage du nom du module
        module_name = _clean_module_name(module_name)
        
        # Génération du module
        click.echo(f"🚀 Génération du module '{module_name}'...")
        click.echo(f"📁 Dossier de sortie: {output}")
        
        generator = OdooModelGenerator()
        
        with click.progressbar(length=100, label='Génération en cours') as bar:
            # Simulation de progression
            bar.update(20)
            module_path = generator.generate_module(
                config_data=config_data,
                output_path=output,
                module_name=module_name
            )
            bar.update(80)
        
        click.echo(f"✅ Module généré avec succès!")
        click.echo(f"📂 Emplacement: {module_path}")
        
        # Affichage de la structure
        if verbose:
            click.echo(f"\n📋 Structure créée:")
            _display_tree(module_path)
        
        # Instructions d'installation
        click.echo(f"\n📖 Instructions d'installation:")
        click.echo(f"1. Copiez le dossier '{module_name}' dans votre répertoire d'addons Odoo")
        click.echo(f"2. Redémarrez le serveur Odoo")
        click.echo(f"3. Activez le mode développeur")
        click.echo(f"4. Allez dans Apps > Mettre à jour la liste")
        click.echo(f"5. Recherchez '{module_name}' et installez-le")
        
    except Exception as e:
        click.echo(f"❌ Erreur lors de la génération: {str(e)}")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

@cli.command()
@click.option('--template', '-t', 
              type=click.Choice(['basic', 'crm', 'inventory', 'hr']),
              default='basic', help='Template de base (défaut: basic)')
@click.option('--output', '-o', type=click.Path(), default='./config.yaml',
              help='Fichier de configuration de sortie (défaut: ./config.yaml)')
@click.option('--format', '-f',
              type=click.Choice(['yaml', 'json']),
              help='Format du fichier (déduit de l\'extension par défaut)')
def init_config(template, output, format):
    """Initialise un fichier de configuration à partir d'un template
    
    Templates disponibles:
    - basic: Module basique avec modèle simple
    - crm: Module CRM avec pistes personnalisées  
    - inventory: Module de gestion des stocks
    - hr: Module de ressources humaines
    """
    
    try:
        click.echo(f"🎨 Création d'un template de configuration '{template}'")
        
        # Détermination du format
        output_path = Path(output)
        if not format:
            format = 'json' if output_path.suffix.lower() == '.json' else 'yaml'
        
        generator = OdooModelGenerator()
        config_file = generator.create_config_template(
            template_type=template,
            output_path=str(output_path.with_suffix(f'.{format}'))
        )
        
        click.echo(f"✅ Configuration initialisée: {config_file}")
        click.echo(f"📝 Format: {format.upper()}")
        click.echo(f"💡 Modifiez le fichier selon vos besoins, puis utilisez:")
        click.echo(f"   omg generate -c {config_file} -n mon_module")
        
    except Exception as e:
        click.echo(f"❌ Erreur lors de l'initialisation: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Affichage détaillé')
def validate(config_file, verbose):
    """Valide un fichier de configuration sans générer le module"""
    
    try:
        click.echo(f"🔍 Validation du fichier: {config_file}")
        
        generator = OdooModelGenerator()
        config_data = generator._load_config_file(config_file)
        
        # Parse et validation
        models = generator._parse_models_config(config_data.get('models', []))
        module_name = config_data.get('module', {}).get('name', 'test_module')
        module_config = generator._parse_module_config(config_data.get('module', {}), module_name)
        
        generator._validate_configuration(models, module_config)
        
        click.echo("✅ Configuration valide!")
        
        if verbose:
            click.echo(f"\n📊 Résumé de la configuration:")
            click.echo(f"   • Module: {module_config.name}")
            click.echo(f"   • Version: {module_config.version}")
            click.echo(f"   • Catégorie: {module_config.category}")
            click.echo(f"   • Modèles: {len(models)}")
            
            for model in models:
                click.echo(f"     - {model.name}: {len(model.fields)} champ(s)")
        
    except Exception as e:
        click.echo(f"❌ Erreur de validation: {str(e)}")
        sys.exit(1)

@cli.command()
def list_templates():
    """Liste les templates de configuration disponibles"""
    
    templates = {
        'basic': 'Module basique avec modèle simple',
        'crm': 'Module CRM avec pistes personnalisées',
        'inventory': 'Module de gestion des stocks', 
        'hr': 'Module de ressources humaines'
    }
    
    click.echo("📚 Templates de configuration disponibles:\n")
    
    for name, description in templates.items():
        click.echo(f"  🎯 {name:12} - {description}")
    
    click.echo(f"\n💡 Utilisez: omg init-config -t <template> pour créer une configuration")

@cli.command()
def list_fields():
    """Liste les types de champs Odoo supportés"""
    
    click.echo("📋 Types de champs Odoo supportés:\n")
    
    field_descriptions = {
        'char': 'Texte court (avec taille limitée)',
        'text': 'Texte long (multilignes)',
        'integer': 'Nombre entier',
        'float': 'Nombre décimal',
        'boolean': 'Case à cocher (True/False)',
        'date': 'Date (sans heure)',
        'datetime': 'Date et heure',
        'selection': 'Liste de choix prédéfinis',
        'many2one': 'Relation vers un autre modèle (N:1)',
        'one2many': 'Relation inverse (1:N)',
        'many2many': 'Relation multiple (N:N)',
        'binary': 'Fichier binaire (images, documents)',
        'html': 'Contenu HTML enrichi',
        'monetary': 'Montant monétaire (avec devise)'
    }
    
    for field_type in FieldType:
        description = field_descriptions.get(field_type.value, 'Type de champ Odoo')
        click.echo(f"  📄 {field_type.value:12} - {description}")
    
    click.echo(f"\n💡 Consultez la documentation Odoo pour plus de détails sur chaque type")

def _interactive_config() -> Dict:
    """Configuration interactive du module"""
    click.echo("\n🚀 Configuration Interactive du Module Odoo")
    click.echo("=" * 55)
    
    # Configuration du module
    click.echo("\n📦 Configuration du Module")
    module_name = click.prompt("Nom du module", type=str)
    module_description = click.prompt("Description du module", type=str)
    
    category = click.prompt("Catégorie", 
                           type=click.Choice(['Custom', 'Sales', 'Inventory', 'HR', 'Accounting']),
                           default='Custom')
    
    # Configuration des modèles
    models = []
    
    while True:
        click.echo(f"\n📋 Configuration du modèle #{len(models) + 1}")
        
        model_name = click.prompt("Nom du modèle (ex: res.partner, x_my_model)", type=str)
        model_desc = click.prompt("Description du modèle", type=str, default=model_name.replace('.', ' ').title())
        
        # Configuration des champs
        fields = []
        click.echo(f"\n🔧 Configuration des champs pour '{model_name}':")
        
        while True:
            field_name = click.prompt("\nNom du champ (ou 'done' pour terminer)", type=str)
            if field_name.lower() in ['done', 'fini', 'terminé']:
                break
                
            # Type de champ avec aide
            click.echo("Types disponibles: char, text, integer, float, boolean, date, datetime, selection, many2one, one2many, many2many, binary, html, monetary")
            field_type = click.prompt("Type de champ", 
                                    type=click.Choice([ft.value for ft in FieldType]))
            
            field_label = click.prompt("Label du champ", 
                                     default=field_name.replace('_', ' ').title())
            field_required = click.confirm("Champ requis?", default=False)
            
            field_config = {
                'name': field_name,
                'type': field_type,
                'label': field_label,
                'required': field_required
            }
            
            # Configuration spécifique selon le type
            if field_type == 'char':
                size = click.prompt("Taille maximale", type=int, default=255)
                field_config['size'] = size
            elif field_type == 'selection':
                click.echo("Entrez les choix (format: valeur|label, un par ligne, ligne vide pour terminer):")
                selection = []
                while True:
                    choice = click.prompt("Choix", type=str, default='')
                    if not choice:
                        break
                    if '|' in choice:
                        value, label = choice.split('|', 1)
                        selection.append([value.strip(), label.strip()])
                    else:
                        selection.append([choice, choice])
                field_config['selection'] = selection
            elif field_type in ['many2one', 'one2many', 'many2many']:
                comodel = click.prompt("Modèle lié (ex: res.partner)", type=str)
                field_config['comodel_name'] = comodel
            
            fields.append(field_config)
            click.echo(f"✅ Champ '{field_name}' ajouté")
        
        models.append({
            'name': model_name,
            'description': model_desc,
            'fields': fields
        })
        
        click.echo(f"✅ Modèle '{model_name}' configuré avec {len(fields)} champ(s)")
        
        if not click.confirm("\nAjouter un autre modèle?"):
            break
    
    return {
        'module': {
            'name': module_name,
            'description': module_description,
            'category': category
        },
        'models': models
    }

def _load_config_file(config_path: str) -> Dict:
    """Charge un fichier de configuration"""
    path = Path(config_path)
    
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
        raise Exception(f"Erreur lors du chargement de {config_path}: {e}")

def _clean_module_name(name: str) -> str:
    """Nettoie le nom du module pour Odoo"""
    # Remplace les espaces et caractères spéciaux par des underscores
    cleaned = ''.join(c if c.isalnum() else '_' for c in name.lower())
    # Supprime les underscores multiples
    while '__' in cleaned:
        cleaned = cleaned.replace('__', '_')
    # Supprime les underscores en début et fin
    return cleaned.strip('_')

def _display_tree(path: str, prefix: str = "", max_depth: int = 3, current_depth: int = 0):
    """Affiche l'arborescence des fichiers"""
    if current_depth >= max_depth:
        return
        
    path = Path(path)
    if not path.exists():
        return
    
    contents = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
    
    for i, item in enumerate(contents):
        if item.name.startswith('.'):
            continue
            
        is_last = i == len(contents) - 1
        current_prefix = "└── " if is_last else "├── "
        
        # Icônes selon le type de fichier
        if item.is_dir():
            icon = "📁"
        elif item.suffix == '.py':
            icon = "🐍"
        elif item.suffix in ['.xml', '.yml', '.yaml']:
            icon = "📄"
        elif item.suffix == '.csv':
            icon = "📊"
        elif item.name == 'README.md':
            icon = "📖"
        else:
            icon = "📄"
        
        click.echo(f"{prefix}{current_prefix}{icon} {item.name}")
        
        if item.is_dir() and current_depth < max_depth - 1:
            extension = "    " if is_last else "│   "
            _display_tree(item, prefix + extension, max_depth, current_depth + 1)

if __name__ == '__main__':
    cli()