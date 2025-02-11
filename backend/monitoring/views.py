from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EntrepriseMere, Entreprise, Aspect, Indicateur, Utilisateur,PrefectureProvince,Commune,EngagementIndicateur,Suivi,Echeance,EngagementAspect
from .serializers import (
    EntrepriseMereSerializer, 
    EntrepriseSerializer, 
    AspectSerializer, 
    IndicateurSerializer,
    SignupSerializer,
    LoginSerializer,PrefectureProvinceSerializer,CommuneSerializer,EngagementIndicateurSerializer,SuiviSerializer,EcheanceSerializer,EngagementAspectSerializer
)
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate


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
    permission_classes = [AllowAny]
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

class EngagementAspectCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementAspect.objects.all()
    serializer_class = EngagementAspectSerializer

    def perform_create(self, serializer):
        engagement = serializer.save()
        date_creation = engagement.date_creation
        frequence = engagement.frequence
        
        # Vérification que la fréquence est valide
        if frequence <= 0:
            raise ValueError("La fréquence doit être supérieure à zéro.")

        intervalle_mois = 12 // frequence
        date_debut = date_creation + relativedelta(months=intervalle_mois)  # Première échéance après intervalle

        for i in range(frequence):
            date_echeance = date_debut + relativedelta(months=(i * intervalle_mois))
            Echeance.objects.create(
                id_engagement_aspect=engagement,
                date_limite=date_echeance,
                statut='en attente'
            )
class EngagementAspectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementAspect.objects.all()
    serializer_class = EngagementAspectSerializer
class EngagementIndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = EngagementIndicateur.objects.all()
    serializer_class = EngagementIndicateurSerializer
class SuiviListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SuiviSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Mise à jour de l'échéance si présente
            echeance = serializer.instance.echeance
            if echeance:
                echeance.statut = 'effectuee'
                echeance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SuiviRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Suivi.objects.all()
    serializer_class = SuiviSerializer

class EcheanceUpdateView(APIView):
    def post(self, request, id_echeance):
        try:
            echeance = Echeance.objects.get(id_echeance=id_echeance)
            echeance.statut = 'effectuee'
            echeance.save()

            return Response({"message": "Echéance mise à jour"}, status=status.HTTP_200_OK)
        except Echeance.DoesNotExist:
            return Response({"error": "Echéance introuvable"}, status=status.HTTP_404_NOT_FOUND)
class EcheanceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Echeance.objects.all()
    serializer_class = EcheanceSerializer
class EcheanceByEntrepriseView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EcheanceSerializer

    def get_queryset(self):
        id_entreprise = self.kwargs['id_entreprise']
        return Echeance.objects.filter(engagement__id_entreprise=id_entreprise)



