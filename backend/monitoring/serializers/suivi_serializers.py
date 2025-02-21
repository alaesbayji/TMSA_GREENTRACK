from rest_framework import serializers
from ..models.suivi_models import EngagementAspect, Suivi ,EngagementIndicateur,SuiviIndicateur,EngagementSousAspectEauPollution,EngagementIndicateurSousAspect,SuiviIndicateurSousAspect,SuiviSousAspect
from ..models.aspect_models import SousAspectEau,IndicateurEauPollution,Indicateur,Aspect
from ..models.suivi_models import Suivi
from ..models.enterprise_models import Entreprise

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

            # Récupérer l'id_sous_aspect  
            id_sous_aspect = validated_data['id_sous_aspect']  

            # Vérifier si est_pollution est True  
            if id_sous_aspect.est_pollution:  
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

