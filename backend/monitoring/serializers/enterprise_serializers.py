from rest_framework import serializers
from ..models.enterprise_models import EntrepriseMere, Entreprise, SecteurActivite, ActiviteIndustrielle
from ..serializers.suivi_serializers import EngagementAspectSerializer
class SecteurActiviteSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = SecteurActivite  
        fields = ['id_secteur', 'nom']  

class ActiviteIndustrielleSerializer(serializers.ModelSerializer):  
    id_secteur = serializers.PrimaryKeyRelatedField(queryset=SecteurActivite.objects.all())  

    class Meta:  
        model = ActiviteIndustrielle  
        fields = ['id_activite', 'nom', 'id_secteur']  
class EntrepriseMereSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepriseMere
        fields = '__all__'
class EntrepriseSerializer(serializers.ModelSerializer):
    engagements_aspects = EngagementAspectSerializer(many=True, read_only=True)
    id_activite = serializers.PrimaryKeyRelatedField(queryset=ActiviteIndustrielle.objects.all())  

    class Meta:
        model = Entreprise
        fields = ['id_entreprise', 'id_entreprise_mere', 'id_commune','id_activite' ,'nom', 'adresse', 'zone', 
                  'montant_investissement', 'nombre_emploi', 'superficie_totale', 
                  'secteur_dominant', 'prefecture_province', 'DAE', 'EIE_PSSE', 'engagements_aspects']