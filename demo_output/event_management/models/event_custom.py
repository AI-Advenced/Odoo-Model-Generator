# -*- coding: utf-8 -*-
"""
Événement
Généré automatiquement par Odoo Model Generator
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventCustom(models.Model):
    """Événement"""
    
    _name = 'event.custom'
    
    _description = 'Événement'
    
    _order = 'name'
    _rec_name = 'name'
    
    # ============ CHAMPS ============
    
    name = fields.Char(string='Nom de l'Événement', required=True, size=200)
    
    description = fields.Html(string='Description')
    
    event_type = fields.Selection(string='Type d'Événement', required=True, selection=[['conference', 'Conférence'], ['workshop', 'Atelier'], ['seminar', 'Séminaire'], ['networking', 'Networking'], ['training', 'Formation'], ['other', 'Autre']])
    
    start_date = fields.Datetime(string='Date de Début', required=True)
    
    end_date = fields.Datetime(string='Date de Fin', required=True)
    
    location = fields.Char(string='Lieu', size=200)
    
    max_participants = fields.Integer(string='Nombre Maximum de Participants', default=50)
    
    price = fields.Float(string='Prix d'Inscription', default=0.0)
    
    organizer_id = fields.Many2One(string='Organisateur', required=True, comodel_name='res.users')
    
    registration_ids = fields.One2Many(string='Inscriptions', comodel_name='event.registration', inverse_name='event_id')
    
    status = fields.Selection(string='Statut', default='draft', selection=[['draft', 'Brouillon'], ['published', 'Publié'], ['ongoing', 'En Cours'], ['done', 'Terminé'], ['cancelled', 'Annulé']])
    
    image = fields.Binary(string='Image de l'Événement')
    
    active = fields.Boolean(string='Actif', help='Décochez pour archiver cet enregistrement', default=True)
    
    
    # ============ MÉTHODES CALCULÉES ============
    
    
    registration_ids_count = fields.Integer(
        string='Nombre de Inscriptions',
        compute='_compute_registration_ids_count'
    )
    
    @api.depends('registration_ids')
    def _compute_registration_ids_count(self):
        """Calcule le nombre d'éléments liés"""
        for record in self:
            record.registration_ids_count = len(record.registration_ids)
    
    
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
    