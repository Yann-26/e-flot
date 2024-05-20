from django.urls import path
from .views import *

urlpatterns = [
    path('Connexion/garage/', login_garage, name='login_garage'),
    path('faire/devis/', create_devis, name='devis'),
    path('display-recu/<int:devis_id>/', display_recu, name='display_recu'),
    path('submit/diagnostic/<int:voiture_id>/', faire_diagnostic, name='diagnostic'),
    # path('recu/<int:devis_id>/pdf/', download_pdf, name='download_pdf'),
]