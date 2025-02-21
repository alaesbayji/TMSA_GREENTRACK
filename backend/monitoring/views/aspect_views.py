from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.aspect_models import Aspect, Indicateur, SousAspectEau, IndicateurEauPollution
from ..serializers.aspect_serializers import AspectSerializer, IndicateurSerializer, SousAspectEauPollutionSerializer, IndicateurEauPollutionSerializer
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
    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer


class IndicateurRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Indicateur.objects.all()
    serializer_class = IndicateurSerializer