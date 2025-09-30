#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration complète d'Odoo Model Generator
"""

import sys
import os
from pathlib import Path

# Ajouter le projet au PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from odoo_model_generator import OdooModelGenerator

def demo_complete():
    """Démonstration complète de la bibliothèque"""
    
    print("🎯 Démonstration d'Odoo Model Generator")
    print("=" * 50)
    
    # Configuration d'un module de gestion d'événements
    config_data = {
        'module': {
            'name': 'Gestion d\'Événements',
            'version': '17.0.1.0.0',
            'category': 'Events',
            'summary': 'Système de gestion d\'événements et inscriptions',
            'description': '''
Module complet de gestion d'événements avec:
- Création et gestion d'événements
- Système d'inscriptions
- Gestion des participants
- Suivi des paiements
- Rapports et analyses
            ''',
            'author': 'Demo Company',
            'website': 'https://demo-events.com',
            'depends': ['base', 'mail', 'website', 'payment']
        },
        'models': [
            # Modèle Événement
            {
                'name': 'event.custom',
                'description': 'Événement',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom de l\'Événement',
                        'required': True,
                        'size': 200
                    },
                    {
                        'name': 'description',
                        'type': 'html',
                        'label': 'Description'
                    },
                    {
                        'name': 'event_type',
                        'type': 'selection',
                        'label': 'Type d\'Événement',
                        'selection': [
                            ['conference', 'Conférence'],
                            ['workshop', 'Atelier'],
                            ['seminar', 'Séminaire'],
                            ['networking', 'Networking'],
                            ['training', 'Formation'],
                            ['other', 'Autre']
                        ],
                        'required': True
                    },
                    {
                        'name': 'start_date',
                        'type': 'datetime',
                        'label': 'Date de Début',
                        'required': True
                    },
                    {
                        'name': 'end_date',
                        'type': 'datetime',
                        'label': 'Date de Fin',
                        'required': True
                    },
                    {
                        'name': 'location',
                        'type': 'char',
                        'label': 'Lieu',
                        'size': 200
                    },
                    {
                        'name': 'max_participants',
                        'type': 'integer',
                        'label': 'Nombre Maximum de Participants',
                        'default': 50
                    },
                    {
                        'name': 'price',
                        'type': 'float',
                        'label': 'Prix d\'Inscription',
                        'default': 0.0
                    },
                    {
                        'name': 'organizer_id',
                        'type': 'many2one',
                        'label': 'Organisateur',
                        'comodel_name': 'res.users',
                        'required': True
                    },
                    {
                        'name': 'registration_ids',
                        'type': 'one2many',
                        'label': 'Inscriptions',
                        'comodel_name': 'event.registration',
                        'inverse_name': 'event_id'
                    },
                    {
                        'name': 'status',
                        'type': 'selection',
                        'label': 'Statut',
                        'selection': [
                            ['draft', 'Brouillon'],
                            ['published', 'Publié'],
                            ['ongoing', 'En Cours'],
                            ['done', 'Terminé'],
                            ['cancelled', 'Annulé']
                        ],
                        'default': 'draft'
                    },
                    {
                        'name': 'image',
                        'type': 'binary',
                        'label': 'Image de l\'Événement'
                    }
                ]
            },
            # Modèle Inscription
            {
                'name': 'event.registration',
                'description': 'Inscription à un Événement',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom du Participant',
                        'required': True,
                        'size': 150
                    },
                    {
                        'name': 'email',
                        'type': 'char',
                        'label': 'Email',
                        'required': True,
                        'size': 100
                    },
                    {
                        'name': 'phone',
                        'type': 'char',
                        'label': 'Téléphone',
                        'size': 20
                    },
                    {
                        'name': 'company',
                        'type': 'char',
                        'label': 'Entreprise',
                        'size': 100
                    },
                    {
                        'name': 'event_id',
                        'type': 'many2one',
                        'label': 'Événement',
                        'comodel_name': 'event.custom',
                        'required': True
                    },
                    {
                        'name': 'registration_date',
                        'type': 'datetime',
                        'label': 'Date d\'Inscription',
                        'default': 'fields.Datetime.now',
                        'readonly': True
                    },
                    {
                        'name': 'state',
                        'type': 'selection',
                        'label': 'État',
                        'selection': [
                            ['draft', 'Brouillon'],
                            ['confirmed', 'Confirmé'],
                            ['attended', 'Présent'],
                            ['cancelled', 'Annulé']
                        ],
                        'default': 'draft'
                    },
                    {
                        'name': 'payment_status',
                        'type': 'selection',
                        'label': 'Statut Paiement',
                        'selection': [
                            ['unpaid', 'Non Payé'],
                            ['partial', 'Partiel'],
                            ['paid', 'Payé'],
                            ['refunded', 'Remboursé']
                        ],
                        'default': 'unpaid'
                    },
                    {
                        'name': 'amount_paid',
                        'type': 'float',
                        'label': 'Montant Payé',
                        'default': 0.0
                    },
                    {
                        'name': 'notes',
                        'type': 'text',
                        'label': 'Notes'
                    }
                ]
            }
        ],
        'global_menu': {
            'root_menu_name': 'Gestion d\'Événements',
            'root_menu_id': 'event_management_root'
        }
    }
    
    try:
        # Génération du module
        print("🚀 Génération du module de gestion d'événements...")
        
        generator = OdooModelGenerator()
        module_path = generator.generate_module(
            config_data=config_data,
            output_path='./demo_output',
            module_name='event_management'
        )
        
        print(f"✅ Module généré avec succès!")
        print(f"📂 Emplacement: {module_path}")
        
        # Affichage des statistiques
        print(f"\n📊 Statistiques du module généré:")
        print(f"   • Nom: {config_data['module']['name']}")
        print(f"   • Modèles: {len(config_data['models'])}")
        print(f"   • Champs totaux: {sum(len(model['fields']) for model in config_data['models'])}")
        
        # Affichage de la structure
        print(f"\n📁 Structure du module:")
        _display_tree(module_path)
        
        # Instructions d'utilisation
        print(f"\n📖 Instructions d'utilisation:")
        print(f"1. Copiez le dossier 'event_management' dans votre répertoire d'addons Odoo")
        print(f"2. Redémarrez votre serveur Odoo")
        print(f"3. Activez le mode développeur dans Odoo")
        print(f"4. Allez dans Apps > Mettre à jour la liste des applications")
        print(f"5. Recherchez 'Gestion d'Événements' et installez le module")
        print(f"6. Utilisez le menu 'Gestion d'Événements' dans l'interface Odoo")
        
        print(f"\n🎉 Le module est prêt à être utilisé dans Odoo!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()
        return False

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
        
        print(f"{prefix}{current_prefix}{icon} {item.name}")
        
        if item.is_dir() and current_depth < max_depth - 1:
            extension = "    " if is_last else "│   "
            _display_tree(item, prefix + extension, max_depth, current_depth + 1)

if __name__ == '__main__':
    # Création du dossier de sortie pour la démo
    demo_output_dir = Path('./demo_output')
    demo_output_dir.mkdir(exist_ok=True)
    
    # Lancement de la démonstration
    success = demo_complete()
    
    if success:
        print(f"\n💡 Pour en savoir plus:")
        print(f"   • Consultez les exemples dans le dossier 'examples/'")
        print(f"   • Lisez la documentation dans README.md")
        print(f"   • Explorez les configurations dans 'examples/config_examples/'")
        print(f"   • Utilisez la CLI: omg --help")
    
    sys.exit(0 if success else 1)