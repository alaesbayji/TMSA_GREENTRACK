from rest_framework import generics
from ..models.Map_models import PrefectureProvince, Commune
from ..serializers.map_serializers import PrefectureProvinceSerializer, CommuneSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

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