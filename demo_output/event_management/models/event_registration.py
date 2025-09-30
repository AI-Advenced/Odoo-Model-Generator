# -*- coding: utf-8 -*-
"""
Inscription à un Événement
Généré automatiquement par Odoo Model Generator
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventRegistration(models.Model):
    """Inscription à un Événement"""
    
    _name = 'event.registration'
    
    _description = 'Inscription à un Événement'
    
    _order = 'name'
    _rec_name = 'name'
    
    # ============ CHAMPS ============
    
    name = fields.Char(string='Nom du Participant', required=True, size=150)
    
    email = fields.Char(string='Email', required=True, size=100)
    
    phone = fields.Char(string='Téléphone', size=20)
    
    company = fields.Char(string='Entreprise', size=100)
    
    event_id = fields.Many2One(string='Événement', required=True, comodel_name='event.custom')
    
    registration_date = fields.Datetime(string='Date d'Inscription', readonly=True, default=fields.Datetime.now)
    
    state = fields.Selection(string='État', default='draft', selection=[['draft', 'Brouillon'], ['confirmed', 'Confirmé'], ['attended', 'Présent'], ['cancelled', 'Annulé']])
    
    payment_status = fields.Selection(string='Statut Paiement', default='unpaid', selection=[['unpaid', 'Non Payé'], ['partial', 'Partiel'], ['paid', 'Payé'], ['refunded', 'Remboursé']])
    
    amount_paid = fields.Float(string='Montant Payé', default=0.0)
    
    notes = fields.Text(string='Notes')
    
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
    