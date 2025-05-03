from django.db import models
from dateutil.relativedelta import relativedelta
from ..models.enterprise_models import ActiviteIndustrielle,Entreprise
from django.core.exceptions import ValidationError

class Aspect(models.Model):
    id_aspect = models.AutoField(primary_key=True)
    typeMilieu = models.CharField(max_length=255)
    description = models.TextField()
    est_eau = models.BooleanField(default=False)

    def clean(self):
        if self.est_eau:
            # Vérifier s'il existe déjà un autre Aspect avec est_eau = True
            existing_water_aspect = Aspect.objects.filter(est_eau=True).exclude(id_aspect=self.id_aspect)
            if existing_water_aspect.exists():
                raise ValidationError("Un seul aspect peut avoir est_eau = True.")

    def save(self, *args, **kwargs):
        self.clean()  # Appliquer la validation avant de sauvegarder
        super().save(*args, **kwargs)

    def __str__(self):
        return self.typeMilieu
class SousAspectEau(models.Model):
    id_sous_aspect = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    est_pollution = models.BooleanField()
    aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE, limit_choices_to={'est_eau': True})

    def clean(self):
        if self.est_pollution:
            # Vérifier s'il existe déjà un autre SousAspectEau avec est_pollution = True
            existing_pollution_aspect = SousAspectEau.objects.filter(est_pollution=True).exclude(id_sous_aspect=self.id_sous_aspect)
            if existing_pollution_aspect.exists():
                raise ValidationError("Un seul sous-aspect peut avoir est_pollution = True.")

    def save(self, *args, **kwargs):
        self.clean()  # Appliquer la validation avant de sauvegarder
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom
class Indicateur(models.Model):
    id_indicateur = models.AutoField(primary_key=True)
    id_aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE,limit_choices_to={'est_eau': False})
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
class IndicateurSousAspect(models.Model):
    id_indicateur_sous_aspect = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    seuil_max = models.FloatField()
    unite = models.CharField(max_length=100)
    id_sous_aspect = models.ForeignKey(SousAspectEau, on_delete=models.CASCADE, limit_choices_to={'est_pollution': False})

    def __str__(self):
        return self.nom