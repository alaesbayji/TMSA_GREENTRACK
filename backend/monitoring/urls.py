from django.urls import path  
from rest_framework_simplejwt.views import TokenRefreshView  
from . import views  
from .views.auth_views import(ResponsableEntrepriseDetailView,ResponsableSuiviDetailView, LoginView,SignupView,TestTokenView,UpdateUserView,ResponsableEntrepriseListView, ResponsableEntrepriseDeleteView,
    ResponsableEntrepriseUpdateView, ResponsableSuiviDeleteView,
    ResponsableSuiviUpdateView,ResponsableSuiviListView)

from .views.enterprise_views import (ActiviteIndusListCreateViewbyid,EntrepriseMereListCreateView,EntrepriseMereRetrieveUpdateDeleteView,EntrepriseListCreateView,EntrepriseRetrieveUpdateDeleteView,
ActiviteIndusListCreateView,ActiviteIndusRetrieveUpdateDeleteView,SecteurListCreateView,SecteurRetrieveUpdateDeleteView)

from .views.aspect_views import (IndicateurSousAspectRetrieveUpdateDeleteView,IndicateurSousAspectListCreateView,AspectListCreateView,AspectRetrieveUpdateDeleteView,IndicateurListCreateView,IndicateurRetrieveUpdateDeleteView,IndicateurEauPollutionListCreateView,IndicateurEauPollutionRetrieveUpdateDeleteView,
SousAspectEauPollutionListCreateView,SousAspectEauPollutionRetrieveUpdateDeleteView)

from .views.suivi_views import( EngagementIndicateurSousAspectCreateView,SuiviSousAspectListCreateView,EngagementSousAspectCreateView, EngagementCreateView,EngagementAspectCreateView,EngagementAspectRetrieveUpdateDeleteView,EngagementIndicateurRetrieveUpdateDeleteView,SuiviListCreateView,SuiviRetrieveUpdateDeleteView,
SuiviIndicateurRetrieveUpdateDeleteView,EngagementIndicateurSousAspectPollutionCreateView,EngagementSousAspectEauPollutionCreateView,EngagementSousAspectPollutionRetrieveUpdateDeleteView,SuiviSousAspectPollutionListCreateView,SuiviSousAspectPollutionRetrieveUpdateDeleteView,
SuiviIndicateurSousAspectPollutionRetrieveUpdateDeleteView)

from .views.map_views import CommuneListCreateViewbyid_pref_prov,ZoneListCreateView,ZoneRetrieveUpdateDeleteView,ImportShapefileView,CommuneListCreateView ,CommuneRetrieveUpdateDeleteView,ProvinceListCreateView,ProvinceRetrieveUpdateDeleteView,ParcelleListCreateView,ParcelleRetrieveUpdateDestroyView
urlpatterns = [  
    # Authentification  
    path('login/', LoginView.as_view(), name='login'),  
    path('signup/', SignupView.as_view(), name='signup'),  
    path('token/verify/', TestTokenView.as_view(), name='token_verify'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='update_user'),  
    path('responsables-entreprise/', ResponsableEntrepriseListView.as_view(), name='responsables-entreprise-list'),
    path('responsables-suivi/', ResponsableSuiviListView.as_view(), name='responsables-entreprise-list'),

    path('responsables-entreprise/<int:pk>/delete/', ResponsableEntrepriseDeleteView.as_view(), name='responsables-entreprise-delete'),
    path('responsables-entreprise/<int:pk>/update/', ResponsableEntrepriseUpdateView.as_view(), name='responsables-entreprise-update'),
    path('responsables-suivi/<int:pk>/delete/', ResponsableSuiviDeleteView.as_view(), name='responsables-suivi-delete'),
    path('responsables-suivi/<int:pk>/update/', ResponsableSuiviUpdateView.as_view(), name='responsables-suivi-update'),

    path('responsables-entreprise/<int:pk>/', ResponsableEntrepriseDetailView.as_view(), name='responsable-entreprise-detail'),
    path('responsables-suivi/<int:pk>/', ResponsableSuiviDetailView.as_view(), name='responsable-suivi-detail'),
    # Entreprises  
    # Entreprises Mère  
    path('entreprise-mere/',EntrepriseMereListCreateView.as_view(), name='entreprise-mere-list-create'),  
    path('entreprise-mere/<int:pk>/', EntrepriseMereRetrieveUpdateDeleteView.as_view(), name='entreprise-mere-detail'),  
  
    path('entreprise/', EntrepriseListCreateView.as_view(), name='entreprise-list-create'),  
    path('entreprise/<int:pk>/', EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-detail'),  

    # Activités  
    path('activites-industrielles/', ActiviteIndusListCreateView.as_view(), name='activite-industrielle-list-create'),  
    path('activites-industriellesbyid/', ActiviteIndusListCreateViewbyid.as_view(), name='activite-industrielle-list-createbyid'),  
    path('activites-industrielles/<int:pk>/', ActiviteIndusRetrieveUpdateDeleteView.as_view(), name='activite-industrielle-detail'),  

    # Aspects  
    path('aspect/', AspectListCreateView.as_view(), name='aspect-list-create'),  
    path('aspect/<int:pk>/', AspectRetrieveUpdateDeleteView.as_view(), name='aspect-detail'),  

    # Engagements  
    path('engagement-Indicateur/', EngagementCreateView.as_view(), name='create_engagement'),  
    path('engagement-aspect/', EngagementAspectCreateView.as_view(), name='engagement-aspect-create'),  
    path('engagement-aspect/<int:pk>/', EngagementAspectRetrieveUpdateDeleteView.as_view(), name='engagement-aspect-detail'),  
    path('engagement-indicateur/<int:pk>/', EngagementIndicateurRetrieveUpdateDeleteView.as_view(), name='engagement-indicateur-detail'),  
    path('engagements/sous-aspect-pollution/', EngagementSousAspectEauPollutionCreateView.as_view(), name='engagement-sous-aspect-create'),  
    path('engagements/sous-aspect-pollution/<int:pk>/', EngagementSousAspectPollutionRetrieveUpdateDeleteView.as_view(), name='engagement-sous-aspect-detail'),  
    path('indicateurs/sous-aspect-pollution/', EngagementIndicateurSousAspectPollutionCreateView.as_view(), name='engagement-indicateur-create'),  

    # Indicateurs  
    path('indicateur/', IndicateurListCreateView.as_view(), name='indicateur-list-create'),  
    path('indicateur/<int:pk>/', IndicateurRetrieveUpdateDeleteView.as_view(), name='indicateur-detail'),  
    path('indicateurs-eau-pollution/', IndicateurEauPollutionListCreateView.as_view(), name='indicateur-eau-pollution-list-create'),  
    path('indicateurs-eau-pollution/<int:pk>/', IndicateurEauPollutionRetrieveUpdateDeleteView.as_view(), name='indicateur-eau-pollution-detail'),  

    # Provinces  
    path('province/', ProvinceListCreateView.as_view(), name='province-list-create'),  
    path('province/<int:pk>/', ProvinceRetrieveUpdateDeleteView.as_view(), name='province-detail'),  
    # Zones  
    path('zone/', ZoneListCreateView.as_view(), name='zone-list-create'),  
    path('zone/<int:pk>/', ZoneRetrieveUpdateDeleteView.as_view(), name='zone-detail'),  

    # Communes  
    path('commune/', CommuneListCreateView.as_view(), name='commune-list-create'),  
    path('communes/', CommuneListCreateViewbyid_pref_prov.as_view(), name='commune-list-createby_id_pref'),  
    path('commune/<int:pk>/', CommuneRetrieveUpdateDeleteView.as_view(), name='commune-detail'),  

    # Suivis  
    path('suivi/', SuiviListCreateView.as_view(), name='suivi-list-create'),  
    path('suivi/<int:pk>/', SuiviRetrieveUpdateDeleteView.as_view(), name='suivi-detail'),  
    path('suivi-indicateurs/<int:pk>/', SuiviIndicateurRetrieveUpdateDeleteView.as_view(), name='suivi-indicateur-detail'),  
    path('suivis/sous-aspect-pollution/',SuiviSousAspectPollutionListCreateView.as_view(), name='suivi-sous-aspect-list-create'),  
    path('suivis/sous-aspect-pollution/<int:pk>/',SuiviSousAspectPollutionRetrieveUpdateDeleteView.as_view(), name='suivi-sous-aspect-detail'),  

    # Secteurs  
    path('secteurs/', SecteurListCreateView.as_view(), name='secteur-list-create'),  
    path('secteurs/<int:pk>/', SecteurRetrieveUpdateDeleteView.as_view(), name='secteur-detail'),  

    # Sous Aspects  
    path('sous-aspects-eau-pollution/', SousAspectEauPollutionListCreateView.as_view(), name='sous-aspect-eau-pollution-list-create'),  
    path('sous-aspects-eau-pollution/<int:pk>/', SousAspectEauPollutionRetrieveUpdateDeleteView.as_view(), name='sous-aspect-eau-pollution-detail'),  
    # URL pour Parcelles  
    path('parcelles/', ParcelleListCreateView.as_view(), name='parcelle-list-create'),  
    path('parcelles/<int:pk>/', ParcelleRetrieveUpdateDestroyView.as_view(), name='parcelle-detail'),  
    path('import-shapefile/', ImportShapefileView.as_view(), name='import-shapefile'),  

    path('indicateurs-sous-aspect/', IndicateurSousAspectListCreateView.as_view(), name='indicateurs-sous-aspect-list-create'),
    path('indicateurs-sous-aspect/<int:pk>/', IndicateurSousAspectRetrieveUpdateDeleteView.as_view(), name='indicateurs-sous-aspect-list-create'),

    # Engagements Sous-Aspect
    path('engagements-sous-aspect/', EngagementSousAspectCreateView.as_view(), name='engagements-sous-aspect-create'),
    path('engagementsindicateur-sous-aspect/', EngagementIndicateurSousAspectCreateView.as_view(), name='engagementsindicateur-sous-aspect-create'),

    # Suivi Indicateurs Sous-Aspect
    path('suivi-sous-aspect/', SuiviSousAspectListCreateView.as_view(), name='suivi-sous-aspect-create'),
]