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
]
