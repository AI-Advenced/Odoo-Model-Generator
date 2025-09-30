# -*- coding: utf-8 -*-
"""
Générateur de menus et actions pour Odoo
"""

from jinja2 import Template
from typing import Dict, List, Optional
from ..config.field_types import ModelConfig

class MenuBuilder:
    """Construit les menus et actions XML pour Odoo"""
    
    def __init__(self):
        self.menu_template = Template('''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Action pour {{ model_name }} -->
        <record id="action_{{ model_name_underscore }}" model="ir.actions.act_window">
            <field name="name">{{ description }}</field>
            <field name="res_model">{{ model_name }}</field>
            <field name="view_mode">{{ view_mode }}</field>
            <field name="context">{{ context }}</field>
            <field name="domain">{{ domain }}</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Créer votre premier {{ description.lower() }}
                </p>
                <p>
                    Utilisez ce menu pour gérer vos {{ description.lower() }}s.
                    {% if help_description %}
                    {{ help_description }}
                    {% endif %}
                </p>
            </field>
            {% if limit %}
            <field name="limit">{{ limit }}</field>
            {% endif %}
            {% if view_ids %}
            <field name="view_ids" 
                   eval="[(5, 0, 0),
                          {% for view in view_ids %}
                          (0, 0, {'view_mode': '{{ view.mode }}', 'view_id': ref('{{ view.id }}')}),
                          {% endfor %}]"/>
            {% endif %}
        </record>

        {% if menu_root and not parent_menu %}
        <!-- Menu racine pour {{ model_name }} -->
        <menuitem id="menu_{{ model_name_underscore }}_root"
                  name="{{ menu_root.name }}"
                  sequence="{{ menu_root.sequence }}"
                  web_icon="{{ menu_root.icon }}"/>
        {% endif %}

        <!-- Menu principal pour {{ model_name }} -->
        <menuitem id="menu_{{ model_name_underscore }}"
                  name="{{ menu_name }}"
                  action="action_{{ model_name_underscore }}"
                  {% if parent_menu or menu_root %}parent="{% if menu_root and not parent_menu %}menu_{{ model_name_underscore }}_root{% else %}{{ parent_menu }}{% endif %}"{% endif %}
                  sequence="{{ sequence }}"
                  {% if groups %}groups="{{ groups }}"{% endif %}/>

        {% if submenu_items %}
        {% for submenu in submenu_items %}
        <!-- Sous-menu: {{ submenu.name }} -->
        <menuitem id="menu_{{ model_name_underscore }}_{{ submenu.id }}"
                  name="{{ submenu.name }}"
                  action="{{ submenu.action }}"
                  parent="menu_{{ model_name_underscore }}"
                  sequence="{{ submenu.sequence }}"
                  {% if submenu.groups %}groups="{{ submenu.groups }}"{% endif %}/>
        {% endfor %}
        {% endif %}

        {% if additional_actions %}
        {% for action in additional_actions %}
        <!-- Action supplémentaire: {{ action.name }} -->
        <record id="action_{{ model_name_underscore }}_{{ action.id }}" model="ir.actions.act_window">
            <field name="name">{{ action.name }}</field>
            <field name="res_model">{{ model_name }}</field>
            <field name="view_mode">{{ action.view_mode }}</field>
            <field name="context">{{ action.context }}</field>
            <field name="domain">{{ action.domain }}</field>
            {% if action.target %}
            <field name="target">{{ action.target }}</field>
            {% endif %}
        </record>
        {% endfor %}
        {% endif %}

        {% if server_actions %}
        {% for server_action in server_actions %}
        <!-- Action serveur: {{ server_action.name }} -->
        <record id="action_server_{{ model_name_underscore }}_{{ server_action.id }}" model="ir.actions.server">
            <field name="name">{{ server_action.name }}</field>
            <field name="model_id" ref="model_{{ model_name_underscore }}"/>
            <field name="binding_model_id" ref="model_{{ model_name_underscore }}"/>
            <field name="state">{{ server_action.state }}</field>
            <field name="code">{{ server_action.code }}</field>
        </record>
        {% endfor %}
        {% endif %}
    </data>
</odoo>''')

        self.action_template = Template('''
        <record id="action_{{ action_id }}" model="ir.actions.act_window">
            <field name="name">{{ name }}</field>
            <field name="res_model">{{ model_name }}</field>
            <field name="view_mode">{{ view_mode }}</field>
            <field name="context">{{ context }}</field>
            <field name="domain">{{ domain }}</field>
            {% if target %}
            <field name="target">{{ target }}</field>
            {% endif %}
            {% if help_text %}
            <field name="help" type="html">{{ help_text }}</field>
            {% endif %}
        </record>''')

    def generate_menu(self, config: ModelConfig, menu_config: Dict = None) -> str:
        """Génère les menus et actions pour un modèle"""
        model_name_underscore = config.name.replace('.', '_')
        menu_config = menu_config or {}
        
        # Configuration des vues
        view_mode = self._get_view_mode(config, menu_config)
        
        # Configuration du contexte et domaine
        context = menu_config.get('context', '{}')
        domain = menu_config.get('domain', '[]')
        
        # Configuration des vues spécifiques
        view_ids = self._generate_view_ids(config, menu_config)
        
        # Menu racine si nécessaire
        menu_root = None
        if menu_config.get('create_root_menu', False):
            menu_root = {
                'name': menu_config.get('root_menu_name', config.description),
                'sequence': menu_config.get('root_sequence', 10),
                'icon': menu_config.get('root_icon', 'fa fa-list')
            }
        
        # Sous-menus
        submenu_items = menu_config.get('submenu_items', [])
        
        # Actions supplémentaires
        additional_actions = self._generate_additional_actions(config, menu_config)
        
        # Actions serveur
        server_actions = self._generate_server_actions(config, menu_config)
        
        # Groupes de sécurité
        groups = ','.join(config.security_groups) if config.security_groups else None
        
        return self.menu_template.render(
            model_name=config.name,
            model_name_underscore=model_name_underscore,
            description=config.description,
            menu_name=menu_config.get('menu_name', config.description),
            view_mode=view_mode,
            context=context,
            domain=domain,
            help_description=menu_config.get('help_description'),
            limit=menu_config.get('limit'),
            view_ids=view_ids,
            menu_root=menu_root,
            parent_menu=config.menu_parent,
            sequence=menu_config.get('sequence', 10),
            groups=groups,
            submenu_items=submenu_items,
            additional_actions=additional_actions,
            server_actions=server_actions
        )

    def generate_dashboard_action(self, config: ModelConfig, dashboard_config: Dict = None) -> str:
        """Génère une action de tableau de bord"""
        dashboard_config = dashboard_config or {}
        model_name_underscore = config.name.replace('.', '_')
        
        # Configuration spéciale pour tableau de bord
        context = {
            'search_default_group_by_date': 1,
            'dashboard_mode': True
        }
        
        if dashboard_config.get('context'):
            context.update(dashboard_config['context'])
        
        return self.action_template.render(
            action_id=f"{model_name_underscore}_dashboard",
            name=f"Tableau de bord {config.description}",
            model_name=config.name,
            view_mode="graph,pivot,tree,form",
            context=str(context).replace("'", '"'),
            domain="[]",
            target=None,
            help_text=f"""
                <p class="o_view_nocontent_smiling_face">
                    Tableau de bord des {config.description.lower()}s
                </p>
                <p>
                    Visualisez les statistiques et analyses de vos {config.description.lower()}s.
                </p>
            """
        )

    def _get_view_mode(self, config: ModelConfig, menu_config: Dict) -> str:
        """Détermine le mode de vue par défaut"""
        default_views = ["tree", "form"]
        
        # Ajouter kanban si approprié
        if self._should_have_kanban_view(config):
            default_views.insert(0, "kanban")
        
        # Ajouter calendar si il y a des champs date
        if any(field.field_type.value in ['date', 'datetime'] for field in config.fields):
            default_views.append("calendar")
        
        # Personnalisation via config
        custom_views = menu_config.get('view_mode')
        if custom_views:
            return custom_views
        
        return ",".join(default_views)

    def _should_have_kanban_view(self, config: ModelConfig) -> bool:
        """Détermine si le modèle devrait avoir une vue kanban"""
        # Kanban approprié pour les modèles avec état/statut
        for field in config.fields:
            if field.field_type.value == 'selection' and 'state' in field.name.lower():
                return True
            if field.name in ['stage_id', 'status', 'state']:
                return True
        return False

    def _generate_view_ids(self, config: ModelConfig, menu_config: Dict) -> List[Dict]:
        """Génère la configuration des IDs de vues"""
        view_ids = []
        model_name_underscore = config.name.replace('.', '_')
        
        # Vues par défaut
        default_views = [
            {'mode': 'tree', 'id': f'view_{model_name_underscore}_tree'},
            {'mode': 'form', 'id': f'view_{model_name_underscore}_form'},
        ]
        
        # Ajouter d'autres vues si configurées
        if self._should_have_kanban_view(config):
            default_views.insert(0, {
                'mode': 'kanban', 
                'id': f'view_{model_name_underscore}_kanban'
            })
        
        # Personnalisation via config
        custom_view_ids = menu_config.get('view_ids')
        if custom_view_ids:
            return custom_view_ids
        
        return default_views

    def _generate_additional_actions(self, config: ModelConfig, menu_config: Dict) -> List[Dict]:
        """Génère des actions supplémentaires"""
        actions = []
        
        # Action pour les enregistrements actifs seulement
        if any(field.name == 'active' for field in config.fields):
            actions.append({
                'id': 'active_only',
                'name': f'{config.description} Actifs',
                'view_mode': 'tree,form',
                'context': '{}',
                'domain': "[('active', '=', True)]",
                'target': None
            })
        
        # Actions personnalisées via config
        custom_actions = menu_config.get('additional_actions', [])
        actions.extend(custom_actions)
        
        return actions

    def _generate_server_actions(self, config: ModelConfig, menu_config: Dict) -> List[Dict]:
        """Génère des actions serveur"""
        server_actions = []
        
        # Action d'archivage si le champ active existe
        if any(field.name == 'active' for field in config.fields):
            server_actions.append({
                'id': 'archive',
                'name': f'Archiver {config.description}',
                'state': 'code',
                'code': """
for record in records:
    record.active = False
"""
            })
            
            server_actions.append({
                'id': 'unarchive',
                'name': f'Désarchiver {config.description}',
                'state': 'code',
                'code': """
for record in records:
    record.active = True
"""
            })
        
        # Actions serveur personnalisées via config
        custom_server_actions = menu_config.get('server_actions', [])
        server_actions.extend(custom_server_actions)
        
        return server_actions

    def generate_report_action(self, config: ModelConfig, report_config: Dict) -> str:
        """Génère une action de rapport"""
        model_name_underscore = config.name.replace('.', '_')
        
        report_action = f"""
        <!-- Action Rapport pour {config.name} -->
        <record id="action_report_{model_name_underscore}" model="ir.actions.report">
            <field name="name">{report_config.get('name', f'Rapport {config.description}')}</field>
            <field name="model">{config.name}</field>
            <field name="report_type">qweb-pdf</field>
            <field name="report_name">{report_config.get('template_name', f'{config.name}.report_template')}</field>
            <field name="report_file">{report_config.get('filename', config.description.lower())}</field>
            <field name="binding_model_id" ref="model_{model_name_underscore}"/>
            <field name="binding_type">report</field>
        </record>
        """
        
        return report_action

    def create_menu_structure(self, models: List[ModelConfig], global_config: Dict = None) -> str:
        """Crée une structure de menu pour plusieurs modèles"""
        global_config = global_config or {}
        
        # Menu racine global
        root_menu_name = global_config.get('root_menu_name', 'Module Personnalisé')
        root_menu_id = global_config.get('root_menu_id', 'custom_module_root')
        
        menu_content = [f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Menu Racine Global -->
        <menuitem id="{root_menu_id}"
                  name="{root_menu_name}"
                  sequence="10"
                  web_icon="fa fa-star"/>
"""]
        
        # Menus pour chaque modèle
        for i, model in enumerate(models):
            model_menu_config = {
                'parent_menu': root_menu_id,
                'sequence': (i + 1) * 10
            }
            
            model_menu = self.generate_menu(model, model_menu_config)
            # Extraire seulement le contenu des menus (sans les balises XML racines)
            menu_data = model_menu.split('<data>')[1].split('</data>')[0].strip()
            menu_content.append(menu_data)
        
        menu_content.append("    </data>\n</odoo>")
        
        return '\n'.join(menu_content)