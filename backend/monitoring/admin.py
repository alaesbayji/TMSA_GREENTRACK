from django.contrib import admin
from .models.user_models import Utilisateur, ResponsableEntreprise, ResponsableSuiviTMSA, Admin
@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'is_active']

@admin.register(ResponsableEntreprise)
class ResponsableEntrepriseAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'id_entreprise']

@admin.register(ResponsableSuiviTMSA)
class ResponsableSuiviTMSAAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email', 'zone_de_suivi']

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'email']
