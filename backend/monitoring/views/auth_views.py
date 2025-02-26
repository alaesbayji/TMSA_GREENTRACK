from rest_framework import generics, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from ..models.user_models import Utilisateur,ResponsableEntreprise,ResponsableSuiviTMSA
from ..serializers.auth_serializers import SignupSerializer, LoginSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate
from ..permissions import IsAdminUser, IsResponsableEntreprise, IsResponsableSuivi

from django.core.mail import send_mail  
from django.conf import settings  

class SignupView(APIView):  
    permission_classes = [AllowAny]  

    def post(self, request):  
        serializer = SignupSerializer(data=request.data)  
        if serializer.is_valid():  
            utilisateur = serializer.save()  

            # Envoyer un email avec les informations d'identification  
            subject = 'Bienvenue dans TANGER MED SUSTAINABLE MONITORING'  
            message = (  
                f"Bonjour {utilisateur.prenom} {utilisateur.nom},\n\n"  
                f"Votre compte a été créé avec succès.\n"  
                f"Email : {utilisateur.email}\n"  
                f"Mot de passe : {request.data.get('password')} (Veuillez le changer dès que possible)\n\n"  
                "Merci de votre inscription !"  
            )  
            recipient_list = [utilisateur.email]  

            try:  
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)  
            except Exception as e:  
                return Response({"error": f"Erreur lors de l'envoi de l'email : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

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
class UpdateUserView(APIView):  
    permission_classes = [IsAuthenticated]  

    def put(self, request, pk):  
        try:  
            user = Utilisateur.objects.get(pk=pk)  
        except Utilisateur.DoesNotExist:  
            return Response({"error": "Utilisateur non trouvé."}, status=status.HTTP_404_NOT_FOUND)  

        serializer = SignupSerializer(user, data=request.data, partial=True)  # partial=True permet de ne mettre à jour que certains champs  
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)  

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ResponsableEntrepriseListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        queryset = ResponsableEntreprise.objects.select_related('id_entreprise__id_zone').all()
        serializer_class = SignupSerializer(queryset, many=True)
        return Response(serializer_class.data)

class ResponsableEntrepriseDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            responsable = ResponsableEntreprise.objects.get(pk=pk)
            responsable.delete()
            return Response({"message": "Responsable d'entreprise supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except ResponsableEntreprise.DoesNotExist:
            return Response({"error": "Responsable d'entreprise non trouvé."}, status=status.HTTP_404_NOT_FOUND)
class ResponsableEntrepriseUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            responsable = ResponsableEntreprise.objects.get(pk=pk)
            serializer = SignupSerializer(responsable, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ResponsableEntreprise.DoesNotExist:
            return Response({"error": "Responsable d'entreprise non trouvé."}, status=status.HTTP_404_NOT_FOUND)
class ResponsableSuiviListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ResponsableSuiviTMSA.objects.select_related('id_zone').all()
        serializer_class = SignupSerializer(queryset, many=True)
        return Response(serializer_class.data)
class ResponsableSuiviDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            responsable = ResponsableSuiviTMSA.objects.get(pk=pk)
            responsable.delete()
            return Response({"message": "Responsable d'entreprise supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)
        except ResponsableEntreprise.DoesNotExist:
            return Response({"error": "Responsable d'entreprise non trouvé."}, status=status.HTTP_404_NOT_FOUND)
class ResponsableSuiviUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            responsable = ResponsableSuiviTMSA.objects.get(pk=pk)
            serializer = SignupSerializer(responsable, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ResponsableEntreprise.DoesNotExist:
            return Response({"error": "Responsable d'entreprise non trouvé."}, status=status.HTTP_404_NOT_FOUND)