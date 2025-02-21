from rest_framework import serializers
from .models import  (Utilisateur,   SecteurActivite,  
    ActiviteIndustrielle,  
    IndicateurEauPollution,  
    SousAspectEau,  
    EngagementSousAspectEauPollution,  
    EngagementIndicateurSousAspect,  
    SuiviSousAspect,  
    SuiviIndicateurSousAspect , ResponsableEntreprise, Admin, SuiviIndicateur,ResponsableSuiviTMSA, EntrepriseMere, Entreprise, EngagementAspect,PrefectureProvince, Commune, EngagementIndicateur, Suivi, Indicateur, Aspect,ActiviteIndustrielle)
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.models import Group
from django.db import IntegrityError  # Ajouté pour gérer les erreurs d'intégrité  
from django.utils import timezone

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
                group = Group.objects.get(name='ResponsableEntreprise')

            elif role == 'ResponsableSuiviTMSA':
                validated_data.pop('id_entreprise', None)
                user = ResponsableSuiviTMSA.objects.create(**validated_data)
                group = Group.objects.get(name='ResponsableSuiviTMSA')

            elif role == 'Admin':
                validated_data.pop('zone_de_suivi', None)
                validated_data.pop('id_entreprise', None)
                user = Admin.objects.create(**validated_data)
                group = Group.objects.get(name='Admin')

            else:
                raise serializers.ValidationError("Rôle invalide")

            user.set_password(validated_data["password"])
            user.groups.add(group)  # Assigne le groupe
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


class PrefectureProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefectureProvince
        fields = ('id_pref_prov', 'nom')


class CommuneSerializer(serializers.ModelSerializer):
    id_pref_prov = serializers.PrimaryKeyRelatedField(queryset=PrefectureProvince.objects.all())

    class Meta:
        model = Commune
        fields = ('id_commune', 'nom', 'id_pref_prov')

class SuiviIndicateurSerializer(serializers.ModelSerializer):
    suivi = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SuiviIndicateur
        fields = ['id_suivi_indicateur', 'suivi', 'engagement_indicateur', 'valeur_mesure', 'observations']

class SuiviSerializer(serializers.ModelSerializer):
    suivi_indicateurs = SuiviIndicateurSerializer(many=True, required=False)

    class Meta:
        model = Suivi
        fields = ['id_suivi', 'id_engagement_aspect', 'date_mesure', 'date_limite', 'justificatif_etude', 'statut', 'cloturer', 'suivi_indicateurs']

    def validate(self, data):
        instance = self.instance

        # Empêcher toute modification si le Suivi est déjà clôturé
        if instance and instance.cloturer:
            raise serializers.ValidationError("Ce suivi est déjà clôturé et ne peut plus être modifié.")

        # Vérifier si le Suivi est en cours de clôture
        if data.get('cloturer', False):
            # Récupérer l'EngagementAspect associé
            engagement_aspect = instance.id_engagement_aspect

            # Récupérer tous les EngagementIndicateur associés à cet EngagementAspect
            engagement_indicateurs_attendus = EngagementIndicateur.objects.filter(
                id_engagement_aspect=engagement_aspect
            ).values_list('id_engagement_indicateur', flat=True)

            # Récupérer les SuiviIndicateur existants en base de données pour ce Suivi
            suivi_indicateurs_existants = SuiviIndicateur.objects.filter(
                suivi=instance
            ).values_list('engagement_indicateur', flat=True)

            # Vérifier que tous les EngagementIndicateur ont des SuiviIndicateur existants
            indicateurs_manquants = set(engagement_indicateurs_attendus) - set(suivi_indicateurs_existants)
            if indicateurs_manquants:
                raise serializers.ValidationError(
                    f"Les EngagementIndicateurs suivants sont manquants de SuiviIndicateurs: {list(indicateurs_manquants)}"
                )

        return data

    def update(self, instance, validated_data):
        # Empêcher la modification si le Suivi est déjà clôturé
        if instance.cloturer:
            raise serializers.ValidationError("Ce suivi est déjà clôturé et ne peut plus être modifié.")

        # Mettre à jour les champs de l'objet Suivi
        instance.date_mesure = validated_data.get('date_mesure', instance.date_mesure)
        instance.justificatif_etude = validated_data.get('justificatif_etude', instance.justificatif_etude)
        instance.save()

        # Si le champ 'cloturer' est passé à True, clôturer le Suivi
        if validated_data.get('cloturer', False):
            instance.cloturer = True
            instance.date_mesure = timezone.now().date()  # Date actuelle
            instance.mettre_a_jour_statut()  # Mettre à jour le statut
            instance.save()

            # Générer une nouvelle échéance et créer un nouveau Suivi
            engagement_aspect = instance.id_engagement_aspect
            engagement_aspect.generer_prochaine_echeance()

        return instance
class EngagementIndicateurSerializer(serializers.ModelSerializer):
    id_indicateur = serializers.PrimaryKeyRelatedField(queryset=Indicateur.objects.all())
    id_engagement_aspect = serializers.PrimaryKeyRelatedField(queryset=EngagementAspect.objects.all())

    class Meta:
        model = EngagementIndicateur
        fields = ['id_engagement_indicateur', 'id_engagement_aspect', 'id_indicateur']

    def create(self, validated_data):
        try:
            return EngagementIndicateur.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Cet indicateur est déjà associé à cet engagement aspect.")


class EngagementAspectSerializer(serializers.ModelSerializer):
    id_entreprise = serializers.PrimaryKeyRelatedField(queryset=Entreprise.objects.all())
    id_aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())
    id_sous_aspect_eau = serializers.PrimaryKeyRelatedField(queryset=SousAspectEau.objects.all(), required=False , allow_null=True)  # Rendre optionnel
    engagements_indicateurs = EngagementIndicateurSerializer(many=True, read_only=True)
    suivis = SuiviSerializer(many=True, read_only=True)

    class Meta:
        model = EngagementAspect
        fields = [
            'id_engagement_aspect', 'id_aspect', 'id_sous_aspect_eau', 'id_entreprise', 
            'lieu_prelevement', 'methode_equipement', 'frequence', 'responsabilite', 
            'date_creation', 'engagements_indicateurs', 'suivis', 'date_prochaine_echeance'
        ]

    def validate(self, data):
        aspect = data.get('id_aspect')
        sous_aspect_eau = data.get('id_sous_aspect_eau')

        # Si l'aspect est "Eau", le sous-aspect est obligatoire
        if aspect.est_eau and not sous_aspect_eau:
            raise serializers.ValidationError({"id_sous_aspect_eau": "Un sous-aspect est requis pour l'aspect Eau."})

        # Si le sous-aspect est "Eau Pollution", utiliser le traitement spécifique
        if sous_aspect_eau and sous_aspect_eau.est_pollution:
            raise serializers.ValidationError({"id_sous_aspect_eau": "Pour l'Eau Pollution, utilisez EngagementSousAspectEauPollution."})

        return data

    def create(self, validated_data):
        try:
            engagement = EngagementAspect.objects.create(**validated_data)
            return engagement
        except IntegrityError as e:
            raise serializers.ValidationError({"error": f"Erreur d'intégrité : {str(e)}"})

    def update(self, instance, validated_data):
        instance.id_aspect = validated_data.get('id_aspect', instance.id_aspect)
        instance.id_entreprise = validated_data.get('id_entreprise', instance.id_entreprise)
        instance.lieu_prelevement = validated_data.get('lieu_prelevement', instance.lieu_prelevement)
        instance.methode_equipement = validated_data.get('methode_equipement', instance.methode_equipement)
        instance.frequence = validated_data.get('frequence', instance.frequence)
        instance.responsabilite = validated_data.get('responsabilite', instance.responsabilite)
        instance.date_creation = validated_data.get('date_creation', instance.date_creation)
        instance.date_prochaine_echeance = validated_data.get('date_prochaine_echeance', instance.date_prochaine_echeance)

        try:
            instance.save()
            instance.generer_prochaine_echeance()  # Régénérer la prochaine échéance
        except IntegrityError as e:
            raise serializers.ValidationError({"error": f"Erreur d'intégrité : {str(e)}"})

        return instance
class IndicateurSerializer(serializers.ModelSerializer):
    id_aspect = serializers.PrimaryKeyRelatedField(queryset=Aspect.objects.all())

    class Meta:
        model = Indicateur
        fields = ['nom', 'seuil_max', 'unite', 'id_aspect']


class AspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = ['id_aspect', 'typeMilieu', 'description', 'est_eau']

    
class EntrepriseSerializer(serializers.ModelSerializer):
    engagements_aspects = EngagementAspectSerializer(many=True, read_only=True)
    id_activite = serializers.PrimaryKeyRelatedField(queryset=ActiviteIndustrielle.objects.all())  

    class Meta:
        model = Entreprise
        fields = ['id_entreprise', 'id_entreprise_mere', 'id_commune','id_activite' ,'nom', 'adresse', 'zone', 
                  'montant_investissement', 'nombre_emploi', 'superficie_totale', 
                  'secteur_dominant', 'prefecture_province', 'DAE', 'EIE_PSSE', 'engagements_aspects']

class SecteurActiviteSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = SecteurActivite  
        fields = ['id_secteur', 'nom']  

class ActiviteIndustrielleSerializer(serializers.ModelSerializer):  
    id_secteur = serializers.PrimaryKeyRelatedField(queryset=SecteurActivite.objects.all())  

    class Meta:  
        model = ActiviteIndustrielle  
        fields = ['id_activite', 'nom', 'id_secteur']  

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

class EngagementSousAspectEauPollutionSerializer(serializers.ModelSerializer):
    id_entreprise = serializers.PrimaryKeyRelatedField(queryset=Entreprise.objects.all())
    id_sous_aspect = serializers.PrimaryKeyRelatedField(queryset=SousAspectEau.objects.all())

    class Meta:
        model = EngagementSousAspectEauPollution
        fields = [
            'id_engagement_sous_aspect', 'id_entreprise', 'id_sous_aspect',
            'lieu_prelevement', 'methode_equipement', 'frequence',
            'responsabilite', 'date_creation', 'date_prochaine_echeance'
        ]

    def create(self, validated_data):
        try:
            # Créer l'engagement sous-aspect
            engagement = EngagementSousAspectEauPollution.objects.create(**validated_data)

            # Récupérer l'activité de l'entreprise
            id_entreprise = validated_data['id_entreprise']
            activite_entreprise = id_entreprise.id_activite  # Supposons que l'entreprise a un champ `id_activite`

            # Récupérer tous les indicateurs associés à cette activité
            indicateurs = IndicateurEauPollution.objects.filter(id_activite=activite_entreprise)

            # Créer automatiquement les EngagementIndicateurSousAspect pour chaque indicateur
            for indicateur in indicateurs:
                EngagementIndicateurSousAspect.objects.create(
                    id_engagement_sous_aspect=engagement,
                    id_indicateur_eaupollution=indicateur
                )

            return engagement
        except IntegrityError:
            raise serializers.ValidationError("Cet engagement est déjà associé à cet aspect.")

    def update(self, instance, validated_data):  
        instance.lieu_prelevement = validated_data.get('lieu_prelevement', instance.lieu_prelevement)  
        instance.methode_equipement = validated_data.get('methode_equipement', instance.methode_equipement)  
        instance.frequence = validated_data.get('frequence', instance.frequence)  
        instance.responsabilite = validated_data.get('responsabilite', instance.responsabilite)  
        instance.date_creation = validated_data.get('date_creation', instance.date_creation)  
        instance.date_prochaine_echeance = validated_data.get('date_prochaine_echeance', instance.date_prochaine_echeance)  

        try:  
            instance.save()  
        except IntegrityError:  
            raise serializers.ValidationError("Cet engagement est déjà associé à cet aspect.")  
        
        instance.generer_prochaine_echeance()  
        return instance  

class EngagementIndicateurSousAspectSerializer(serializers.ModelSerializer):  
    id_indicateur_eaupollution = serializers.PrimaryKeyRelatedField(queryset=IndicateurEauPollution.objects.all())  
    id_engagement_sous_aspect = serializers.PrimaryKeyRelatedField(queryset=EngagementSousAspectEauPollution.objects.all())  

    class Meta:  
        model = EngagementIndicateurSousAspect  
        fields = ['id_engagement_indicateur_sous_aspect', 'id_indicateur_eaupollution', 'id_engagement_sous_aspect']  

    def create(self, validated_data):  
        try:  
            return EngagementIndicateurSousAspect.objects.create(**validated_data)  
        except IntegrityError:  
            raise serializers.ValidationError("Cet indicateur est déjà associé à cet engagement sous aspect.")  
class SuiviIndicateurSousAspectSerializer(serializers.ModelSerializer):  
    suivi = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:  
        model = SuiviIndicateurSousAspect  
        fields = ['id_suivi_indicateur_sous_aspect', 'suivi',   
                  'engagement_indicateur_sous_aspect', 'valeur_mesure', 'observations']  

    def create(self, validated_data):  
        try:  
            return SuiviIndicateurSousAspect.objects.create(**validated_data)  
        except IntegrityError:  
            raise serializers.ValidationError("Ce suivi indicateur est déjà enregistré.")
class SuiviSousAspectSerializer(serializers.ModelSerializer):
    id_engagement_sous_aspect = serializers.PrimaryKeyRelatedField(queryset=EngagementSousAspectEauPollution.objects.all())
    suivi_indicateurs_sous_aspect = SuiviIndicateurSousAspectSerializer(many=True, required=False)

    class Meta:
        model = SuiviSousAspect
        fields = ['id_suivi_sous_aspect', 'id_engagement_sous_aspect', 
                  'date_mesure', 'date_limite', 'justificatif_etude', 'statut', 'cloturer','suivi_indicateurs_sous_aspect']

    def validate(self, data):
        instance = self.instance

        # Empêcher toute modification si le Suivi est déjà clôturé
        if instance and instance.cloturer:
            raise serializers.ValidationError("Ce suivi est déjà clôturé et ne peut plus être modifié.")

        # Vérifier si le Suivi est en cours de clôture
        if data.get('cloturer', False):
            # Récupérer l'EngagementSousAspect associé
            engagement_sous_aspect = instance.id_engagement_sous_aspect

            # Récupérer tous les EngagementIndicateurSousAspect associés à cet EngagementSousAspect
            engagement_indicateurs_attendus = EngagementIndicateurSousAspect.objects.filter(
                id_engagement_sous_aspect=engagement_sous_aspect
            ).values_list('id_engagement_indicateur_sous_aspect', flat=True)

            # Récupérer les SuiviIndicateurSousAspect existants en base de données pour ce Suivi
            suivi_indicateurs_existants = SuiviIndicateurSousAspect.objects.filter(
                suivi=instance
            ).values_list('engagement_indicateur_sous_aspect', flat=True)

            # Vérifier que tous les EngagementIndicateurSousAspect ont des SuiviIndicateurSousAspect existants
            indicateurs_manquants = set(engagement_indicateurs_attendus) - set(suivi_indicateurs_existants)
            if indicateurs_manquants:
                raise serializers.ValidationError(
                    f"Les EngagementIndicateursSousAspect suivants sont manquants de SuiviIndicateursSousAspect: {list(indicateurs_manquants)}{list(engagement_indicateurs_attendus)}{list(suivi_indicateurs_existants)}"
                )

        return data

    def update(self, instance, validated_data):
        # Empêcher la modification si le Suivi est déjà clôturé
        if instance.cloturer:
            raise serializers.ValidationError("Ce suivi est déjà clôturé et ne peut plus être modifié.")

        # Mettre à jour les champs de l'objet Suivi
        instance.date_mesure = validated_data.get('date_mesure', instance.date_mesure)
        instance.justificatif_etude = validated_data.get('justificatif_etude', instance.justificatif_etude)
        instance.save()

        # Si le champ 'cloturer' est passé à True, clôturer le Suivi
        if validated_data.get('cloturer', False):
            instance.cloturer = True
            instance.date_mesure = timezone.now().date()  # Date actuelle
            instance.mettre_a_jour_statut()  # Mettre à jour le statut
            instance.save()

            # Générer une nouvelle échéance et créer un nouveau Suivi
            engagement_sous_aspect = instance.id_engagement_sous_aspect
            engagement_sous_aspect.generer_prochaine_echeance()

        return instance

