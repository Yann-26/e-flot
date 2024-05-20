from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect,  get_object_or_404
from django.urls import reverse

from diagnostic.models import *
from .models import*
from authenticate.models import type_client
from django.contrib import messages
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail



# Create your views here.
def dashboard_user(request, devis_id):
    user = request.user
    type_client = request.GET.get('type', 'particulier')
    voitures = Voiture.objects.all()
    garages = Garage.objects.all()
    User = get_user_model()
    current_user_count = User.objects.count()
    previous_user_count = 100  # assume this is the previous count of users
    if current_user_count > previous_user_count:
        percentage_increase = ((current_user_count - previous_user_count) / previous_user_count) * 100
        percentage_text = f"Increased by {percentage_increase:.2f}%"
    elif current_user_count < previous_user_count:
        percentage_decrease = ((previous_user_count - current_user_count) / previous_user_count) * 100
        percentage_text = f"Decreased by {percentage_decrease:.2f}%"
    else:
        percentage_text = "No change"

    user_type = user.type_client.type if hasattr(user, 'type_client') else 'Unknown'
    #affiché les voitures assignées

    # garage = Garage.objects.get(email=email)
   
    cars = Voiture.objects.filter(statut='en attente de diagnostic')
    diagnostics = Diagnostic.objects.all()
    devis = Devis.objects.get(id=devis_id)

    contexts = {
        'cars': cars,
        'devis':devis,
        'type_client': type_client,
        'voitures': voitures,
        'garages': garages,
        'diagnostics':diagnostics,
        'user_type': user_type,
        'user': current_user_count, 
        'percentage_text': percentage_text,
    }
    return render(request, 'dist/dashboard.html', contexts)


def new_voiture(request):
    marque_voitures = MarqueVoiture.objects.all()
    modeles = Modele.objects.all()

    #  creation d'un dictionnaire pour stocker les marques de voitures
    # ce dico sera renvoyer en json pour le filtre des modeles selon lamarque selectionnée
    modeles_data = {}
    for modele in modeles:
        if modele.marque_id not in modeles_data:
            modeles_data[modele.marque_id] = []
        modeles_data[modele.marque_id].append({'id': modele.id, 'nom': modele.nom})

    if request.method == "POST":
        marque_voiture_id = request.POST.get("marque_voiture")
        modele_voiture_id = request.POST.get("modele")
        immatriculation = request.POST.get("immatriculation")
        numero_serie = request.POST.get("numero_serie")
        couleur_voiture = request.POST.get("couleur_voiture")
        photo_voiture = request.FILES.get("photo_voiture/")
        annee_fabrication = request.POST.get("annee_fabrication")
        kilometrage = request.POST.get("kilometrage")
        type_carburant = request.POST.get("type_carburant")
        transmission = request.POST.get("transmission")
        symptomes = request.POST.get("symptomes")
        historique_maintenance = request.POST.get("historique_maintenance")
        codes_erreur = request.POST.get("codes_erreur")
        numero_chassi = request.POST.get("numero_chassi")
        nombre_de_vitesse = request.POST.get("nombre_de_vitesse")

        try:
            marque_voiture_obj = MarqueVoiture.objects.get(pk=marque_voiture_id)
        except MarqueVoiture.DoesNotExist:
            messages.error(request, "La marque sélectionnée n'existe pas.")
            return redirect('/Tableau/de/board/ajout/vehicule/')

        try:
            modele_voiture_obj = Modele.objects.get(pk=modele_voiture_id)
        except Modele.DoesNotExist:
            messages.error(request, "Le modèle sélectionné n'existe pas.")
            return redirect('/Tableau/de/board/ajout/vehicule/')

        add_voiture = Voiture(
            modele=modele_voiture_obj,
            annee_fabrication=annee_fabrication,
            kilometrage=kilometrage,
            type_carburant=type_carburant,
            transmission=transmission,
            numero_serie=numero_serie,
            immatriculation=immatriculation,
            couleur_voiture=couleur_voiture,
            symptomes=symptomes,
            historique_maintenance=historique_maintenance,
            codes_erreur=codes_erreur,
            numero_chassi=numero_chassi,
            nombre_de_vitesse=nombre_de_vitesse,
        )

        if photo_voiture:
            add_voiture.photo_voiture = photo_voiture

        add_voiture.save()
        messages.success(request, f'Voiture {add_voiture.modele} a été bien ajoutée!')
        return redirect('dashboard')

    datas = {
        'marque_voitures': marque_voitures,
        'modeles': modeles,
        #  envoi du dico en json
        'modeles_data': json.dumps(modeles_data),
    }
    return render(request, 'dist/pages/tables/Ajout-vehicule.html', datas)


#  ajout de garage
def new_garage(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        site_web = request.POST.get('site_web')
        email = request.POST.get('email')
        horaire = request.POST.get('horaire')
        service = request.POST.get('service')
        photo_garage = request.POST.get('photo_garage')
        logo_garage = request.POST.get('logo_garage')

        # Find the "Garage" type client or create it if it doesn't exist
        garage_type, created = type_client.objects.get_or_create(type='Garage')

        newGarage = Garage()
        newGarage.name = name
        newGarage.adresse = adresse
        newGarage.telephone = telephone
        newGarage.site_web = site_web
        newGarage.email = email
        newGarage.horaire = horaire
        newGarage.service = service
        newGarage.photo_garage = photo_garage
        newGarage.logo_garage = logo_garage
        newGarage.type_client = garage_type
        newGarage.save()

        # Creer un compte pour le garage
        username = name
        password = User.objects.make_random_password()
        user = User.objects.create_user(username, newGarage.email, password)

        # envoyer un email au propriétaire au garage avec son mot de passe 
        subject = 'Your Garage Account Password'
        login_url = request.build_absolute_uri(reverse('login_garage'))
        message = f'Dear {newGarage.name},\n\nYour garage account has been created successfully. Your username is {username} and your password is {password}. You can log in to your account at {login_url}.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [newGarage.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    datas = {}
    return render(request, 'dist/pages/tables/Ajout-garage.html', datas)



#  liste des garages
def list_garage(request):
    garages = Garage.objects.all().order_by('-id')
    datas = {
        'garages': garages,
    }
    return render(request, 'dist/pages/gestion/liste-garage.html', datas)


def list_voitures(request):
    voitures = Voiture.objects.all().order_by('-id')
    datas = {
        'voitures': voitures,
    }
    return render(request, 'dist/pages/gestion/liste-vehicule.html', datas)


def detail_garages(request, garage_id):
    garages = Garage.objects.get(id=garage_id)
    datas = {
        'garages': garages,
    }
    return render(request, 'dist/pages/gestion/garages.html', datas)


def detail_voitures(request, voiture_id):
    voitures = Voiture.objects.get(id=voiture_id)
    datas = {
        'voitures': voitures,
    }
    return render(request, 'dist/pages/gestion/vehicule.html', datas)