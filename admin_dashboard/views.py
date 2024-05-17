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

    # recuperation de la marque
    # créer d'un dictionnaire
    # tri des modeles selon la marque sélectionnée 
    modeles_data = {}
    for modele in modeles:
        if modele.marque_id not in modeles_data:
            modeles_data[modele.marque_id] = []
        modeles_data[modele.marque_id].append({'id': modele.id, 'nom': modele.nom})

    
    if request.method == "POST":
        marque_voiture = request.POST.get("marque_voiture")
        modele_voiture = request.POST.get("modele_voiture")
        immatriculation = request.POST.get("immatriculation")
        numero_serie = request.POST.get("numero_serie")
        couleur_voiture = request.POST.get("couleur_voiture")
        photo_voiture = request.FILES.get("photo_voiture")
        annee_fabrication=request.POST.get("annee_fabrication"),
        kilometrage=request.POST.get("kilometrage"),
        type_carburant=request.POST.get("type_carburant"),
        transmission=request.POST.get("transmission"),
        symptomes=request.POST.get("symptomes"),
        historique_maintenance=request.POST.get("historique_maintenance"),
        codes_erreur=request.POST.get("codes_erreur"),
        numero_chassi = request.POST.get('nemero_chassi'),
        nombre_de_vitesse = request.POST.get('nombre_de_vitesse')
        
        if marque_voiture == "autre":
            nouvelle_marque = request.POST.get("nouvelle_marque")
            if nouvelle_marque:
                try:
                    marque_voiture_obj = MarqueVoiture.objects.get(marque=nouvelle_marque)
                except MarqueVoiture.DoesNotExist:
                    marque_voiture_obj = MarqueVoiture.objects.create(marque=nouvelle_marque)
                else:
                    messages.error(request, f'La marque {nouvelle_marque} existe déjà.')
                    return redirect('/')
        else:
            marque_voiture_obj = MarqueVoiture.objects.get(marque=marque_voiture)

        if modele_voiture == "autre":
            nouveau_modele = request.POST.get("nouveau_modele")
            if nouveau_modele:
                try:
                    modele_voiture_obj = Modele.objects.get(nom=nouveau_modele)
                except Modele.DoesNotExist:
                    modele_voiture_obj = Modele.objects.create(nom=nouveau_modele, marque=marque_voiture_obj)
                else:
                    messages.error(request, f'Le modèle {nouveau_modele} existe déjà.')
                    return redirect('/')
        else:
            modele_voiture_obj = Modele.objects.get(pk=modele_voiture)
        
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
        return redirect('/')
    
    datas = {
        'marque_voitures': marque_voitures,
        'modeles': modeles,
        'modeles_data': json.dumps(modeles_data), # exportation du dictionnaire en json 
    }
    return render(request, 'dist/pages/tables/basic-table.html', datas)




