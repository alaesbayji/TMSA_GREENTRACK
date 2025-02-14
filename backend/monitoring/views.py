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

        # Vérifier que tous les EngagementIndicateur sont renseignés
        engagement_indicateurs_attendus = EngagementIndicateur.objects.filter(
            id_engagement_aspect_id=id_engagement_aspect
        ).values_list('id_engagement_indicateur', flat=True)

        engagement_indicateurs_reçus = [item['engagement_indicateur'] for item in suivi_indicateurs_data]

        indicateurs_manquants = set(engagement_indicateurs_attendus) - set(engagement_indicateurs_reçus)
        if indicateurs_manquants:
            return Response(
                {"error": f"Les EngagementIndicateurs suivants sont manquants de SuiviIndicateurs: {list(indicateurs_manquants)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Créer le Suivi et les SuiviIndicateur
        serializer = SuiviSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SuiviRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Suivi.objects.all()
    serializer_class = SuiviSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Empêcher la modification si le Suivi est déjà clôturé
        if instance.cloturer:
            return Response({"error": "Ce suivi est déjà clôturé et ne peut plus être modifié."}, status=status.HTTP_400_BAD_REQUEST)

        # Passer la requête au sérialiseur pour la mise à jour
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
class EntrepriseAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Entreprise.objects.prefetch_related(
        'engagements_aspects__suivis__suivi_indicateurs',
        'engagements_aspects__engagements_indicateurs',
        'engagements_aspects__echeances'
    ).all()
    serializer_class = EntrepriseSerializer