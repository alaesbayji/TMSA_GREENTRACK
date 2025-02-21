from django.urls import path  
from rest_framework_simplejwt.views import TokenRefreshView  
from . import views  
from .views.auth_views import( LoginView,SignupView,TestTokenView)
from .views.enterprise_views import (EntrepriseMereListCreateView,EntrepriseMereRetrieveUpdateDeleteView,EntrepriseListCreateView,EntrepriseRetrieveUpdateDeleteView,
ActiviteIndusListCreateView,ActiviteIndusRetrieveUpdateDeleteView,SecteurListCreateView,SecteurRetrieveUpdateDeleteView)
from .views.aspect_views import (AspectListCreateView,AspectRetrieveUpdateDeleteView,IndicateurListCreateView,IndicateurRetrieveUpdateDeleteView,IndicateurEauPollutionListCreateView,IndicateurEauPollutionRetrieveUpdateDeleteView,
SousAspectEauPollutionListCreateView,SousAspectEauPollutionRetrieveUpdateDeleteView)
from .views.suivi_views import( EngagementCreateView,EngagementAspectCreateView,EngagementAspectRetrieveUpdateDeleteView,EngagementIndicateurRetrieveUpdateDeleteView,SuiviListCreateView,SuiviRetrieveUpdateDeleteView,
SuiviIndicateurRetrieveUpdateDeleteView,EngagementIndicateurSousAspectCreateView,EngagementSousAspectEauPollutionCreateView,EngagementSousAspectRetrieveUpdateDeleteView,SuiviSousAspectListCreateView,SuiviSousAspectRetrieveUpdateDeleteView,
SuiviIndicateurSousAspectRetrieveUpdateDeleteView)
from .views.map_views import CommuneListCreateView ,CommuneRetrieveUpdateDeleteView,ProvinceListCreateView,ProvinceRetrieveUpdateDeleteView
urlpatterns = [  
    # Authentification  
    path('login/', LoginView.as_view(), name='login'),  
    path('signup/', SignupView.as_view(), name='signup'),  
    path('token/verify/', TestTokenView.as_view(), name='token_verify'),  

    # Entreprises Mère  
    path('entreprise-mere/',EntrepriseMereListCreateView.as_view(), name='entreprise-mere-list-create'),  
    path('entreprise-mere/<int:pk>/', EntrepriseMereRetrieveUpdateDeleteView.as_view(), name='entreprise-mere-detail'),  

    # Entreprises  
    path('entreprise/', EntrepriseListCreateView.as_view(), name='entreprise-list-create'),  
    path('entreprise/<int:pk>/', EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-detail'),  

    # Activités  
    path('activites-industrielles/', ActiviteIndusListCreateView.as_view(), name='activite-industrielle-list-create'),  
    path('activites-industrielles/<int:pk>/', ActiviteIndusRetrieveUpdateDeleteView.as_view(), name='activite-industrielle-detail'),  

    # Aspects  
    path('aspect/', AspectListCreateView.as_view(), name='aspect-list-create'),  
    path('aspect/<int:pk>/', AspectRetrieveUpdateDeleteView.as_view(), name='aspect-detail'),  

    # Engagements  
    path('engagement-Indicateur/', EngagementCreateView.as_view(), name='create_engagement'),  
    path('engagement-aspect/', EngagementAspectCreateView.as_view(), name='engagement-aspect-create'),  
    path('engagement-aspect/<int:pk>/', EngagementAspectRetrieveUpdateDeleteView.as_view(), name='engagement-aspect-detail'),  
    path('engagement-indicateur/<int:pk>/', EngagementIndicateurRetrieveUpdateDeleteView.as_view(), name='engagement-indicateur-detail'),  
    path('engagements/sous-aspect/', EngagementSousAspectEauPollutionCreateView.as_view(), name='engagement-sous-aspect-create'),  
    path('engagements/sous-aspect/<int:pk>/', EngagementSousAspectRetrieveUpdateDeleteView.as_view(), name='engagement-sous-aspect-detail'),  
    path('indicateurs/sous-aspect/', EngagementIndicateurSousAspectCreateView.as_view(), name='engagement-indicateur-create'),  

    # Indicateurs  
    path('indicateur/', IndicateurListCreateView.as_view(), name='indicateur-list-create'),  
    path('indicateur/<int:pk>/', IndicateurRetrieveUpdateDeleteView.as_view(), name='indicateur-detail'),  
    path('indicateurs-eau-pollution/', IndicateurEauPollutionListCreateView.as_view(), name='indicateur-eau-pollution-list-create'),  
    path('indicateurs-eau-pollution/<int:pk>/', IndicateurEauPollutionRetrieveUpdateDeleteView.as_view(), name='indicateur-eau-pollution-detail'),  

    # Provinces  
    path('province/', ProvinceListCreateView.as_view(), name='province-list-create'),  
    path('province/<int:pk>/', ProvinceRetrieveUpdateDeleteView.as_view(), name='province-detail'),  

    # Communes  
    path('commune/', CommuneListCreateView.as_view(), name='commune-list-create'),  
    path('commune/<int:pk>/', CommuneRetrieveUpdateDeleteView.as_view(), name='commune-detail'),  

    # Suivis  
    path('suivi/', SuiviListCreateView.as_view(), name='suivi-list-create'),  
    path('suivi/<int:pk>/', SuiviRetrieveUpdateDeleteView.as_view(), name='suivi-detail'),  
    path('suivi-indicateurs/<int:pk>/', SuiviIndicateurRetrieveUpdateDeleteView.as_view(), name='suivi-indicateur-detail'),  
    path('suivis/sous-aspect/',SuiviSousAspectListCreateView.as_view(), name='suivi-sous-aspect-list-create'),  
    path('suivis/sous-aspect/<int:pk>/',SuiviSousAspectRetrieveUpdateDeleteView.as_view(), name='suivi-sous-aspect-detail'),  

    # Secteurs  
    path('secteurs/', SecteurListCreateView.as_view(), name='secteur-list-create'),  
    path('secteurs/<int:pk>/', SecteurRetrieveUpdateDeleteView.as_view(), name='secteur-detail'),  

    # Sous Aspects  
    path('sous-aspects-eau-pollution/', SousAspectEauPollutionListCreateView.as_view(), name='sous-aspect-eau-pollution-list-create'),  
    path('sous-aspects-eau-pollution/<int:pk>/', SousAspectEauPollutionRetrieveUpdateDeleteView.as_view(), name='sous-aspect-eau-pollution-detail'),  
]