from rest_framework import serializers
from ..models.enterprise_models import EntrepriseMere, Entreprise, SecteurActivite, ActiviteIndustrielle
from ..models.Map_models import Parcelle,Zone,Commune
from ..serializers.suivi_serializers import EngagementAspectSerializer
from .map_serializers import ZoneSerializer,CommuneSerializer
class SecteurActiviteSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = SecteurActivite  
        fields = ['id_secteur', 'nom']  

class ActiviteIndustrielleSerializer(serializers.ModelSerializer):  
    id_secteur = serializers.PrimaryKeyRelatedField(queryset=SecteurActivite.objects.all()) 
    id_secteur_detail = SecteurActiviteSerializer(source='id_secteur', read_only=True)  

    class Meta:  
        model = ActiviteIndustrielle  
        fields = ['id_activite', 'nom', 'id_secteur','id_secteur_detail']  
class EntrepriseMereSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepriseMere
        fields = '__all__'
class EntrepriseSerializer(serializers.ModelSerializer):  
    # Relations détaillées (lecture seule)  
    id_commune_detail = CommuneSerializer(source='id_commune', read_only=True)  
    id_activite_detail = ActiviteIndustrielleSerializer(source='id_activite', read_only=True)  
    id_zone_detail = ZoneSerializer(source='id_zone', read_only=True)  

    # Relations modifiables via ID  
    id_commune = serializers.PrimaryKeyRelatedField(queryset=Commune.objects.all(), required=True)  
    id_activite = serializers.PrimaryKeyRelatedField(queryset=ActiviteIndustrielle.objects.all(), allow_null=True, required=False)  
    id_zone = serializers.PrimaryKeyRelatedField(queryset=Zone.objects.all(), allow_null=True, required=False)  
    id_parcelle = serializers.PrimaryKeyRelatedField(queryset=Parcelle.objects.all())
    class Meta:  
        model = Entreprise  
        fields = [  
            'id_entreprise', 'id_entreprise_mere', 'id_commune', 'id_commune_detail',  
            'id_activite', 'id_activite_detail', 'id_zone', 'id_zone_detail',  
            'nom', 'adresse', 'Ilot', 'lot', 'avenue', 'secteur', 'rue',  'id_parcelle',
            'montant_investissement', 'nombre_emploi', 'superficie_totale',  
            'DAE', 'EIE_PSSE'  
        ]  
    def create(self, validated_data):  
        entreprise = super().create(validated_data)  
        # Vous pouvez ajouter d'autres logiques ici après la création, si nécessaire  
        return entreprise  