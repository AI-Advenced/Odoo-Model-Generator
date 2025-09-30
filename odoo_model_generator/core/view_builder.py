# -*- coding: utf-8 -*-
"""
Générateur de vues XML pour Odoo
"""

from jinja2 import Template
from typing import List, Dict
from ..config.field_types import ModelConfig, FieldConfig, FieldType

class ViewBuilder:
    """Construit les vues XML pour Odoo"""
    
    def __init__(self):
        self.form_template = Template('''
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Vue Formulaire pour {{ model_name }} -->
        <record id="view_{{ model_name_underscore }}_form" model="ir.ui.view">
            <field name="name">{{ description }} - Formulaire</field>
            <field name="model">{{ model_name }}</field>
            <field name="arch" type="xml">
                <form string="{{ description }}">
                    <header>
                        <!-- Boutons d'action -->
                        {% if has_active_field %}
                        <button name="toggle_active" type="object" 
                                string="Basculer Actif/Inactif" 
                                class="btn-secondary"/>
                        {% endif %}
                    </header>
                    <sheet>
                        <div class="oe_button_box" name="button_box">
                            {% for stat_button in stat_buttons %}
                            <button class="oe_stat_button" type="object" 
                                    name="action_view_{{ stat_button.field }}" 
                                    icon="fa-{{ stat_button.icon }}">
                                <field string="{{ stat_button.label }}" 
                                       name="{{ stat_button.field }}_count" 
                                       widget="statinfo"/>
                            </button>
                            {% endfor %}
                        </div>
                        
                        {% if has_image_field %}
                        <field name="{{ image_field_name }}" widget="image" 
                               class="oe_avatar" 
                               options="{'preview_image': '{{ image_field_name }}', 'size': [90, 90]}"/>
                        {% endif %}
                        
                        <div class="oe_title">
                            {% if title_field %}
                            <h1>
                                <field name="{{ title_field.name }}" 
                                       placeholder="{{ title_field.label }}"/>
                            </h1>
                            {% endif %}
                        </div>
                        
                        <group>
                            {% for section in form_sections %}
                            <group string="{{ section.title }}" col="{{ section.cols }}">
                                {% for field in section.fields %}
                                <field name="{{ field.name }}"{% if field.attrs %} {{ field.attrs }}{% endif %}/>
                                {% endfor %}
                            </group>
                            {% endfor %}
                        </group>
                        
                        {% if notebook_pages %}
                        <notebook>
                            {% for page in notebook_pages %}
                            <page string="{{ page.title }}">
                                {% if page.fields %}
                                <group>
                                    {% for field in page.fields %}
                                    <field name="{{ field.name }}"{% if field.attrs %} {{ field.attrs }}{% endif %}/>
                                    {% endfor %}
                                </group>
                                {% endif %}
                            </page>
                            {% endfor %}
                        </notebook>
                        {% endif %}
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>
    </data>
</odoo>''')

        self.tree_template = Template('''
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Vue Liste pour {{ model_name }} -->
        <record id="view_{{ model_name_underscore }}_tree" model="ir.ui.view">
            <field name="name">{{ description }} - Liste</field>
            <field name="model">{{ model_name }}</field>
            <field name="arch" type="xml">
                <tree string="{{ description }}"{% if editable %} editable="{{ editable }}"{% endif %}{% if decoration %} {{ decoration }}{% endif %}>
                    {% for field in tree_fields %}
                    <field name="{{ field.name }}"{% if field.attrs %} {{ field.attrs }}{% endif %}/>
                    {% endfor %}
                </tree>
            </field>
        </record>
    </data>
</odoo>''')

        self.search_template = Template('''
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Vue Recherche pour {{ model_name }} -->
        <record id="view_{{ model_name_underscore }}_search" model="ir.ui.view">
            <field name="name">{{ description }} - Recherche</field>
            <field name="model">{{ model_name }}</field>
            <field name="arch" type="xml">
                <search string="Rechercher {{ description }}">
                    <!-- Champs de recherche -->
                    {% for field in search_fields %}
                    <field name="{{ field.name }}"{% if field.attrs %} {{ field.attrs }}{% endif %}/>
                    {% endfor %}
                    
                    <!-- Filtres prédéfinis -->
                    <separator/>
                    {% for filter in filters %}
                    <filter string="{{ filter.label }}" 
                            name="{{ filter.name }}" 
                            domain="{{ filter.domain }}"/>
                    {% endfor %}
                    
                    <!-- Groupements -->
                    <separator/>
                    <filter string="Grouper par {{ group_by_label }}" 
                            name="group_by_{{ group_by_field }}" 
                            context="{'group_by':'{{ group_by_field }}'}"/>
                </search>
            </field>
        </record>
    </data>
</odoo>''')

        self.kanban_template = Template('''
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- Vue Kanban pour {{ model_name }} -->
        <record id="view_{{ model_name_underscore }}_kanban" model="ir.ui.view">
            <field name="name">{{ description }} - Kanban</field>
            <field name="model">{{ model_name }}</field>
            <field name="arch" type="xml">
                <kanban>
                    <templates>
                        <t t-name="kanban-box">
                            <div class="oe_kanban_card oe_kanban_global_click">
                                <div class="oe_kanban_content">
                                    <div class="o_kanban_record_top">
                                        <div class="o_kanban_record_headings">
                                            <strong class="o_kanban_record_title">
                                                <field name="{{ title_field }}"/>
                                            </strong>
                                        </div>
                                    </div>
                                    {% for field in kanban_fields %}
                                    <div class="o_kanban_record_body">
                                        <field name="{{ field.name }}"/>
                                    </div>
                                    {% endfor %}
                                </div>
                            </div>
                        </t>
                    </templates>
                </kanban>
            </field>
        </record>
    </data>
</odoo>''')

    def generate_form_view(self, config: ModelConfig) -> str:
        """Génère la vue formulaire"""
        model_name_underscore = config.name.replace('.', '_')
        
        # Organisation des champs en sections
        basic_fields = []
        detail_fields = []
        relation_fields = []
        
        # Détection des champs spéciaux
        title_field = None
        image_field_name = None
        has_active_field = False
        
        for field in config.fields:
            field_data = {
                'name': field.name,
                'attrs': self._get_field_attrs(field, view_type='form')
            }
            
            # Identification des champs spéciaux
            if field.name in ['name', 'title'] and not title_field:
                title_field = field
                continue
            elif field.field_type == FieldType.BINARY and 'image' in field.name.lower():
                image_field_name = field.name
                continue
            elif field.name == 'active':
                has_active_field = True
                continue
            
            # Classification des champs
            if field.field_type in [FieldType.CHAR, FieldType.INTEGER, FieldType.FLOAT, 
                                  FieldType.BOOLEAN, FieldType.SELECTION]:
                basic_fields.append(field_data)
            elif field.field_type in [FieldType.TEXT, FieldType.HTML, FieldType.DATE, 
                                    FieldType.DATETIME, FieldType.MONETARY]:
                detail_fields.append(field_data)
            else:
                relation_fields.append(field_data)
        
        # Sections du formulaire
        form_sections = []
        if basic_fields:
            form_sections.append({
                'title': 'Informations Générales', 
                'cols': 2, 
                'fields': basic_fields
            })
        
        # Pages du notebook
        notebook_pages = []
        if detail_fields:
            notebook_pages.append({'title': 'Détails', 'fields': detail_fields})
        if relation_fields:
            notebook_pages.append({'title': 'Relations', 'fields': relation_fields})
        
        # Boutons statistiques pour les champs One2many
        stat_buttons = []
        for field in config.fields:
            if field.field_type == FieldType.ONE2MANY:
                stat_buttons.append({
                    'field': field.name,
                    'label': field.label,
                    'icon': 'list-ul'
                })
        
        return self.form_template.render(
            model_name=config.name,
            model_name_underscore=model_name_underscore,
            description=config.description,
            form_sections=form_sections,
            notebook_pages=notebook_pages,
            title_field=title_field,
            has_image_field=bool(image_field_name),
            image_field_name=image_field_name,
            has_active_field=has_active_field,
            stat_buttons=stat_buttons
        )

    def generate_tree_view(self, config: ModelConfig) -> str:
        """Génère la vue liste"""
        model_name_underscore = config.name.replace('.', '_')
        
        # Sélection des champs pour la vue liste
        tree_fields = []
        field_count = 0
        
        for field in config.fields:
            if field_count >= 8:  # Limite de champs dans la liste
                break
                
            if field.field_type not in [FieldType.TEXT, FieldType.HTML, FieldType.ONE2MANY]:
                tree_fields.append({
                    'name': field.name,
                    'attrs': self._get_field_attrs(field, view_type='tree')
                })
                field_count += 1
        
        # Décoration pour les champs actifs
        decoration = ""
        if any(field.name == 'active' for field in config.fields):
            decoration = 'decoration-muted="not active"'
        
        return self.tree_template.render(
            model_name=config.name,
            model_name_underscore=model_name_underscore,
            description=config.description,
            tree_fields=tree_fields,
            editable=None,
            decoration=decoration
        )

    def generate_search_view(self, config: ModelConfig) -> str:
        """Génère la vue de recherche"""
        model_name_underscore = config.name.replace('.', '_')
        
        # Champs de recherche (texte et sélection principalement)
        search_fields = []
        for field in config.fields:
            if field.field_type in [FieldType.CHAR, FieldType.TEXT, FieldType.SELECTION, 
                                  FieldType.MANY2ONE]:
                search_fields.append({
                    'name': field.name,
                    'attrs': ''
                })
        
        # Filtres prédéfinis
        filters = []
        if any(field.name == 'active' for field in config.fields):
            filters.extend([
                {'name': 'active', 'label': 'Actifs', 'domain': "[('active', '=', True)]"},
                {'name': 'inactive', 'label': 'Inactifs', 'domain': "[('active', '=', False)]"}
            ])
        
        # Champ de groupement par défaut
        group_by_field = 'create_date'
        group_by_label = 'Date de création'
        
        for field in config.fields:
            if field.field_type in [FieldType.SELECTION, FieldType.MANY2ONE]:
                group_by_field = field.name
                group_by_label = field.label
                break
        
        return self.search_template.render(
            model_name=config.name,
            model_name_underscore=model_name_underscore,
            description=config.description,
            search_fields=search_fields,
            filters=filters,
            group_by_field=group_by_field,
            group_by_label=group_by_label
        )

    def generate_kanban_view(self, config: ModelConfig) -> str:
        """Génère la vue kanban"""
        model_name_underscore = config.name.replace('.', '_')
        
        # Champ titre pour le kanban
        title_field = 'id'
        for field in config.fields:
            if field.name in ['name', 'title'] or field.field_type == FieldType.CHAR:
                title_field = field.name
                break
        
        # Autres champs à afficher
        kanban_fields = []
        for field in config.fields[:3]:  # Limite à 3 champs
            if field.name != title_field and field.field_type not in [FieldType.TEXT, FieldType.HTML]:
                kanban_fields.append({
                    'name': field.name
                })
        
        return self.kanban_template.render(
            model_name=config.name,
            model_name_underscore=model_name_underscore,
            description=config.description,
            title_field=title_field,
            kanban_fields=kanban_fields
        )

    def _get_field_attrs(self, field: FieldConfig, view_type: str = 'form') -> str:
        """Génère les attributs XML pour un champ"""
        attrs = []
        
        if field.required and view_type == 'form':
            attrs.append('required="1"')
        if field.readonly:
            attrs.append('readonly="1"')
            
        # Widgets spécifiques
        if field.field_type == FieldType.HTML:
            attrs.append('widget="html"')
        elif field.field_type == FieldType.MONETARY:
            attrs.append('widget="monetary"')
        elif field.field_type == FieldType.BINARY:
            if 'image' in field.name.lower():
                attrs.append('widget="image"')
            else:
                attrs.append('widget="binary"')
        elif field.field_type == FieldType.BOOLEAN and view_type == 'tree':
            attrs.append('widget="boolean_toggle"')
        elif field.field_type == FieldType.MANY2MANY and view_type == 'form':
            attrs.append('widget="many2many_tags"')
        
        # Attributs de vue spécifiques
        if view_type == 'tree':
            if field.field_type in [FieldType.CHAR, FieldType.TEXT]:
                attrs.append('optional="show"')
        
        return ' '.join(attrs)

    def generate_all_views(self, config: ModelConfig) -> str:
        """Génère toutes les vues dans un seul fichier XML"""
        views = []
        
        # Vue liste
        tree_view = self.generate_tree_view(config)
        views.append(tree_view.split('<data>')[1].split('</data>')[0].strip())
        
        # Vue formulaire
        form_view = self.generate_form_view(config)
        views.append(form_view.split('<data>')[1].split('</data>')[0].strip())
        
        # Vue recherche
        search_view = self.generate_search_view(config)
        views.append(search_view.split('<data>')[1].split('</data>')[0].strip())
        
        # Vue kanban (optionnelle)
        kanban_view = self.generate_kanban_view(config)
        views.append(kanban_view.split('<data>')[1].split('</data>')[0].strip())
        
        return f"""<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        {chr(10).join(views)}
    </data>
</odoo>"""