from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
import json



# Create your views here.
def dashboard_user(request):
    type_client = request.GET.get('type', 'particulier')

    contexts = {
        'type_client': type_client,
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


def new_garage(request) : 
    if request.method == 'POST' : 
        name = request.POST.get('name')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        site_web = request.POST.get('site_web')
        email = request.POST.get('email')
        horaire = request.POST.get('horaire')
        service = request.POST.get('service')
        photo_garage = request.POST.get('photo_garage')
        logo_garage = request.POST.get('logo_garage')
        
        
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
        newGarage.save()
    datas = {
     }   
    return render(request, 'dist/pages/tables/Ajout-garage.html', datas)


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