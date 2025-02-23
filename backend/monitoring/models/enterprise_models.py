from django.db import models
from .Map_models import Commune ,Parcelle
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
    id_entreprise_mere = models.ForeignKey(EntrepriseMere, on_delete=models.CASCADE, null=True, blank=True)  
    id_commune = models.ForeignKey(Commune, on_delete=models.CASCADE)  
    id_activite = models.ForeignKey(ActiviteIndustrielle, on_delete=models.CASCADE,null=True, blank=True)  
    id_parcelle = models.OneToOneField(Parcelle, on_delete=models.SET_NULL, null=True, blank=True)  # Utilisation de OneToOneField  
    nom = models.CharField(max_length=255)  
    adresse = models.CharField(max_length=255)  
    zone = models.CharField(max_length=255)  
    montant_investissement = models.FloatField()  
    nombre_emploi = models.IntegerField()  
    superficie_totale = models.FloatField()  
    DAE = models.FileField(upload_to=set_entreprise_file_path, null=True, blank=True)  
    EIE_PSSE = models.FileField(upload_to=set_entreprise_file_path, null=True, blank=True)  