from django.contrib.gis.db import models

class PrefectureProvince(models.Model):
    id_pref_prov = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
class Zone(models.Model):
    id_zone = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
class Commune(models.Model):
    id_commune = models.AutoField(primary_key=True)
    id_pref_prov = models.ForeignKey(PrefectureProvince, on_delete=models.CASCADE , null=False)
    nom = models.CharField(max_length=255)

class Parcelle(models.Model):
    id_parcelle = models.AutoField(primary_key=True)
    id_zone =  models.ForeignKey(Zone, on_delete=models.CASCADE,null=True, blank=True) 
    geom = models.PolygonField(srid=26191)  # Géométrie de la parcelle
    geom = models.PolygonField(srid=26191)  # Géométrie de la parcelle  
    x = models.FloatField(null=True, blank=True)  # Coordonnée X du centre  
    y = models.FloatField(null=True, blank=True)  # Coordonnée Y du centre  

    def save(self, *args, **kwargs):  
        # Calculer le centroïde et mettre à jour les coordonnées X et Y  
        centroid = self.geom.centroid  # Utilisation de la méthode centroid pour obtenir le centroïde  
        self.x = centroid.x  
        self.y = centroid.y  
        super().save(*args, **kwargs)  # Appeler la méthode save parent pour enregistrer l'instance  

    def __str__(self):  
        return f"Parcelle {self.id_parcelle}"  