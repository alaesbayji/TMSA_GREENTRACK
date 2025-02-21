from django.db import models
from dateutil.relativedelta import relativedelta
from ..models.enterprise_models import ActiviteIndustrielle,Entreprise

class Aspect(models.Model):
    id_aspect = models.AutoField(primary_key=True)
    typeMilieu = models.CharField(max_length=255)
    description = models.TextField()
    est_eau = models.BooleanField(default=False)  # Nouveau champ pour identifier l'eau

    def __str__(self):
        return self.typeMilieu
class SousAspectEau(models.Model):
    id_sous_aspect = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)  # Ex: "Eau Souterraine", "Eau Superficielle", "Eau Pollution"
    est_pollution = models.BooleanField()  # True uniquement pour "Eau Pollution"
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, limit_choices_to={'typeMilieu': 'Eau'})
class Indicateur(models.Model):
    id_indicateur = models.AutoField(primary_key=True)
    id_aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    seuil_max = models.FloatField()
    unite = models.CharField(max_length=100)
class IndicateurEauPollution(models.Model):
    id_indicateur_eaupollution = models.AutoField(primary_key=True)
    id_sous_aspect = models.ForeignKey(SousAspectEau, on_delete=models.CASCADE)
    id_activite = models.ForeignKey(ActiviteIndustrielle, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    seuil_max = models.FloatField()
    unite = models.CharField(max_length=100)
    code_MICNT = models.IntegerField()
