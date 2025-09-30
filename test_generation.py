#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour valider la génération de modules Odoo
"""

import sys
import os
import traceback
from pathlib import Path

# Ajouter le dossier du projet au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from odoo_model_generator import OdooModelGenerator

def test_basic_generation():
    """Test de génération basique"""
    print("🧪 Test de génération basique...")
    
    # Configuration simple
    config_data = {
        'module': {
            'name': 'Test Module Basique',
            'version': '17.0.1.0.0',
            'category': 'Test',
            'description': 'Module de test généré automatiquement',
            'author': 'Test Author',
            'depends': ['base', 'mail']
        },
        'models': [
            {
                'name': 'test.product',
                'description': 'Produit de Test',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom du Produit',
                        'required': True,
                        'size': 100
                    },
                    {
                        'name': 'description',
                        'type': 'text',
                        'label': 'Description'
                    },
                    {
                        'name': 'price',
                        'type': 'float',
                        'label': 'Prix',
                        'required': True,
                        'default': 0.0
                    },
                    {
                        'name': 'active',
                        'type': 'boolean',
                        'label': 'Actif',
                        'default': True
                    }
                ]
            }
        ]
    }
    
    try:
        generator = OdooModelGenerator()
        module_path = generator.generate_module(
            config_data=config_data,
            output_path='./test_output',
            module_name='test_module_basic'
        )
        
        print(f"✅ Module généré avec succès: {module_path}")
        return True, module_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        traceback.print_exc()
        return False, None

def test_advanced_generation():
    """Test de génération avancée avec relations"""
    print("\n🧪 Test de génération avancée...")
    
    config_data = {
        'module': {
            'name': 'Test Module Avancé',
            'category': 'Test',
            'description': 'Module de test avec relations',
            'depends': ['base', 'mail']
        },
        'models': [
            {
                'name': 'test.category',
                'description': 'Catégorie de Test',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom',
                        'required': True
                    },
                    {
                        'name': 'code',
                        'type': 'char',
                        'label': 'Code',
                        'size': 10
                    }
                ]
            },
            {
                'name': 'test.advanced.product',
                'description': 'Produit Avancé',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom',
                        'required': True
                    },
                    {
                        'name': 'category_id',
                        'type': 'many2one',
                        'label': 'Catégorie',
                        'comodel_name': 'test.category',
                        'required': True
                    },
                    {
                        'name': 'tag_ids',
                        'type': 'many2many',
                        'label': 'Étiquettes',
                        'comodel_name': 'test.tag',
                        'relation': 'product_tag_rel',
                        'column1': 'product_id',
                        'column2': 'tag_id'
                    },
                    {
                        'name': 'status',
                        'type': 'selection',
                        'label': 'Statut',
                        'selection': [
                            ['draft', 'Brouillon'],
                            ['active', 'Actif'],
                            ['archived', 'Archivé']
                        ],
                        'default': 'draft'
                    }
                ]
            }
        ]
    }
    
    try:
        generator = OdooModelGenerator()
        module_path = generator.generate_module(
            config_data=config_data,
            output_path='./test_output',
            module_name='test_module_advanced'
        )
        
        print(f"✅ Module avancé généré avec succès: {module_path}")
        return True, module_path
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération avancée: {e}")
        traceback.print_exc()
        return False, None

def validate_generated_files(module_path):
    """Valide les fichiers générés"""
    print(f"\n🔍 Validation des fichiers générés dans {module_path}...")
    
    required_files = [
        '__manifest__.py',
        '__init__.py',
        'models/__init__.py',
        'security/ir.model.access.csv',
        'README.md'
    ]
    
    module_path = Path(module_path)
    validation_results = {}
    
    for file_path in required_files:
        full_path = module_path / file_path
        exists = full_path.exists()
        validation_results[file_path] = exists
        
        status = "✅" if exists else "❌"
        print(f"   {status} {file_path}")
        
        # Validation du contenu pour certains fichiers
        if exists and file_path == '__manifest__.py':
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "'name':" in content and "'version':" in content:
                        print(f"      ✅ Contenu du manifest valide")
                    else:
                        print(f"      ❌ Contenu du manifest invalide")
            except Exception as e:
                print(f"      ❌ Erreur de lecture: {e}")
    
    return validation_results

def test_cli_functionality():
    """Test des fonctionnalités CLI"""
    print(f"\n🧪 Test des fonctionnalités CLI...")
    
    try:
        # Test de création de template
        generator = OdooModelGenerator()
        config_path = generator.create_config_template(
            template_type='basic',
            output_path='./test_output/test_config.yaml'
        )
        
        print(f"✅ Template créé: {config_path}")
        
        # Test de génération depuis fichier
        module_path = generator.generate_from_file(
            config_file_path=config_path,
            output_path='./test_output',
            module_name='test_from_config'
        )
        
        print(f"✅ Module généré depuis config: {module_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test CLI: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Lance tous les tests"""
    print("🚀 Démarrage des tests de génération Odoo Model Generator")
    print("=" * 60)
    
    results = []
    
    # Test 1: Génération basique
    success, module_path = test_basic_generation()
    results.append(('Génération basique', success))
    
    if success and module_path:
        validate_generated_files(module_path)
    
    # Test 2: Génération avancée
    success, module_path = test_advanced_generation()
    results.append(('Génération avancée', success))
    
    if success and module_path:
        validate_generated_files(module_path)
    
    # Test 3: Fonctionnalités CLI
    success = test_cli_functionality()
    results.append(('Fonctionnalités CLI', success))
    
    # Résumé des résultats
    print(f"\n📊 Résumé des tests:")
    print("-" * 40)
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    for test_name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 Résultat global: {passed_tests}/{total_tests} tests réussis")
    
    if passed_tests == total_tests:
        print("🎉 Tous les tests sont passés avec succès!")
        print("🚀 La bibliothèque Odoo Model Generator est prête à l'utilisation!")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == '__main__':
    # Création du dossier de sortie
    test_output_dir = Path('./test_output')
    test_output_dir.mkdir(exist_ok=True)
    
    # Lancement des tests
    success = run_all_tests()
    
    # Code de sortie
    sys.exit(0 if success else 1)