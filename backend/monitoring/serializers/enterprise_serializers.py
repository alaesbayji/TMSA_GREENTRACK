from rest_framework import serializers
from ..models.enterprise_models import EntrepriseMere, Entreprise, SecteurActivite, ActiviteIndustrielle
from ..models.Map_models import Parcelle
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
    id_parcelle = serializers.PrimaryKeyRelatedField(queryset=Parcelle.objects.all())  

    class Meta:
        model = Entreprise
        fields = ['id_entreprise', 'id_entreprise_mere', 'id_commune','id_activite' ,'nom', 'adresse', 'zone', 
                  'montant_investissement', 'nombre_emploi', 'superficie_totale', 
                    'DAE', 'EIE_PSSE', 'engagements_aspects','id_parcelle']
    def create(self, validated_data):  
        entreprise = super().create(validated_data)  
        # Vous pouvez ajouter d'autres logiques ici après la création, si nécessaire  
        return entreprise  