from rest_framework import serializers
from ..models.Map_models import PrefectureProvince, Commune,Parcelle,Zone

class PrefectureProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefectureProvince
        fields = ('id_pref_prov', 'nom')

class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ('id_zone', 'nom')


class CommuneSerializer(serializers.ModelSerializer):
    id_pref_prov = PrefectureProvinceSerializer(read_only=True)
    class Meta:
        model = Commune
        fields = ('id_commune', 'nom', 'id_pref_prov')

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelle
        fields = ['id_parcelle', 'geom']