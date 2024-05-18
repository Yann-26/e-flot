from django.urls import path
from .views import *


urlpatterns = [

    path('Tableau/de/board/', dashboard_user, name='dashboard' ),
    path('Tableau/de/board/ajout/vehicule/', new_voiture, name='ajout_vehicule'),
    path('Tableau/de/board/ajout/garage/', new_garage, name='ajout_garage'),
    path('Tableau/de/board/liste/garages/', list_garage, name='liste_garage'),
    path('Tableau/de/board/liste/vehicules/', list_voitures, name='liste_voiture'),
    
]