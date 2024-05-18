from django.shortcuts import render, redirect
from .models import envoi_contact
from admin_dashboard.models import Garage
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def home(request):
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



