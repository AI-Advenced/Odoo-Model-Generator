# -*- coding: utf-8 -*-
"""
Formateurs de code pour une sortie propre
"""

import re
from typing import List, Dict

class CodeFormatter:
    """Formateur de code Python et XML pour Odoo"""
    
    @staticmethod
    def format_python_code(code: str) -> str:
        """Formate le code Python selon les standards Odoo"""
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Suppression des espaces en fin de ligne
            line = line.rstrip()
            
            # Ajout des lignes non vides
            formatted_lines.append(line)
        
        # Suppression des lignes vides multiples
        result = []
        prev_empty = False
        
        for line in formatted_lines:
            if not line.strip():
                if not prev_empty:
                    result.append(line)
                prev_empty = True
            else:
                result.append(line)
                prev_empty = False
        
        return '\n'.join(result)
    
    @staticmethod
    def format_xml_code(xml_code: str) -> str:
        """Formate le code XML avec indentation correcte"""
        lines = xml_code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Diminuer l'indentation pour les balises fermantes
            if line.startswith('</') or line.startswith('<!--') and '-->' in line:
                indent_level = max(0, indent_level - 1)
            
            # Ajouter l'indentation
            formatted_lines.append('    ' * indent_level + line)
            
            # Augmenter l'indentation pour les balises ouvrantes
            if line.startswith('<') and not line.startswith('</') and not line.endswith('/>') and not line.startswith('<!--'):
                indent_level += 1
            # Diminuer pour les balises auto-fermantes
            elif line.endswith('/>'):
                pass  # Pas de changement d'indentation
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def format_field_name(name: str) -> str:
        """Formate un nom de champ selon les conventions Odoo"""
        # Conversion en snake_case
        name = re.sub(r'([A-Z])', r'_\1', name).lower()
        name = re.sub(r'[^a-z0-9_]', '_', name)
        name = re.sub(r'_+', '_', name)
        name = name.strip('_')
        
        # S'assurer que le nom commence par une lettre
        if name and name[0].isdigit():
            name = f'field_{name}'
        
        return name
    
    @staticmethod
    def format_model_name(name: str) -> str:
        """Formate un nom de modèle selon les conventions Odoo"""
        # Conversion en minuscules avec points
        name = name.lower()
        name = re.sub(r'[^a-z0-9._]', '.', name)
        name = re.sub(r'\.+', '.', name)
        name = name.strip('.')
        
        return name
    
    @staticmethod
    def format_class_name(model_name: str) -> str:
        """Génère un nom de classe Python à partir du nom du modèle"""
        # Conversion en PascalCase
        parts = model_name.split('.')
        class_name = ''.join(word.capitalize() for word in parts)
        return class_name
    
    @staticmethod
    def format_label(field_name: str) -> str:
        """Génère un label lisible à partir du nom de champ"""
        # Remplacement des underscores par des espaces et capitalisation
        label = field_name.replace('_', ' ').title()
        
        # Corrections spécifiques
        corrections = {
            'Id': 'ID',
            'Url': 'URL',
            'Html': 'HTML',
            'Xml': 'XML',
            'Api': 'API',
            'Ui': 'UI'
        }
        
        for old, new in corrections.items():
            label = label.replace(old, new)
        
        return label
    
    @staticmethod
    def format_description(text: str, max_length: int = 80) -> str:
        """Formate une description avec retour à la ligne"""
        if len(text) <= max_length:
            return text
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    @staticmethod
    def format_docstring(text: str, indent: str = '    ') -> str:
        """Formate une docstring Python"""
        lines = text.strip().split('\n')
        formatted_lines = [f'{indent}"""']
        
        for line in lines:
            formatted_lines.append(f'{indent}{line}')
        
        formatted_lines.append(f'{indent}"""')
        
        return '\n'.join(formatted_lines)
    
    @staticmethod
    def format_selection_values(selection_list: List[List]) -> str:
        """Formate une liste de sélection pour le code Python"""
        formatted_items = []
        
        for item in selection_list:
            if len(item) == 2:
                value, label = item
                formatted_items.append(f"('{value}', '{label}')")
        
        return '[' + ', '.join(formatted_items) + ']'
    
    @staticmethod
    def add_file_header(content: str, file_type: str = 'python', 
                       module_name: str = None, description: str = None) -> str:
        """Ajoute un en-tête standard au fichier"""
        
        if file_type == 'python':
            header = '# -*- coding: utf-8 -*-\n'
            if description:
                header += f'"""\n{description}\n"""\n\n'
        elif file_type == 'xml':
            header = '<?xml version="1.0" encoding="utf-8"?>\n'
        else:
            header = ''
        
        return header + content
    
    @staticmethod
    def remove_extra_blank_lines(content: str, max_consecutive: int = 2) -> str:
        """Supprime les lignes vides excessives"""
        lines = content.split('\n')
        result = []
        empty_count = 0
        
        for line in lines:
            if not line.strip():
                empty_count += 1
                if empty_count <= max_consecutive:
                    result.append(line)
            else:
                empty_count = 0
                result.append(line)
        
        return '\n'.join(result)
    
    @staticmethod
    def format_manifest_dependencies(deps: List[str]) -> str:
        """Formate la liste des dépendances pour __manifest__.py"""
        if not deps:
            return '[]'
        
        if len(deps) == 1:
            return f"['{deps[0]}']"
        
        # Multi-lignes pour plusieurs dépendances
        formatted_deps = ["["]
        for dep in deps:
            formatted_deps.append(f"    '{dep}',")
        formatted_deps.append("]")
        
        return '\n'.join(formatted_deps)
    
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """Convertit CamelCase en snake_case"""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def snake_to_camel(name: str) -> str:
        """Convertit snake_case en CamelCase"""
        components = name.split('_')
        return ''.join(word.capitalize() for word in components)
    
    @staticmethod
    def pluralize(word: str) -> str:
        """Ajoute la forme plurielle (simple)"""
        if word.endswith('y'):
            return word[:-1] + 'ies'
        elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return word + 'es'
        else:
            return word + 's'