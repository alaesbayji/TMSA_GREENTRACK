from django.contrib.gis.db import models

class PrefectureProvince(models.Model):
    id_pref_prov = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)

class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    id_pref_prov = models.ForeignKey(PrefectureProvince, on_delete=models.CASCADE , null=False)
    nom = models.CharField(max_length=255)

class Parcelle(models.Model):
    id_parcelle = models.AutoField(primary_key=True)
    geom = models.PolygonField(srid=26191)  # Géométrie de la parcelle
    def __str__(self):
        return f"Parcelle {self.id_parcelle}"