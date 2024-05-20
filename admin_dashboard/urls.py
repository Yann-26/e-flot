from django.urls import path
from .views import *


urlpatterns = [

    path('Tableau/de/board/<int:devis_id>', dashboard_user, name='dashboard'),
    path('Tableau/de/board/ajout/vehicule/', new_voiture, name='ajout_vehicule'),
    path('Tableau/de/board/ajout/garage/', new_garage, name='ajout_garage'),
    path('Tableau/de/board/liste/garages/', list_garage, name='liste_garage'),
    path('Tableau/de/board/liste/vehicules/', list_voitures, name='liste_voiture'),
    path('Tableau/de/board/liste/vehicules/<int:voiture_id>/', detail_voitures, name='detail_voiture'),
    path('Tableau/de/board/detail/garage/<int:garage_id>/', detail_garages, name='detail_garage'),
    
]