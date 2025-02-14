from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superutilisateur doit avoir is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superutilisateur doit avoir is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Utilisateur(AbstractUser):
    idUtilisateur = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    username = None  # Supprime l'usage par défaut de `username`
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']
    objects = CustomUserManager()

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
    id_entreprise = models.ForeignKey('Entreprise', on_delete=models.CASCADE, related_name='engagements_aspects', null=True, blank=True)
    id_aspect = models.ForeignKey('Aspect', on_delete=models.CASCADE, null=True, blank=True)
    lieu_prelevement = models.CharField(max_length=255)
    methode_equipement = models.CharField(max_length=255)
    frequence = models.IntegerField()
    responsabilite = models.CharField(max_length=255)
    date_creation = models.DateField()
    date_prochaine_echeance = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id_aspect'],
                name='unique_engagement_aspect_aspect'
            )
        ]

    def generer_prochaine_echeance(self):
        """Génère la prochaine échéance et crée un suivi"""
        self.date_prochaine_echeance = self.calculer_prochaine_date()
        self.save()

        if self.date_prochaine_echeance:
            Suivi.objects.create(
                id_engagement_aspect=self,
                date_limite=self.date_prochaine_echeance,
                statut="en attente"
            )

    def calculer_prochaine_date(self):
        """Calculer la date en fonction de la fréquence"""
        if self.frequence > 0:
            return self.date_creation + relativedelta(months=(12 // self.frequence))
        return None


class EngagementIndicateur(models.Model):
    id_engagement_indicateur = models.AutoField(primary_key=True)
    id_indicateur = models.ForeignKey('Indicateur', on_delete=models.CASCADE)
    id_engagement_aspect = models.ForeignKey(EngagementAspect, on_delete=models.CASCADE, null=True, blank=True, related_name='engagements_indicateurs')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['id_engagement_aspect', 'id_indicateur'],
                name='unique_engagement_aspect_indicateur'
            )
        ]

class Suivi(models.Model):
    STATUT_CHOICES = [
        ('en attente', 'En attente'),
        ('effectué', 'Effectué'),
        ('effectué_Retard', 'Effectué_Retard'),
    ]

    id_suivi = models.AutoField(primary_key=True)
    id_engagement_aspect = models.ForeignKey(EngagementAspect, on_delete=models.CASCADE, related_name='suivis')
    date_mesure = models.DateField(null=True, blank=True)
    date_limite = models.DateField(null=True, blank=True)
    justificatif_etude = models.FileField(upload_to='justificatifs/', null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en attente')
    cloturer = models.BooleanField(default=False)  # Nouveau champ

    def mettre_a_jour_statut(self):
        if self.date_mesure:
            if self.date_mesure <= self.date_limite:
                self.statut = "effectué"
            else:
                self.statut = "effectué_Retard"
            self.save()

class SuiviIndicateur(models.Model):
    id_suivi_indicateur = models.AutoField(primary_key=True)
    suivi = models.ForeignKey(Suivi, on_delete=models.CASCADE, related_name='suivi_indicateurs')
    engagement_indicateur = models.ForeignKey(EngagementIndicateur, on_delete=models.CASCADE)
    valeur_mesure = models.FloatField()
    observations = models.TextField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['suivi', 'engagement_indicateur'],
                name='unique_suivi_engagement_indicateur'
            )
        ]