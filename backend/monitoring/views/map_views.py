from rest_framework import generics,status
from ..models.Map_models import PrefectureProvince, Commune,Parcelle,Zone
from ..serializers.map_serializers import PrefectureProvinceSerializer, CommuneSerializer,ParcelleSerializer,ZoneSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
import geopandas as gpd
from django.http import JsonResponse
from rest_framework.views import APIView  
import zipfile
import io
import geopandas as gpd
from rest_framework.response import Response

class ProvinceListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = PrefectureProvince.objects.all()
    serializer_class = PrefectureProvinceSerializer

class ProvinceRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = PrefectureProvince.objects.all()
    serializer_class = PrefectureProvinceSerializer
class ZoneListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class ZoneRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

class CommuneListCreateViewbyid_pref_prov(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    def get_queryset(self):  
        queryset = self.queryset  
        id_pref_prov = self.request.query_params.get('id_pref_prov', None)  
        if id_pref_prov is not None:  
            queryset = queryset.filter(id_pref_prov=id_pref_prov)  # Filtrer par id_pref_prov  
        return queryset  
class CommuneListCreateView(generics.ListCreateAPIView):  
    permission_classes = [AllowAny]

    queryset = Commune.objects.all()  
    serializer_class = CommuneSerializer  
class ParcelleListCreateView(generics.ListCreateAPIView):  
    permission_classes = [AllowAny]

    queryset = Parcelle.objects.all()  
    serializer_class = ParcelleSerializer  

class ParcelleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):  
    permission_classes = [AllowAny]

    queryset = Parcelle.objects.all()  
    serializer_class = ParcelleSerializer  
class CommuneRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer

import geopandas as gpd
from shapely.wkt import dumps
from django.http import JsonResponse
from django.views import View
import os
from django.conf import settings

class ImportShapefileView(APIView):  
    permission_classes = [AllowAny]  

    def post(self, request):  
        # Récupérer le fichier Shapefile depuis la requête  
        shapefile = request.FILES.get('shapefile')  
        if not shapefile:  
            return JsonResponse({"error": "Aucun fichier Shapefile trouvé."}, status=400)  

        try:  
            # Sauvegarder temporairement le fichier Shapefile  
            temp_dir = settings.MEDIA_ROOT  
            shapefile_path = os.path.join(temp_dir, shapefile.name)  

            with open(shapefile_path, 'wb+') as destination:  
                for chunk in shapefile.chunks():  
                    destination.write(chunk)  

            # Lire le Shapefile avec GeoPandas  
            gdf = gpd.read_file(shapefile_path)  

            # Vérifiez si le GeoDataFrame contient des géométries valides  
            if gdf.empty or 'geometry' not in gdf.columns:  
                return JsonResponse({"error": "Le shapefile ne contient pas de géométries."}, status=400)  

            # Assurez-vous que le GeoDataFrame a un SRID valide  
            if gdf.crs is None:  
                return JsonResponse({"error": "Le shapefile ne contient pas de système de référence spatiale (CRS)."}, status=400)  

            # Reprojeter en EPSG:4326 si le CRS n'est pas déjà le bon  
            if gdf.crs.to_string() != 'EPSG:26191':  
                gdf = gdf.to_crs(epsg=26191)  # Transformer en WGS84  

            # Convertir les géométries en WKT et les insérer dans la base de données  
            for geom in gdf.geometry:  
                # Convertir la géométrie en WKT  
                wkt_geom = dumps(geom)  

                # Créer une nouvelle instance de Parcelle  
                parcelle = Parcelle(geom=wkt_geom)  
                parcelle.save()  

            # Supprimer le fichier temporaire  
            os.remove(shapefile_path)  

            return JsonResponse({"status": "success", "message": "Shapefile importé avec succès."}, status=201)  

        except Exception as e:  
            # En cas d'erreur, supprimez le fichier temporaire s'il a été créé  
            if os.path.exists(shapefile_path):  
                os.remove(shapefile_path)  
            return JsonResponse({"error": str(e)}, status=500)