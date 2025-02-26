from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.response import Response

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
    def get(self, request):
        queryset = Entreprise.objects.select_related('id_activite').all()
        serializer_class = EntrepriseSerializer(queryset, many=True)
        return Response(serializer_class.data)
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
class ActiviteIndusListCreateViewbyid(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ActiviteIndustrielle.objects.all()
    serializer_class = ActiviteIndustrielleSerializer
    def get_queryset(self):  
        queryset = self.queryset  
        id_secteur = self.request.query_params.get('id_secteur', None)  
        if id_secteur is not None:  
            queryset = queryset.filter(id_secteur=id_secteur)  # Filtrer par id_pref_prov  
        return queryset 
class ActiviteIndusListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    def get(self, request):
        queryset = ActiviteIndustrielle.objects.select_related('id_secteur').all()
        serializer_class = ActiviteIndustrielleSerializer(queryset, many=True)
        return Response(serializer_class.data)
class ActiviteIndusRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ActiviteIndustrielle.objects.all()
    serializer_class = ActiviteIndustrielleSerializer