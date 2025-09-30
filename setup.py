#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup configuration for Odoo Model Generator
"""

from setuptools import setup, find_packages
import os

# Lecture du README pour la description longue
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# Lecture des requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name='odoo-model-generator',
    version='1.0.0',
    description='Générateur automatique de modules Odoo à partir de configurations YAML/JSON',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    
    # Informations sur l'auteur
    author='Odoo Model Generator Team',
    author_email='info@odoo-model-generator.com',
    maintainer='Odoo Model Generator Team',
    maintainer_email='info@odoo-model-generator.com',
    
    # URLs du projet
    url='https://github.com/odoo-model-generator/odoo-model-generator',
    project_urls={
        'Bug Reports': 'https://github.com/odoo-model-generator/odoo-model-generator/issues',
        'Source': 'https://github.com/odoo-model-generator/odoo-model-generator',
        'Documentation': 'https://odoo-model-generator.readthedocs.io',
    },
    
    # Configuration des packages
    packages=find_packages(exclude=['tests*', 'examples*']),
    include_package_data=True,
    package_data={
        'odoo_model_generator': [
            'templates/*.py',
            'config/*.py',
        ],
    },
    
    # Dépendances
    install_requires=read_requirements(),
    python_requires='>=3.8',
    
    # Scripts de ligne de commande
    entry_points={
        'console_scripts': [
            'omg=odoo_model_generator.cli:cli',
            'odoo-model-generator=odoo_model_generator.cli:cli',
        ],
    },
    
    # Classification
    classifiers=[
        # Statut de développement
        'Development Status :: 4 - Beta',
        
        # Audience visée
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        
        # Domaine d'application
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Enterprise Resource Planning (ERP)',
        
        # Licence
        'License :: OSI Approved :: MIT License',
        
        # Systèmes d'exploitation
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        
        # Versions Python supportées
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        
        # Interface
        'Environment :: Console',
        'Environment :: Web Environment',
    ],
    
    # Mots-clés pour la recherche
    keywords=[
        'odoo', 'erp', 'model', 'generator', 'code-generation', 
        'automation', 'development-tools', 'yaml', 'json', 'cli'
    ],
    
    # Licence
    license='MIT',
    
    # Options de distribution
    zip_safe=False,
    
    # Dépendances optionnelles
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'black>=23.0',
            'flake8>=5.0',
            'mypy>=1.0',
            'pre-commit>=3.0',
        ],
        'docs': [
            'sphinx>=6.0',
            'sphinx-rtd-theme>=1.0',
            'myst-parser>=1.0',
        ],
        'test': [
            'pytest>=7.0',
            'pytest-cov>=4.0',
            'coverage>=7.0',
        ],
    },
    
    # Configuration des tests
    test_suite='tests',
    tests_require=[
        'pytest>=7.0',
        'pytest-cov>=4.0',
    ],
)