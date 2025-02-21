from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser

from ..models.enterprise_models import EntrepriseMere, Entreprise,SecteurActivite, ActiviteIndustrielle
from ..serializers.enterprise_serializers import EntrepriseMereSerializer, EntrepriseSerializer,SecteurActiviteSerializer, ActiviteIndustrielleSerializer
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

class SecteurListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = SecteurActivite.objects.all()
    serializer_class = SecteurActiviteSerializer


class SecteurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = SecteurActivite.objects.all()
    serializer_class = SecteurActiviteSerializer
class ActiviteIndusListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ActiviteIndustrielle.objects.all()
    serializer_class = ActiviteIndustrielleSerializer


class ActiviteIndusRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ActiviteIndustrielle.objects.all()
    serializer_class = ActiviteIndustrielleSerializer