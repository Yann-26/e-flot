from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404

from diagnostic.models import Devis
from .models import envoi_contact
from admin_dashboard.models import Garage, Voiture
from django.contrib import messages
from django.core.mail import send_mail


# Create your views here.
def home(request,):
    garages = Garage.objects.all().order_by('-id')
    
    # formulaire d'envoi de contact
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        newContact = envoi_contact()
        newContact.nom = nom
        newContact.email = email
        newContact.message = message
        newContact.save()
        messages.success(request, 'Merci votre message ! ')
        return redirect('/')

    datas = {
        "garages":garages,
       
    }
    return render(request, 'index.html', datas)

#  assigner une voiture à un garage 
def assign_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    garages = Garage.objects.all()

    if request.method == 'POST':
        garage_id = request.POST.get('garage')
        try:
            garage = Garage.objects.get(pk=garage_id)
        except Garage.DoesNotExist:
            messages.error(request, "Le garage sélectionné n'existe pas.")
            return redirect('assign_voiture', voiture_id=voiture_id)

        voiture.garage_assigné = garage
        voiture.statut = 'en attente de diagnostic'
        voiture.save()

        # Envoyer un email au garage
        subject = 'Nouvelle voiture assignée pour diagnostic'
        message = f'Bonjour {garage.name},\n\nUne nouvelle voiture a été assignée à votre garage pour diagnostic.\n\nImmatriculation: {voiture.immatriculation}\nModèle: {voiture.modele.nom}\n\nMerci.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [garage.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        messages.success(request, f'Voiture {voiture.modele} a été assignée au garage {garage.name}.')
        return redirect('dashboard')

    context = {
        'voiture': voiture,
        'garages': garages
    }
    return render(request, 'assign_voiture.html', context)