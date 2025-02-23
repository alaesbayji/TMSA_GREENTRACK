from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..models.user_models import Utilisateur
from ..serializers.auth_serializers import SignupSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from ..permissions import IsAdminUser, IsResponsableEntreprise, IsResponsableSuivi

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

            # Déterminer le rôle en fonction des groupes de l'utilisateur
            if user.groups.filter(name='Admin').exists():
                role = 'Admin'
            elif user.groups.filter(name='ResponsableEntreprise').exists():
                role = 'ResponsableEntreprise'
            elif user.groups.filter(name='ResponsableSuiviTMSA').exists():
                role = 'ResponsableSuiviTMSA'
            else:
                role = 'Utilisateur'  # Rôle par défaut

            # Générer les tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "idUtilisateur": user.idUtilisateur,
                    "email": user.email,
                    "nom": user.nom,
                    "prenom": user.prenom,
                    "role": role,  # Retourner le rôle déterminé
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Déterminer le rôle en fonction des groupes de l'utilisateur
        if user.groups.filter(name='Admin').exists():
            role = 'Admin'
        elif user.groups.filter(name='ResponsableEntreprise').exists():
            role = 'ResponsableEntreprise'
        elif user.groups.filter(name='ResponsableSuiviTMSA').exists():
            role = 'ResponsableSuiviTMSA'
        else:
            role = 'Utilisateur'  # Rôle par défaut

        return Response({
            "message": "Token valide !",
            "user": {
                "email": user.email,
                "id": user.idUtilisateur,
                "role": role,  # Retourner le rôle déterminé
            }
        })