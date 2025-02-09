from rest_framework import serializers
from .models import Utilisateur, ResponsableEntreprise, Admin, ResponsableSuiviTMSA, EntrepriseMere, Entreprise, PrefectureProvince, Commune, EngagementIndicateur, Suivi, Indicateur, Aspect
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Utilisateur.objects.create(
            nom=validated_data['nom'],
            prenom=validated_data['prenom'],
            email=validated_data['email'],
            username=validated_data['email']  # Use email as username
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
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
        fields = ('id_pref_prov', 'nom')


class CommuneSerializer(serializers.ModelSerializer):
    id_pref_prov = serializers.PrimaryKeyRelatedField(queryset=PrefectureProvince.objects.all())

    class Meta:
        model = Commune
        fields = ('id_commune', 'nom', 'id_pref_prov')

class EngagementIndicateurSerializer(serializers.ModelSerializer):
    id_entreprise = serializers.PrimaryKeyRelatedField(queryset=Entreprise.objects.all())
    id_indicateur = serializers.PrimaryKeyRelatedField(queryset=Indicateur.objects.all())

    class Meta:
        model = EngagementIndicateur
        fields = ('id_engagement_indicateur', 'id_entreprise', 'id_indicateur', 
                  'lieu_prelevement', 'methode_equipement', 'frequence', 
                  'responsabilite')


class SuiviSerializer(serializers.ModelSerializer):
    id_engagement_aspect = serializers.PrimaryKeyRelatedField(queryset=EngagementIndicateur.objects.all())

    class Meta:
        model = Suivi
        fields = ('idSuivi', 'id_engagement_aspect', 'dateMesure', 'valeurMesure', 'observations', 'justificatif_etude')


class IndicateurSerializer(serializers.ModelSerializer):
    id_aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())

    class Meta:
        model = Indicateur
        fields = ['nom', 'seuil_max', 'unite', 'id_aspect']


class AspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = '__all__'
