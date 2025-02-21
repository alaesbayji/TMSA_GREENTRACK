from rest_framework import serializers
from ..models.aspect_models import Aspect, Indicateur, SousAspectEau, IndicateurEauPollution
from ..models.enterprise_models import EntrepriseMere, Entreprise, SecteurActivite, ActiviteIndustrielle

class IndicateurSerializer(serializers.ModelSerializer):
    id_aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())

    class Meta:
        model = Indicateur
        fields = ['nom', 'seuil_max', 'unite', 'id_aspect']


class AspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = ['id_aspect', 'typeMilieu', 'description', 'est_eau']
class SousAspectEauPollutionSerializer(serializers.ModelSerializer):  
    aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())  

    class Meta:  
        model = SousAspectEau 
        fields = ['id_sous_aspect', 'nom','est_pollution','aspect']  

class IndicateurEauPollutionSerializer(serializers.ModelSerializer):  
    id_sous_aspect = serializers.PrimaryKeyRelatedField(queryset=SousAspectEau.objects.all())  
    id_activite = serializers.PrimaryKeyRelatedField(queryset=ActiviteIndustrielle.objects.all())  

    class Meta:  
        model = IndicateurEauPollution  
        fields = ['id_indicateur_eaupollution', 'nom', 'seuil_max', 'unite', 'code_MICNT', 'id_sous_aspect', 'id_activite']  

    def create(self, validated_data):  
        try:  
            return IndicateurEauPollution.objects.create(**validated_data)  
        except IntegrityError:  
            raise serializers.ValidationError("Ce code MICNT est déjà utilisé pour cet indicateur.")  
