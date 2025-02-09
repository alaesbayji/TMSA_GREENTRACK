from rest_framework import serializers
from .models import Utilisateur, ResponsableEntreprise, Admin, ResponsableSuiviTMSA, EntrepriseMere, Entreprise, PrefectureProvince, Commune, EngagementIndicateur, Suivi, Indicateur, Aspect
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'motDePasse')
        extra_kwargs = {'motDePasse': {'write_only': True}}

    def create(self, validated_data):
        user = Utilisateur.objects.create(
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            email=validated_data['email'],
            motDePasse=validated_data['motDePasse']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    motDePasse = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], motDePasse=data['motDePasse'])
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        return user

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

class ResponsableEntrepriseSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer()

    class Meta:
        model = ResponsableEntreprise
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer()

    class Meta:
        model = Admin
        fields = '__all__'


class ResponsableSuiviTMSASerializer(serializers.ModelSerializer):
    utilisateur = UtilisateurSerializer()

    class Meta:
        model = ResponsableSuiviTMSA
        fields = '__all__'


class EntrepriseMereSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntrepriseMere
        fields = '__all__'
class EntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entreprise
        fields = '__all__'

class PrefectureProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefectureProvince
        fields = '__all__'


class CommuneSerializer(serializers.ModelSerializer):
    prefecture_province = PrefectureProvinceSerializer()

    class Meta:
        model = Commune
        fields = '__all__'


class EngagementIndicateurSerializer(serializers.ModelSerializer):
    entreprise = EntrepriseSerializer()
    indicateur = serializers.PrimaryKeyRelatedField(queryset=Indicateur.objects.all())

    class Meta:
        model = EngagementIndicateur
        fields = '__all__'


class SuiviSerializer(serializers.ModelSerializer):
    engagement_indicateur = EngagementIndicateurSerializer()

    class Meta:
        model = Suivi
        fields = '__all__'


class IndicateurSerializer(serializers.ModelSerializer):
    aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())

    class Meta:
        model = Indicateur
        fields = '__all__'


class AspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = '__all__'
