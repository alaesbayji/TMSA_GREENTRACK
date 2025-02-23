from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser

from ..models.enterprise_models import EntrepriseMere, Entreprise,SecteurActivite, ActiviteIndustrielle
from ..serializers.enterprise_serializers import EntrepriseMereSerializer, EntrepriseSerializer,SecteurActiviteSerializer, ActiviteIndustrielleSerializer
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
    def perform_create(self, serializer):  
        instance = serializer.save() 

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
    def get_queryset(self):  
        queryset = self.queryset  
        id_secteur = self.request.query_params.get('id_secteur', None)  
        if id_secteur is not None:  
            queryset = queryset.filter(id_secteur=id_secteur)  # Filtrer par id_pref_prov  
        return queryset 

class ActiviteIndusRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ActiviteIndustrielle.objects.all()
    serializer_class = ActiviteIndustrielleSerializer