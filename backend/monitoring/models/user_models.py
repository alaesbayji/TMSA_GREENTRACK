from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager
from .enterprise_models import Entreprise  
from .Map_models import Zone  
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
    id_zone = models.ForeignKey(Zone, on_delete=models.CASCADE , null=True)


class Admin(Utilisateur):
    pass

class ResponsableEntreprise(Utilisateur):
    id_entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE , null=True)
