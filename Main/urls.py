from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('assign/voiture/<int:voiture_id>/', assign_voiture, name='assign_voiture'),
]