from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/verify/', views.TestTokenView.as_view(), name='token_verify'),

    path('entreprise-mere/', views.EntrepriseMereListCreateView.as_view(), name='entreprise-mere-list-create'),
    path('entreprise-mere/<int:pk>/', views.EntrepriseMereRetrieveUpdateDeleteView.as_view(), name='entreprise-mere-detail'),

    path('entreprise/', views.EntrepriseListCreateView.as_view(), name='entreprise-list-create'),
    path('entreprise/<int:pk>/', views.EntrepriseRetrieveUpdateDeleteView.as_view(), name='entreprise-detail'),

    path('aspect/', views.AspectListCreateView.as_view(), name='aspect-list-create'),
    path('aspect/<int:pk>/', views.AspectRetrieveUpdateDeleteView.as_view(), name='aspect-detail'),

    path('indicateur/', views.IndicateurListCreateView.as_view(), name='indicateur-list-create'),
    path('indicateur/<int:pk>/', views.IndicateurRetrieveUpdateDeleteView.as_view(), name='indicateur-detail'),

    path('province/', views.ProvinceListCreateView.as_view(), name='province-list-create'),
    path('province/<int:pk>/', views.ProvinceRetrieveUpdateDeleteView.as_view(), name='province-detail'),

    path('commune/', views.CommuneListCreateView.as_view(), name='commune-list-create'),
    path('commune/<int:pk>/', views.CommuneRetrieveUpdateDeleteView.as_view(), name='commune-detail'),

    path('engagement-Indicateur/', views.EngagementCreateView.as_view(), name='create_engagement'),
    path('engagement-Indicateur/<int:pk>/', views.EngagementIndicateurRetrieveUpdateDeleteView.as_view(), name='engagement-detail'),

    path('engagement-Aspect/', views.EngagementAspectCreateView.as_view(), name='create_engagement'),
    path('engagement-Aspect/<int:pk>/', views.EngagementAspectRetrieveUpdateDeleteView.as_view(), name='engagement-detail'),
    
    path('suivi/', views.SuiviListCreateView.as_view(), name='suivi-list-create'),
    path('suivi/<int:pk>/', views.SuiviRetrieveUpdateDeleteView.as_view(), name='suivi-detail'),

    path('echeances/entreprise/<int:id_entreprise>/', views.EcheanceByEntrepriseView.as_view(), name='echeance-by-entreprise'),
    path('echeances/', views.EcheanceListView.as_view(), name='echeance-list'),
    


]
