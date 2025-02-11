from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.contrib.auth.hashers import make_password

class Utilisateur(AbstractUser):
    idUtilisateur = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    username = None  # Supprime l'usage par défaut de `username`
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.email})"




class ResponsableSuiviTMSA(Utilisateur):
    zone_de_suivi = models.CharField(max_length=255, null=True, blank=True)


class Admin(Utilisateur):
    pass



class PrefectureProvince(models.Model):
    id_pref_prov = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    id_pref_prov = models.ForeignKey(PrefectureProvince, on_delete=models.CASCADE , null=False)
    nom = models.CharField(max_length=255)

class EntrepriseMere(models.Model):
    id_entreprise_mere = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    statut_juridique = models.CharField(max_length=255)

class Entreprise(models.Model):
    id_entreprise = models.AutoField(primary_key=True)
    id_entreprise_mere = models.ForeignKey(EntrepriseMere, on_delete=models.CASCADE, null=True, blank=True)
    id_commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    zone = models.CharField(max_length=255)
    montant_investissement = models.FloatField()
    nombre_emploi = models.IntegerField()
    superficie_totale = models.FloatField()
    secteur_dominant = models.CharField(max_length=255)
    prefecture_province = models.CharField(max_length=255)
    DAE = models.FileField(upload_to='documents/', null=True, blank=True)
    EIE_PSSE = models.FileField(upload_to='documents/', null=True, blank=True)
class ResponsableEntreprise(Utilisateur):
    id_entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE , null=True)

class Aspect(models.Model):
    id_aspect = models.AutoField(primary_key=True)
    typeMilieu = models.CharField(max_length=255)
    description = models.TextField()

class Indicateur(models.Model):
    id_indicateur = models.AutoField(primary_key=True)
    id_aspect = models.ForeignKey(Aspect, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    seuil_max = models.FloatField()
    unite = models.CharField(max_length=100)



class EngagementAspect(models.Model):
    id_engagement_aspect = models.AutoField(primary_key=True)
    lieu_prelevement = models.CharField(max_length=255)
    methode_equipement = models.CharField(max_length=255)
    frequence = models.IntegerField()
    responsabilite = models.CharField(max_length=255)
    date_creation = models.DateField()  # Champ manuel pour saisir la date

    def __str__(self):
        return f"Aspect {self.id_engagement_aspect} - {self.engagement_indicateur.id_engagement_indicateur}"
class EngagementIndicateur(models.Model):
    id_engagement_indicateur = models.AutoField(primary_key=True)
    id_entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, related_name='engagements')
    id_indicateur = models.ForeignKey(Indicateur, on_delete=models.CASCADE, related_name='engagements')
    id_engagement_aspect = models.ForeignKey(EngagementAspect, on_delete=models.CASCADE, related_name='aspects',null=True, blank=True,)

    def __str__(self):
        return f"Engagement {self.id_engagement_indicateur} - {self.entreprise.nom}"
class Echeance(models.Model):
    id_echeance = models.AutoField(primary_key=True)
    id_engagement_aspect = models.ForeignKey(EngagementAspect, on_delete=models.CASCADE, null=True, blank=True,related_name='echeances')
    date_limite = models.DateField()
    statut = models.CharField(max_length=50, choices=[('en attente', 'En attente'), ('effectuee', 'Effectuée')], default='en attente')

    def __str__(self):
        return f"Echéance {self.id_echeance} - {self.engagement_aspect.id_engagement_aspect}"

class Suivi(models.Model):
    id_suivi = models.AutoField(primary_key=True)
    id_engagement_aspect = models.ForeignKey('EngagementAspect', on_delete=models.CASCADE, related_name='suivis')
    date_mesure = models.DateField()
    justificatif_etude = models.FileField(upload_to='justificatifs/', null=True, blank=True)
    echeance = models.OneToOneField('Echeance', on_delete=models.CASCADE, null=True, blank=True, related_name='suivi_associe')

    def __str__(self):
        return f"Suivi {self.id_suivi} - Mesure le {self.date_mesure}"


class SuiviIndicateur(models.Model):
    id_suivi_indicateur = models.AutoField(primary_key=True)
    suivi = models.ForeignKey(Suivi, on_delete=models.CASCADE, related_name='suivi_indicateurs')
    engagement_indicateur = models.ForeignKey('EngagementIndicateur', on_delete=models.CASCADE)
    valeur_mesure = models.FloatField()
    observations = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Suivi Indicateur {self.id_suivi_indicateur} - {self.engagement_indicateur.id_indicateur}"
