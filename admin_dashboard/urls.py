from django.urls import path
from .views import *


urlpatterns = [
    path('Tableau/de/board/', dashboard_user, name='dashboard' ),
    path('Tableau/de/board/ajout/vehicule/', new_voiture, name='ajout_vehicule' )
]