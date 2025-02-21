from django.db import models

class PrefectureProvince(models.Model):
    id_pref_prov = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    id_pref_prov = models.ForeignKey(PrefectureProvince, on_delete=models.CASCADE , null=False)
    nom = models.CharField(max_length=255)
