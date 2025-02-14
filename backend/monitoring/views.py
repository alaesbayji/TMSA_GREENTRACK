from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EntrepriseMere, Entreprise, Aspect, Indicateur, Utilisateur,PrefectureProvince,Commune,EngagementIndicateur,Suivi,SuiviIndicateur,EngagementAspect
from .serializers import (
    EntrepriseMereSerializer, 
    EntrepriseSerializer, 
    AspectSerializer, 
    IndicateurSerializer,
    SignupSerializer,
    LoginSerializer,PrefectureProvinceSerializer,CommuneSerializer,EngagementIndicateurSerializer,SuiviSerializer,EngagementAspectSerializer,SuiviIndicateurSerializer
)
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from .permissions import IsAdminUser, IsResponsableEntreprise, IsResponsableSuivi


# Authentication Views
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            utilisateur = serializer.save()
            return Response({
                "idUtilisateur": utilisateur.idUtilisateur,
                "nom": utilisateur.nom,
                "prenom": utilisateur.prenom,
                "email": utilisateur.email,
                "role": request.data.get('role'),
                "message": "Inscription réussie"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=request.data['email'], password=request.data['password'])
            if not user:
                return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "Token valide !",
            "user": {
                "email": request.user.email,
                "id": request.user.idUtilisateur
            }
        })

# EntrepriseMere Views
class EntrepriseMereListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = EntrepriseMere.objects.all()
    serializer_class = EntrepriseMereSerializer


class EntrepriseMereRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = EntrepriseMere.objects.all()
    serializer_class = EntrepriseMereSerializer


# Entreprise Views
class EntrepriseListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer


class EntrepriseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer


# Aspect Views
class AspectListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Aspect.objects.all()
    serializer_class = AspectSerializer


class AspectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Aspect.objects.all()
    serializer_class = AspectSerializer


# Indicateur Views
class IndicateurListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer


class IndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer
class ProvinceListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = PrefectureProvince.objects.all()
    serializer_class = PrefectureProvinceSerializer

class ProvinceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PrefectureProvince.objects.all()
    serializer_class = PrefectureProvinceSerializer
class CommuneListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer


class CommuneRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
class EngagementCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementIndicateur.objects.all()
    serializer_class = EngagementIndicateurSerializer

from dateutil.relativedelta import relativedelta

class EngagementAspectCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementAspect.objects.all()
    serializer_class = EngagementAspectSerializer

    def perform_create(self, serializer):
        engagement = serializer.save()

        if engagement.frequence <= 0:
            raise serializers.ValidationError({"frequence": "La fréquence doit être supérieure à zéro."})

        engagement.generer_prochaine_echeance()

class EngagementAspectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementAspect.objects.all()
    serializer_class = EngagementAspectSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().update(request, *args, **kwargs)
        instance.generer_prochaine_echeance()
        return response

class EngagementIndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementIndicateur.objects.all()
    serializer_class = EngagementIndicateurSerializer

class SuiviListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Suivi.objects.all()
    serializer_class = SuiviSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        id_engagement_aspect = data.get('id_engagement_aspect')
        suivi_indicateurs_data = data.get('suivi_indicateurs', [])

        if not id_engagement_aspect:
            return Response({"error": "EngagementAspect est obligatoire."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification de tous les indicateurs attendus
        engagement_indicateurs_attendus = EngagementIndicateur.objects.filter(
            id_engagement_aspect_id=id_engagement_aspect
        ).values_list('id_engagement_indicateur', flat=True)

        engagement_indicateurs_reçus = {item['engagement_indicateur'] for item in suivi_indicateurs_data}
        indicateurs_manquants = set(engagement_indicateurs_attendus) - engagement_indicateurs_reçus

        if indicateurs_manquants:
            return Response(
                {"error": f"Les EngagementIndicateurs suivants sont manquants: {list(indicateurs_manquants)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Création de l'instance principale
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            suivi_instance = serializer.save()

            # Création des SuiviIndicateurs associés
            for indicateur_data in suivi_indicateurs_data:
                SuiviIndicateur.objects.create(suivi=suivi_instance, **indicateur_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SuiviRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Suivi.objects.all()
    serializer_class = SuiviSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Mise à jour des champs simples, sauf clôture
        cloture_demande = request.data.get("cloturer", False)
        request_data = request.data.copy()
        request_data.pop("cloturer", None)  # On retire temporairement la clôture

        serializer = self.get_serializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Mise à jour ou création des suivi_indicateurs
        suivi_indicateurs_data = request.data.get("suivi_indicateurs", [])
        for ind_data in suivi_indicateurs_data:
            engagement_id = ind_data.get("engagement_indicateur")
            valeur_mesure = ind_data.get("valeur_mesure")
            observations = ind_data.get("observations")

            # Récupérer ou créer l'indicateur
            suivi_ind, created = SuiviIndicateur.objects.get_or_create(
                suivi=instance,
                engagement_indicateur_id=engagement_id,
                defaults={
                    "valeur_mesure": valeur_mesure,
                    "observations": observations
                }
            )
            if not created:
                # Mettre à jour si l'indicateur existe déjà
                suivi_ind.valeur_mesure = valeur_mesure
                suivi_ind.observations = observations
                suivi_ind.save()

                # Passer la requête au sérialiseur pour la mise à jour
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class SuiviIndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = SuiviIndicateur.objects.all()
    serializer_class = SuiviIndicateurSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Empêcher la modification si le Suivi est clôturé
        if instance.suivi.cloturer:
            return Response({"error": "Le suivi associé est clôturé. Modification impossible."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Empêcher la suppression si le Suivi est clôturé
        if instance.suivi.cloturer:
            return Response({"error": "Le suivi associé est clôturé. Suppression impossible."}, status=status.HTTP_400_BAD_REQUEST)

        return super().destroy(request, *args, **kwargs)


class EntrepriseAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Entreprise.objects.prefetch_related(
        'engagements_aspects__suivis__suivi_indicateurs',
        'engagements_aspects__engagements_indicateurs',
        'engagements_aspects__echeances'
    ).all()
    serializer_class = EntrepriseSerializer