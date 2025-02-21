from django.urls import path  
from rest_framework_simplejwt.views import TokenRefreshView  
from . import views  

urlpatterns = [  
    # Authentification  
    path('login/', views.LoginView.as_view(), name='login'),  
    path('signup/', views.SignupView.as_view(), name='signup'),  
    path('token/verify/', views.TestTokenView.as_view(), name='token_verify'),  

    # Entreprises Mère  
    path('entreprise-mere/', views.EntrepriseMereListCreateView.as_view(), name='entreprise-mere-list-create'),  
    path('entreprise-mere/<int:pk>/', views.EntrepriseMereRetrieveUpdateDeleteView.as_view(), name='entreprise-mere-detail'),  

    # Entreprises  
    path('entreprise/', views.EntrepriseListCreateView.as_view(), name='entreprise-list-create'),  
    path('entreprise/<int:pk>/', views.EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-detail'),  

    # Activités  
    path('activites-industrielles/', views.ActiviteIndusListCreateView.as_view(), name='activite-industrielle-list-create'),  
    path('activites-industrielles/<int:pk>/', views.ActiviteIndusRetrieveUpdateDeleteView.as_view(), name='activite-industrielle-detail'),  

    # Aspects  
    path('aspect/', views.AspectListCreateView.as_view(), name='aspect-list-create'),  
    path('aspect/<int:pk>/', views.AspectRetrieveUpdateDeleteView.as_view(), name='aspect-detail'),  

    # Engagements  
    path('engagement-Indicateur/', views.EngagementCreateView.as_view(), name='create_engagement'),  
    path('engagement-aspect/', views.EngagementAspectCreateView.as_view(), name='engagement-aspect-create'),  
    path('engagement-aspect/<int:pk>/', views.EngagementAspectRetrieveUpdateDeleteView.as_view(), name='engagement-aspect-detail'),  
    path('engagement-indicateur/<int:pk>/', views.EngagementIndicateurRetrieveUpdateDeleteView.as_view(), name='engagement-indicateur-detail'),  
    path('engagements/sous-aspect/', views.EngagementSousAspectEauPollutionCreateView.as_view(), name='engagement-sous-aspect-create'),  
    path('engagements/sous-aspect/<int:pk>/', views.EngagementSousAspectRetrieveUpdateDeleteView.as_view(), name='engagement-sous-aspect-detail'),  
    path('indicateurs/sous-aspect/', views.EngagementIndicateurSousAspectCreateView.as_view(), name='engagement-indicateur-create'),  

    # Indicateurs  
    path('indicateur/', views.IndicateurListCreateView.as_view(), name='indicateur-list-create'),  
    path('indicateur/<int:pk>/', views.IndicateurRetrieveUpdateDeleteView.as_view(), name='indicateur-detail'),  
    path('indicateurs-eau-pollution/', views.IndicateurEauPollutionListCreateView.as_view(), name='indicateur-eau-pollution-list-create'),  
    path('indicateurs-eau-pollution/<int:pk>/', views.IndicateurEauPollutionRetrieveUpdateDeleteView.as_view(), name='indicateur-eau-pollution-detail'),  

    # Provinces  
    path('province/', views.ProvinceListCreateView.as_view(), name='province-list-create'),  
    path('province/<int:pk>/', views.ProvinceRetrieveUpdateDeleteView.as_view(), name='province-detail'),  

    # Communes  
    path('commune/', views.CommuneListCreateView.as_view(), name='commune-list-create'),  
    path('commune/<int:pk>/', views.CommuneRetrieveUpdateDeleteView.as_view(), name='commune-detail'),  

    # Suivis  
    path('suivi/', views.SuiviListCreateView.as_view(), name='suivi-list-create'),  
    path('suivi/<int:pk>/', views.SuiviRetrieveUpdateDeleteView.as_view(), name='suivi-detail'),  
    path('suivi-indicateurs/<int:pk>/', views.SuiviIndicateurRetrieveUpdateDeleteView.as_view(), name='suivi-indicateur-detail'),  
    path('suivis/sous-aspect/', views.SuiviSousAspectListCreateView.as_view(), name='suivi-sous-aspect-list-create'),  
    path('suivis/sous-aspect/<int:pk>/', views.SuiviSousAspectRetrieveUpdateDeleteView.as_view(), name='suivi-sous-aspect-detail'),  

    # Secteurs  
    path('secteurs/', views.SecteurListCreateView.as_view(), name='secteur-list-create'),  
    path('secteurs/<int:pk>/', views.SecteurRetrieveUpdateDeleteView.as_view(), name='secteur-detail'),  

    # Sous Aspects  
    path('sous-aspects-eau-pollution/', views.SousAspectEauPollutionListCreateView.as_view(), name='sous-aspect-eau-pollution-list-create'),  
    path('sous-aspects-eau-pollution/<int:pk>/', views.SousAspectEauPollutionRetrieveUpdateDeleteView.as_view(), name='sous-aspect-eau-pollution-detail'),  
]