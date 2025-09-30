#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple d'utilisation basique d'Odoo Model Generator

Cet exemple montre comment créer un module simple avec un modèle de produit personnalisé.
"""

from odoo_model_generator import OdooModelGenerator, FieldType, FieldConfig, ModelConfig, ModuleConfig

def create_basic_module():
    """Crée un module basique avec un modèle de produit"""
    
    # 1. Configuration des champs du modèle
    fields = [
        FieldConfig(
            name='name',
            field_type=FieldType.CHAR,
            label='Nom du Produit',
            required=True,
            size=200
        ),
        FieldConfig(
            name='code',
            field_type=FieldType.CHAR,
            label='Code Produit',
            required=True,
            size=50,
            help_text='Code unique du produit'
        ),
        FieldConfig(
            name='description',
            field_type=FieldType.TEXT,
            label='Description'
        ),
        FieldConfig(
            name='price',
            field_type=FieldType.FLOAT,
            label='Prix de Vente',
            required=True,
            default_value=0.0
        ),
        FieldConfig(
            name='cost_price',
            field_type=FieldType.FLOAT,
            label='Prix de Revient',
            default_value=0.0
        ),
        FieldConfig(
            name='category',
            field_type=FieldType.SELECTION,
            label='Catégorie',
            selection=[
                ('electronics', 'Électronique'),
                ('clothing', 'Vêtements'),
                ('books', 'Livres'),
                ('home', 'Maison'),
                ('other', 'Autre')
            ]
        ),
        FieldConfig(
            name='supplier_id',
            field_type=FieldType.MANY2ONE,
            label='Fournisseur',
            comodel_name='res.partner'
        ),
        FieldConfig(
            name='in_stock',
            field_type=FieldType.BOOLEAN,
            label='En Stock',
            default_value=True
        ),
        FieldConfig(
            name='image',
            field_type=FieldType.BINARY,
            label='Image du Produit'
        ),
        FieldConfig(
            name='launch_date',
            field_type=FieldType.DATE,
            label='Date de Lancement'
        )
    ]
    
    # 2. Configuration du modèle
    model = ModelConfig(
        name='product.custom',
        description='Produit Personnalisé',
        fields=fields,
        auto_create_views=True,
        auto_create_menu=True
    )
    
    # 3. Configuration du module
    module_config = ModuleConfig(
        name='Gestion de Produits Personnalisés',
        version='17.0.1.0.0',
        category='Sales',
        summary='Module de gestion de produits avec fonctionnalités étendues',
        description='Ce module permet de gérer des produits personnalisés avec des champs supplémentaires.',
        author='Mon Entreprise',
        website='https://monentreprise.com',
        depends=['base', 'mail', 'product']
    )
    
    # 4. Configuration globale
    config_data = {
        'module': {
            'name': module_config.name,
            'version': module_config.version,
            'category': module_config.category,
            'summary': module_config.summary,
            'description': module_config.description,
            'author': module_config.author,
            'website': module_config.website,
            'depends': module_config.depends
        },
        'models': [
            {
                'name': model.name,
                'description': model.description,
                'fields': [
                    {
                        'name': field.name,
                        'type': field.field_type.value,
                        'label': field.label,
                        'required': field.required,
                        'readonly': field.readonly,
                        'help_text': field.help_text,
                        'default': field.default_value,
                        **field.extra_attrs
                    }
                    for field in model.fields
                ]
            }
        ]
    }
    
    # 5. Génération du module
    generator = OdooModelGenerator()
    
    try:
        print("🚀 Génération du module en cours...")
        module_path = generator.generate_module(
            config_data=config_data,
            output_path='./output',
            module_name='product_management'
        )
        
        print(f"✅ Module généré avec succès!")
        print(f"📂 Emplacement: {module_path}")
        print(f"🎯 Modèle créé: {model.name}")
        print(f"🔧 Champs: {len(model.fields)} champs configurés")
        
        return module_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        return None

def create_config_file_example():
    """Crée un exemple de fichier de configuration"""
    
    config_data = {
        'module': {
            'name': 'Gestion de Produits Personnalisés',
            'version': '17.0.1.0.0',
            'category': 'Sales',
            'description': 'Module de gestion de produits avec fonctionnalités étendues',
            'author': 'Mon Entreprise',
            'depends': ['base', 'mail', 'product']
        },
        'models': [
            {
                'name': 'product.custom',
                'description': 'Produit Personnalisé',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom du Produit',
                        'required': True,
                        'size': 200
                    },
                    {
                        'name': 'code',
                        'type': 'char',
                        'label': 'Code Produit',
                        'required': True,
                        'size': 50
                    },
                    {
                        'name': 'price',
                        'type': 'float',
                        'label': 'Prix de Vente',
                        'required': True,
                        'default': 0.0
                    },
                    {
                        'name': 'category',
                        'type': 'selection',
                        'label': 'Catégorie',
                        'selection': [
                            ['electronics', 'Électronique'],
                            ['clothing', 'Vêtements'],
                            ['books', 'Livres']
                        ]
                    }
                ]
            }
        ]
    }
    
    import yaml
    with open('./examples/product_config.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    
    print("📄 Fichier de configuration créé: ./examples/product_config.yaml")

if __name__ == '__main__':
    print("🎯 Exemple d'utilisation d'Odoo Model Generator")
    print("=" * 50)
    
    # Création du module via code Python
    print("\n1. Création via code Python:")
    module_path = create_basic_module()
    
    # Création d'un fichier de configuration
    print("\n2. Création d'un fichier de configuration:")
    create_config_file_example()
    
    if module_path:
        print(f"\n📖 Instructions d'installation:")
        print(f"1. Copiez le dossier généré dans votre répertoire d'addons Odoo")
        print(f"2. Redémarrez le serveur Odoo")
        print(f"3. Activez le mode développeur")
        print(f"4. Allez dans Apps > Mettre à jour la liste")
        print(f"5. Recherchez 'product_management' et installez-le")
    
    print(f"\n💡 Pour utiliser le fichier de configuration:")
    print(f"   omg generate -c ./examples/product_config.yaml -n product_management")