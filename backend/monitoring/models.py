from django.db import models

class Utilisateur(models.Model):
    idUtilisateur = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    motDePasse = models.CharField(max_length=100)

class ResponsableEntreprise(Utilisateur):
    id_entreprise_mere = models.IntegerField()
    id_entreprise = models.IntegerField()

class Admin(Utilisateur):
    pass

class ResponsableSuiviTMSA(Utilisateur):
    zone_de_suivi = models.CharField(max_length=255)

class PrefectureProvince(models.Model):
    id_pref_prov = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    id_pref_prov = models.ForeignKey(PrefectureProvince, on_delete=models.CASCADE)
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
    montantInvestissement = models.FloatField()
    nombreEmploi = models.IntegerField()
    superficieTotale = models.FloatField()
    secteurDominant = models.CharField(max_length=255)
    prefectureProvince = models.CharField(max_length=255)
    DAE = models.FileField(upload_to='documents/', null=True, blank=True)
    EIE_PSSE = models.FileField(upload_to='documents/', null=True, blank=True)

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

class EngagementIndicateur(models.Model):
    id_engagement_indicateur = models.AutoField(primary_key=True)
    id_entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    id_indicateur = models.ForeignKey(Indicateur, on_delete=models.CASCADE)
    lieu_prelevement = models.CharField(max_length=255)
    methode_equipement = models.CharField(max_length=255)
    frequence = models.IntegerField()
    responsabilite = models.CharField(max_length=255)

class Suivi(models.Model):
    idSuivi = models.AutoField(primary_key=True)
    id_engagement_aspect = models.ForeignKey(EngagementIndicateur, on_delete=models.CASCADE)
    dateMesure = models.DateField()
    valeurMesure = models.FloatField()
    observations = models.TextField()
    justificatif_etude = models.FileField(upload_to='documents/', null=True, blank=True)
