#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemple avancé d'utilisation d'Odoo Model Generator

Cet exemple montre comment créer un module complexe avec plusieurs modèles liés
et des fonctionnalités avancées.
"""

from odoo_model_generator import OdooModelGenerator

def create_advanced_crm_module():
    """Crée un module CRM avancé avec plusieurs modèles liés"""
    
    config_data = {
        'module': {
            'name': 'CRM Avancé',
            'version': '17.0.1.0.0',
            'category': 'Sales/CRM',
            'summary': 'Module CRM avec gestion avancée des prospects et clients',
            'description': '''
Module CRM personnalisé avec fonctionnalités avancées:

• Gestion des prospects avec scoring
• Suivi des interactions client
• Gestion des campagnes marketing
• Rapports et analyses détaillées
• Intégration avec les réseaux sociaux
            ''',
            'author': 'CRM Solutions Inc.',
            'website': 'https://crm-solutions.com',
            'depends': ['base', 'mail', 'crm', 'sale', 'website']
        },
        'models': [
            # Modèle 1: Prospect avancé
            {
                'name': 'crm.prospect.advanced',
                'description': 'Prospect Avancé',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom Complet',
                        'required': True,
                        'size': 150
                    },
                    {
                        'name': 'company_name',
                        'type': 'char',
                        'label': 'Entreprise',
                        'size': 200
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
                        'name': 'source',
                        'type': 'selection',
                        'label': 'Source',
                        'selection': [
                            ['website', 'Site Web'],
                            ['social_media', 'Réseaux Sociaux'],
                            ['referral', 'Référence'],
                            ['cold_call', 'Appel à Froid'],
                            ['trade_show', 'Salon Professionnel'],
                            ['advertising', 'Publicité'],
                            ['other', 'Autre']
                        ],
                        'required': True
                    },
                    {
                        'name': 'status',
                        'type': 'selection',
                        'label': 'Statut',
                        'selection': [
                            ['new', 'Nouveau'],
                            ['contacted', 'Contacté'],
                            ['qualified', 'Qualifié'],
                            ['proposal', 'Devis Envoyé'],
                            ['negotiation', 'Négociation'],
                            ['won', 'Gagné'],
                            ['lost', 'Perdu']
                        ],
                        'default': 'new'
                    },
                    {
                        'name': 'score',
                        'type': 'integer',
                        'label': 'Score de Qualification',
                        'default': 0,
                        'help_text': 'Score de 0 à 100 basé sur les critères de qualification'
                    },
                    {
                        'name': 'expected_revenue',
                        'type': 'float',
                        'label': 'Chiffre d\'Affaires Estimé',
                        'default': 0.0
                    },
                    {
                        'name': 'probability',
                        'type': 'float',
                        'label': 'Probabilité (%)',
                        'default': 0.0
                    },
                    {
                        'name': 'interest_ids',
                        'type': 'many2many',
                        'label': 'Centres d\'Intérêt',
                        'comodel_name': 'crm.interest',
                        'relation': 'prospect_interest_rel',
                        'column1': 'prospect_id',
                        'column2': 'interest_id'
                    },
                    {
                        'name': 'interaction_ids',
                        'type': 'one2many',
                        'label': 'Interactions',
                        'comodel_name': 'crm.interaction',
                        'inverse_name': 'prospect_id'
                    },
                    {
                        'name': 'assigned_to',
                        'type': 'many2one',
                        'label': 'Assigné à',
                        'comodel_name': 'res.users'
                    },
                    {
                        'name': 'next_action_date',
                        'type': 'datetime',
                        'label': 'Prochaine Action'
                    },
                    {
                        'name': 'next_action_description',
                        'type': 'text',
                        'label': 'Description Prochaine Action'
                    },
                    {
                        'name': 'notes',
                        'type': 'html',
                        'label': 'Notes'
                    },
                    {
                        'name': 'avatar',
                        'type': 'binary',
                        'label': 'Photo'
                    }
                ]
            },
            # Modèle 2: Interactions client
            {
                'name': 'crm.interaction',
                'description': 'Interaction Client',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Sujet',
                        'required': True,
                        'size': 200
                    },
                    {
                        'name': 'prospect_id',
                        'type': 'many2one',
                        'label': 'Prospect',
                        'comodel_name': 'crm.prospect.advanced',
                        'required': True
                    },
                    {
                        'name': 'interaction_type',
                        'type': 'selection',
                        'label': 'Type d\'Interaction',
                        'selection': [
                            ['call', 'Appel Téléphonique'],
                            ['email', 'Email'],
                            ['meeting', 'Rendez-vous'],
                            ['demo', 'Démonstration'],
                            ['proposal', 'Présentation'],
                            ['social', 'Réseaux Sociaux'],
                            ['other', 'Autre']
                        ],
                        'required': True
                    },
                    {
                        'name': 'date',
                        'type': 'datetime',
                        'label': 'Date et Heure',
                        'required': True,
                        'default': 'fields.Datetime.now'
                    },
                    {
                        'name': 'duration',
                        'type': 'float',
                        'label': 'Durée (minutes)',
                        'default': 0.0
                    },
                    {
                        'name': 'description',
                        'type': 'html',
                        'label': 'Description'
                    },
                    {
                        'name': 'outcome',
                        'type': 'selection',
                        'label': 'Résultat',
                        'selection': [
                            ['positive', 'Positif'],
                            ['neutral', 'Neutre'],
                            ['negative', 'Négatif'],
                            ['no_response', 'Pas de Réponse']
                        ]
                    },
                    {
                        'name': 'follow_up_required',
                        'type': 'boolean',
                        'label': 'Suivi Requis',
                        'default': False
                    },
                    {
                        'name': 'follow_up_date',
                        'type': 'datetime',
                        'label': 'Date de Suivi'
                    },
                    {
                        'name': 'user_id',
                        'type': 'many2one',
                        'label': 'Responsable',
                        'comodel_name': 'res.users',
                        'default': 'lambda self: self.env.user'
                    }
                ]
            },
            # Modèle 3: Centres d'intérêt
            {
                'name': 'crm.interest',
                'description': 'Centre d\'Intérêt',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom',
                        'required': True,
                        'size': 100
                    },
                    {
                        'name': 'category',
                        'type': 'selection',
                        'label': 'Catégorie',
                        'selection': [
                            ['product', 'Produit'],
                            ['service', 'Service'],
                            ['industry', 'Secteur'],
                            ['technology', 'Technologie'],
                            ['other', 'Autre']
                        ]
                    },
                    {
                        'name': 'description',
                        'type': 'text',
                        'label': 'Description'
                    },
                    {
                        'name': 'color',
                        'type': 'integer',
                        'label': 'Couleur',
                        'help_text': 'Couleur pour l\'affichage dans l\'interface'
                    }
                ]
            },
            # Modèle 4: Campagne marketing
            {
                'name': 'crm.campaign',
                'description': 'Campagne Marketing',
                'fields': [
                    {
                        'name': 'name',
                        'type': 'char',
                        'label': 'Nom de la Campagne',
                        'required': True,
                        'size': 150
                    },
                    {
                        'name': 'campaign_type',
                        'type': 'selection',
                        'label': 'Type de Campagne',
                        'selection': [
                            ['email', 'Email Marketing'],
                            ['social', 'Réseaux Sociaux'],
                            ['advertising', 'Publicité'],
                            ['event', 'Événement'],
                            ['webinar', 'Webinaire'],
                            ['content', 'Marketing de Contenu']
                        ],
                        'required': True
                    },
                    {
                        'name': 'start_date',
                        'type': 'date',
                        'label': 'Date de Début',
                        'required': True
                    },
                    {
                        'name': 'end_date',
                        'type': 'date',
                        'label': 'Date de Fin'
                    },
                    {
                        'name': 'budget',
                        'type': 'float',
                        'label': 'Budget',
                        'default': 0.0
                    },
                    {
                        'name': 'target_audience',
                        'type': 'text',
                        'label': 'Audience Cible'
                    },
                    {
                        'name': 'objectives',
                        'type': 'html',
                        'label': 'Objectifs'
                    },
                    {
                        'name': 'status',
                        'type': 'selection',
                        'label': 'Statut',
                        'selection': [
                            ['draft', 'Brouillon'],
                            ['planned', 'Planifiée'],
                            ['running', 'En Cours'],
                            ['completed', 'Terminée'],
                            ['cancelled', 'Annulée']
                        ],
                        'default': 'draft'
                    },
                    {
                        'name': 'leads_generated',
                        'type': 'integer',
                        'label': 'Prospects Générés',
                        'readonly': True,
                        'default': 0
                    },
                    {
                        'name': 'conversion_rate',
                        'type': 'float',
                        'label': 'Taux de Conversion (%)',
                        'readonly': True,
                        'default': 0.0
                    },
                    {
                        'name': 'roi',
                        'type': 'float',
                        'label': 'ROI (%)',
                        'readonly': True,
                        'default': 0.0
                    }
                ]
            }
        ],
        'global_menu': {
            'root_menu_name': 'CRM Avancé',
            'root_menu_id': 'crm_advanced_root'
        }
    }
    
    return config_data

def create_library_management_module():
    """Crée un module de gestion de bibliothèque"""
    
    config_data = {
        'module': {
            'name': 'Gestion de Bibliothèque',
            'version': '17.0.1.0.0',
            'category': 'Education',
            'summary': 'Système complet de gestion de bibliothèque',
            'description': '''
Module de gestion de bibliothèque avec:

• Catalogue de livres et ressources
• Gestion des membres et abonnements  
• Système d'emprunts et retours
• Réservations et listes d'attente
• Gestion des amendes et pénalités
• Rapports et statistiques
            ''',
            'author': 'Library Solutions',
            'depends': ['base', 'mail']
        },
        'models': [
            {
                'name': 'library.book',
                'description': 'Livre',
                'fields': [
                    {'name': 'title', 'type': 'char', 'label': 'Titre', 'required': True, 'size': 200},
                    {'name': 'isbn', 'type': 'char', 'label': 'ISBN', 'size': 20},
                    {'name': 'author_ids', 'type': 'many2many', 'label': 'Auteurs', 
                     'comodel_name': 'library.author'},
                    {'name': 'category_id', 'type': 'many2one', 'label': 'Catégorie',
                     'comodel_name': 'library.category'},
                    {'name': 'publisher', 'type': 'char', 'label': 'Éditeur', 'size': 100},
                    {'name': 'publication_date', 'type': 'date', 'label': 'Date de Publication'},
                    {'name': 'pages', 'type': 'integer', 'label': 'Nombre de Pages'},
                    {'name': 'language', 'type': 'selection', 'label': 'Langue',
                     'selection': [['fr', 'Français'], ['en', 'Anglais'], ['es', 'Espagnol']]},
                    {'name': 'summary', 'type': 'text', 'label': 'Résumé'},
                    {'name': 'cover_image', 'type': 'binary', 'label': 'Image de Couverture'},
                    {'name': 'available_copies', 'type': 'integer', 'label': 'Exemplaires Disponibles'},
                    {'name': 'total_copies', 'type': 'integer', 'label': 'Total Exemplaires'}
                ]
            },
            {
                'name': 'library.member',
                'description': 'Membre',
                'fields': [
                    {'name': 'name', 'type': 'char', 'label': 'Nom Complet', 'required': True},
                    {'name': 'member_id', 'type': 'char', 'label': 'N° Membre', 'required': True},
                    {'name': 'email', 'type': 'char', 'label': 'Email'},
                    {'name': 'phone', 'type': 'char', 'label': 'Téléphone'},
                    {'name': 'address', 'type': 'text', 'label': 'Adresse'},
                    {'name': 'membership_date', 'type': 'date', 'label': 'Date d\'Adhésion'},
                    {'name': 'expiry_date', 'type': 'date', 'label': 'Date d\'Expiration'},
                    {'name': 'member_type', 'type': 'selection', 'label': 'Type de Membre',
                     'selection': [['student', 'Étudiant'], ['teacher', 'Enseignant'], ['public', 'Grand Public']]},
                    {'name': 'status', 'type': 'selection', 'label': 'Statut',
                     'selection': [['active', 'Actif'], ['suspended', 'Suspendu'], ['expired', 'Expiré']]}
                ]
            }
        ]
    }
    
    return config_data

def generate_multiple_modules():
    """Génère plusieurs modules d'exemple"""
    
    generator = OdooModelGenerator()
    
    modules = [
        ('CRM Avancé', create_advanced_crm_module(), 'crm_advanced'),
        ('Gestion de Bibliothèque', create_library_management_module(), 'library_management')
    ]
    
    results = []
    
    for module_title, config_data, module_name in modules:
        try:
            print(f"🚀 Génération du module '{module_title}'...")
            
            module_path = generator.generate_module(
                config_data=config_data,
                output_path='./output',
                module_name=module_name
            )
            
            results.append({
                'title': module_title,
                'path': module_path,
                'name': module_name,
                'models': len(config_data['models']),
                'success': True
            })
            
            print(f"✅ Module '{module_title}' généré avec succès!")
            print(f"   📂 Chemin: {module_path}")
            print(f"   🎯 Modèles: {len(config_data['models'])}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération de '{module_title}': {e}")
            results.append({
                'title': module_title,
                'name': module_name,
                'success': False,
                'error': str(e)
            })
    
    return results

if __name__ == '__main__':
    print("🎯 Exemples avancés d'Odoo Model Generator")
    print("=" * 55)
    
    # Génération de plusieurs modules
    print("Génération de modules d'exemple avancés...\n")
    
    results = generate_multiple_modules()
    
    # Résumé des résultats
    print(f"\n📊 Résumé de la génération:")
    print("-" * 40)
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"✅ Modules générés avec succès: {len(successful)}")
    for result in successful:
        print(f"   • {result['title']} ({result['models']} modèles)")
    
    if failed:
        print(f"❌ Modules échoués: {len(failed)}")
        for result in failed:
            print(f"   • {result['title']}: {result['error']}")
    
    if successful:
        print(f"\n📖 Instructions d'installation:")
        print(f"1. Copiez les dossiers générés dans votre répertoire d'addons Odoo")
        print(f"2. Redémarrez le serveur Odoo")
        print(f"3. Activez le mode développeur")  
        print(f"4. Allez dans Apps > Mettre à jour la liste")
        print(f"5. Recherchez et installez les modules générés")
    
    print(f"\n💡 Ces exemples montrent les capacités avancées du générateur:")
    print(f"   • Modèles avec relations complexes")
    print(f"   • Champs calculés et contraintes")
    print(f"   • Vues personnalisées")
    print(f"   • Menus structurés")
    print(f"   • Données de démonstration")