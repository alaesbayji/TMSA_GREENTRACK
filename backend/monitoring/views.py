from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import EntrepriseMere, Entreprise, Aspect, Indicateur, Utilisateur
from .serializers import (
    EntrepriseMereSerializer, 
    EntrepriseSerializer, 
    AspectSerializer, 
    IndicateurSerializer,
    SignupSerializer,
    LoginSerializer
)


# Authentication Views
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
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
                "id": request.user.id
            }
        })
# Modifiez vos vues existantes pour ajouter la permission
class EntrepriseMereListCreateView(generics.ListCreateAPIView):
    queryset = EntrepriseMere.objects.all()
    serializer_class = EntrepriseMereSerializer

# EntrepriseMere Views
class EntrepriseMereListCreateView(generics.ListCreateAPIView):
    queryset = EntrepriseMere.objects.all()
    serializer_class = EntrepriseMereSerializer


class EntrepriseMereRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EntrepriseMere.objects.all()
    serializer_class = EntrepriseMereSerializer


# Entreprise Views
class EntrepriseListCreateView(generics.ListCreateAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer


class EntrepriseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entreprise.objects.all()
    serializer_class = EntrepriseSerializer


# Aspect Views
class AspectListCreateView(generics.ListCreateAPIView):
    queryset = Aspect.objects.all()
    serializer_class = AspectSerializer


class AspectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Aspect.objects.all()
    serializer_class = AspectSerializer


# Indicateur Views
class IndicateurListCreateView(generics.ListCreateAPIView):
    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer


class IndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer