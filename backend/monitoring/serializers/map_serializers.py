from rest_framework import serializers
from ..models.Map_models import PrefectureProvince, Commune,Parcelle

class PrefectureProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefectureProvince
        fields = ('id_pref_prov', 'nom')


class CommuneSerializer(serializers.ModelSerializer):
    id_pref_prov = serializers.PrimaryKeyRelatedField(queryset=PrefectureProvince.objects.all())

    class Meta:
        model = Commune
        fields = ('id_commune', 'nom', 'id_pref_prov')

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelle
        fields = ['id_parcelle', 'geom']