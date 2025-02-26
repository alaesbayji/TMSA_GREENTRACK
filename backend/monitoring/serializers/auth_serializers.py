from rest_framework import serializers
from ..models.user_models import Utilisateur, ResponsableEntreprise, ResponsableSuiviTMSA, Admin
from ..models.enterprise_models import Entreprise
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.models import Group
from django.db import IntegrityError  # Ajouté pour gérer les erreurs d'intégrité  
from django.utils import timezone
from ..models.Map_models import Zone
from .enterprise_serializers  import EntrepriseSerializer  
from ..serializers.map_serializers import ZoneSerializer

class SignupSerializer(serializers.ModelSerializer):
    id_entreprise = EntrepriseSerializer(read_only=True)  # Inclure les détails de l'entreprise
    id_zone = ZoneSerializer(read_only=True)
    role = serializers.CharField(write_only=True)
    
    class Meta:
        model = Utilisateur
        fields = ('nom', 'prenom', 'email', 'password', 'id_entreprise', 'id_zone', 'role')
        extra_kwargs = {
            'password': {'write_only': True},
            'id_entreprise': {'required': False},
            'id_zone': {'required': False}
        }

    def create(self, validated_data):
        role = validated_data.pop('role', None)

        with transaction.atomic():
            if role == 'ResponsableEntreprise':
                validated_data.pop('id_zone', None)
                user = ResponsableEntreprise.objects.create(**validated_data)
                group = Group.objects.get(name='ResponsableEntreprise')

            elif role == 'ResponsableSuiviTMSA':
                validated_data.pop('id_entreprise', None)
                user = ResponsableSuiviTMSA.objects.create(**validated_data)
                group = Group.objects.get(name='ResponsableSuiviTMSA')

            elif role == 'Admin':
                validated_data.pop('id_zone', None)
                validated_data.pop('id_entreprise', None)
                user = Admin.objects.create(**validated_data)
                group = Group.objects.get(name='Admin')

            else:
                raise serializers.ValidationError("Rôle invalide")

            user.set_password(validated_data["password"])
            user.groups.add(group)  # Assigner le groupe correspondant
            user.save()
            return user

    def validate(self, data):
        role = data.get('role')
        if role == 'ResponsableEntreprise' and not data.get('id_entreprise'):
            raise serializers.ValidationError("L'id de l'entreprise est requis pour ResponsableEntreprise.")
        if role == 'ResponsableSuiviTMSA' and not data.get('id_zone'):
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