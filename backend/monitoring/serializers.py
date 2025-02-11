from rest_framework import serializers
from .models import Utilisateur, ResponsableEntreprise, Admin, SuiviIndicateur,ResponsableSuiviTMSA, EntrepriseMere, Entreprise, EngagementAspect,PrefectureProvince, Commune, EngagementIndicateur, Suivi, Indicateur, Aspect,Echeance
from django.contrib.auth import authenticate
from django.db import transaction

class SignupSerializer(serializers.ModelSerializer):
    id_entreprise = serializers.PrimaryKeyRelatedField(
        queryset=Entreprise.objects.all(), required=False, allow_null=True
    )
    zone_de_suivi = serializers.CharField(write_only=True, required=False)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'password', 'id_entreprise', 'zone_de_suivi', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'id_entreprise': {'required': False},
            'zone_de_suivi': {'required': False}
        }

    def create(self, validated_data):
        role = validated_data.pop('role', None)

        with transaction.atomic():
            if role == 'ResponsableEntreprise':
                validated_data.pop('zone_de_suivi', None)
                user = ResponsableEntreprise.objects.create(**validated_data)

            elif role == 'ResponsableSuiviTMSA':
                validated_data.pop('id_entreprise', None)
                user = ResponsableSuiviTMSA.objects.create(**validated_data)

            elif role == 'Admin':
                validated_data.pop('zone_de_suivi', None)
                validated_data.pop('id_entreprise', None)
                user = Admin.objects.create(**validated_data)

            else:
                raise serializers.ValidationError("Rôle invalide")

            user.set_password(validated_data["password"])
            user.save()
            return user

    def validate(self, data):
        role = data.get('role')
        if role == 'ResponsableEntreprise' and not data.get('id_entreprise'):
            raise serializers.ValidationError("L'id de l'entreprise est requis pour ResponsableEntreprise.")
        if role == 'ResponsableSuiviTMSA' and not data.get('zone_de_suivi'):
            raise serializers.ValidationError("La zone de suivi est requise pour ResponsableSuiviTMSA.")
        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Identifiants invalides")
        return user

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
class EcheanceSerializer(serializers.ModelSerializer):
    id_engagement_aspect = serializers.PrimaryKeyRelatedField(queryset=EngagementAspect.objects.all())

    class Meta:
        model = Echeance
        fields = ['id_echeance', 'id_engagement_aspect', 'date_limite', 'statut']


class SuiviIndicateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviIndicateur
        fields = ['id_suivi_indicateur', 'engagement_indicateur', 'valeur_mesure', 'observations']

class SuiviSerializer(serializers.ModelSerializer):
    suivi_indicateurs = SuiviIndicateurSerializer(many=True, required=True, write_only=True)

    class Meta:
        model = Suivi
        fields = ['id_suivi', 'id_engagement_aspect', 'date_mesure', 'justificatif_etude', 'echeance', 'suivi_indicateurs']

    def create(self, validated_data):
        # Extraire les suivi_indicateurs avant de sauvegarder
        suivi_indicateurs_data = validated_data.pop('suivi_indicateurs')
        suivi = Suivi.objects.create(**validated_data)

        # Créer les SuiviIndicateurs associés
        for indicateur_data in suivi_indicateurs_data:
            SuiviIndicateur.objects.create(suivi=suivi, **indicateur_data)

        return suivi

class EngagementIndicateurSerializer(serializers.ModelSerializer):
    entreprise = serializers.PrimaryKeyRelatedField(queryset=Entreprise.objects.all())
    indicateur = serializers.PrimaryKeyRelatedField(queryset=Indicateur.objects.all())
    engagement_aspect= serializers.PrimaryKeyRelatedField(queryset=EngagementAspect.objects.all())

    aspects = serializers.SerializerMethodField()

    class Meta:
        model = EngagementIndicateur
        fields = ['id_engagement_indicateur', 'engagement_aspect','entreprise', 'indicateur', 'aspects']

    def get_aspects(self, obj):
        aspects = obj.aspects.all()
        return EngagementAspectSerializer(aspects, many=True).data
class EngagementAspectSerializer(serializers.ModelSerializer):
    echeances = serializers.SerializerMethodField()

    class Meta:
        model = EngagementAspect
        fields = ['id_engagement_aspect', 'lieu_prelevement',
                  'methode_equipement', 'frequence', 'responsabilite', 'date_creation', 'echeances']

    def get_echeances(self, obj):
        echeances = obj.echeances.all()
        return EcheanceSerializer(echeances, many=True).data
    def validate(self, data):
        """
        Validation pour empêcher la création de plusieurs engagements
        pour un même indicateur pour la même entreprise.
        """
        entreprise = data.get('id_entreprise')
        indicateur = data.get('id_indicateur')

        # Vérifie si un engagement similaire existe
        if EngagementIndicateur.objects.filter(id_entreprise=entreprise, id_indicateur=indicateur).exists():
            raise serializers.ValidationError("Cet indicateur est déjà associé à cette entreprise.")
        return data


class IndicateurSerializer(serializers.ModelSerializer):
    id_aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())

    class Meta:
        model = Indicateur
        fields = ['nom', 'seuil_max', 'unite', 'id_aspect']


class AspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = '__all__'
