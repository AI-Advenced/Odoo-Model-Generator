# -*- coding: utf-8 -*-
"""
Produit Avancé
Généré automatiquement par Odoo Model Generator
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TestAdvancedProduct(models.Model):
    """Produit Avancé"""
    
    _name = 'test.advanced.product'
    
    _description = 'Produit Avancé'
    
    _order = 'name'
    _rec_name = 'name'
    
    # ============ CHAMPS ============
    
        name = fields.Char(string='Nom', required=True, size=255)
    
        category_id = fields.Many2One(string='Catégorie', required=True, comodel_name='test.category')
    
        tag_ids = fields.Many2Many(string='Étiquettes', comodel_name='test.tag', relation='product_tag_rel', column1='product_id', column2='tag_id')
    
        status = fields.Selection(string='Statut', default='draft', selection=[['draft', 'Brouillon'], ['active', 'Actif'], ['archived', 'Archivé']])
    
        active = fields.Boolean(string='Actif', help='Décochez pour archiver cet enregistrement', default=True)
    
    
    # ============ MÉTHODES CALCULÉES ============
    
    
    # ============ CONTRAINTES ============
    
    
    # ============ MÉTHODES BUSINESS ============
    def name_get(self):
        """Personnalisation de l'affichage du nom"""
        result = []
        for record in self:
            
            name = record.name or f"#{record.id}"
            
            result.append((record.id, name))
        return result
    
    @api.model
    def create(self, vals):
        """Méthode de création personnalisée"""
        # Ajoutez ici votre logique de création
        return super().create(vals)
    
    def write(self, vals):
        """Méthode de modification personnalisée"""
        # Ajoutez ici votre logique de modification
        return super().write(vals)
    
    def unlink(self):
        """Méthode de suppression personnalisée"""
        # Ajoutez ici votre logique de suppression
        return super().unlink()
    
    
    
    def toggle_active(self):
        """Bascule l'état actif/inactif"""
        for record in self:
            record.active = not record.active
        return True
    
    def archive(self):
        """Archive les enregistrements"""
        return self.write({'active': False})
    
    def unarchive(self):
        """Désarchive les enregistrements"""
        return self.write({'active': True})
    