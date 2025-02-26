from django.db import models
from .Map_models import Commune ,Parcelle,Zone,PrefectureProvince
class EntrepriseMere(models.Model):
    id_entreprise_mere = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    statut_juridique = models.CharField(max_length=255)
class SecteurActivite(models.Model):
    id_secteur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.nom


class ActiviteIndustrielle(models.Model):
    id_activite = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255, unique=True)
    id_secteur = models.ForeignKey(SecteurActivite, on_delete=models.CASCADE, related_name='activites')
    
    def __str__(self):
        return self.nom
def set_entreprise_file_path(instance, filename):  
    # Créer un chemin basé sur l'ID de l'entreprise mère et celui de l'entreprise  
    return f'DAE+PSSE/{instance.id_entreprise_mere.nom}/{instance.nom}/{filename}'  
class Entreprise(models.Model):  
    id_entreprise = models.AutoField(primary_key=True)  
    id_entreprise_mere = models.ForeignKey('EntrepriseMere', on_delete=models.CASCADE, null=True, blank=True)  
    id_commune = models.ForeignKey('Commune', on_delete=models.CASCADE)  
    id_activite = models.ForeignKey('ActiviteIndustrielle', on_delete=models.CASCADE, null=True, blank=True)  
    id_parcelle = models.OneToOneField('Parcelle', on_delete=models.SET_NULL, null=True, blank=True)  
    id_zone = models.ForeignKey('Zone', on_delete=models.CASCADE, null=True, blank=True)   
    Ilot = models.CharField(max_length=255, null=True, blank=True)  
    lot = models.CharField(max_length=255, null=True, blank=True)  
    avenue = models.CharField(max_length=255, null=True, blank=True)  
    rue = models.CharField(max_length=255, null=True, blank=True)  
    secteur = models.CharField(max_length=255, null=True, blank=True)  
    regime = models.CharField(max_length=255, null=True, blank=True)  
    nom = models.CharField(max_length=255, null=True, blank=True)  
    adresse = models.CharField(max_length=500, null=True, blank=True)  # Modification pour stocker l'adresse générée  
    montant_investissement = models.FloatField()  
    nombre_emploi = models.IntegerField()  
    superficie_totale = models.FloatField()  
    DAE = models.FileField(upload_to='uploads/', null=True, blank=True)  
    EIE_PSSE = models.FileField(upload_to='uploads/', null=True, blank=True)  

    def save(self, *args, **kwargs):  
        self.adresse = self.generer_adresse()  # Générer l'adresse avant de sauvegarder  
        super().save(*args, **kwargs)  

    def generer_adresse(self):  
        """Génère l'adresse à partir des différents attributs."""  
        x = self.id_parcelle.x if self.id_parcelle else ''  
        y = self.id_parcelle.y if self.id_parcelle else ''  
        zone = self.id_zone.nom if self.id_zone else ''  
        commune = self.id_commune.nom if self.id_commune else ''  
        prefecture = self.id_commune.id_pref_prov.nom if self.id_commune and self.id_commune.id_pref_prov else ''  

        components = [  
            self.nom,  
            zone,  
            self.secteur,  
        ]  

        # Ajout conditionnel pour Ilot et d'autres composants  
        if zone == "TFZ":  
            components.append(f"Ilot: {self.Ilot}")  
        
        components.extend([  
            f"lot: {self.lot}",  
            f"Avenue: {self.avenue}",  
            f"Rue: {self.rue}",  
            commune,  
            prefecture,  
            f"Coordonnées: {x}, {y}"  
        ])  

        # Filtrer les composants vides et rejoindre avec des espaces  
        adresse_complete = ' '.join(filter(None, components))  
        
        return adresse_complete.strip()  # Retourne l'adresse générée  
