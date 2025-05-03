from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.aspect_models import Aspect, Indicateur, SousAspectEau, IndicateurEauPollution,IndicateurSousAspect
from ..serializers.aspect_serializers import IndicateurSousAspectSerializer,AspectSerializer, IndicateurSerializer, SousAspectEauPollutionSerializer, IndicateurEauPollutionSerializer
# Aspect Views
class AspectListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Aspect.objects.all()
    serializer_class = AspectSerializer


class AspectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Aspect.objects.all()
    serializer_class = AspectSerializer
class IndicateurEauPollutionListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = IndicateurEauPollution.objects.all()
    serializer_class = IndicateurEauPollutionSerializer


class IndicateurEauPollutionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = IndicateurEauPollution.objects.all()
    serializer_class = IndicateurEauPollutionSerializer
class SousAspectEauPollutionListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = SousAspectEau.objects.all()
    serializer_class = SousAspectEauPollutionSerializer

class SousAspectEauPollutionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = SousAspectEau.objects.all()
    serializer_class = SousAspectEauPollutionSerializer
# Indicateur Views
class IndicateurListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = IndicateurSerializer
    def get_queryset(self):
        # Filtrer les indicateurs liés à des aspects où est_eau = False
        return Indicateur.objects.filter(id_aspect__est_eau=False)

class IndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = IndicateurSerializer

class IndicateurSousAspectListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = IndicateurSousAspect.objects.all()
    serializer_class = IndicateurSousAspectSerializer
class IndicateurSousAspectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = IndicateurSousAspect.objects.all()
    serializer_class = IndicateurSousAspectSerializer