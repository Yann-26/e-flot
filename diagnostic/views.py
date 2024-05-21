from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.forms.models import modelform_factory
from admin_dashboard.models import Garage, Voiture
from authenticate.models import type_client
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Devis, DevisField, Diagnostic
# from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import JsonResponse


def login_garage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        # Connexion standard
        if not new_password and not confirm_new_password:
            user = authenticate(request, username=username, password=current_password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                messages.error(request, 'Invalide username ou mot de passe')

        # Définition ou changement du mot de passe
        elif new_password and confirm_new_password:
            if new_password != confirm_new_password:
                messages.error(request, 'Passwords do not match')
            else:
                try:
                    user = User.objects.get(username=username, email=email)
                    if user.check_password(current_password):
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)  # Important pour éviter de déconnecter l'utilisateur
                        messages.success(request, 'Mot de passe mis a jour avec succes!')
                        login(request, user)
                        return redirect('home')  
                    else:
                        messages.error(request, 'Ancien mot de passe incorrect! \n Veuillez verifier le mot de passe envoyé par email svp!')
                except User.DoesNotExist:
                    messages.error(request, 'Invalide username ou email')

    return render(request, 'login-garage.html')



# @login_required
def create_devis(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        commentaire = request.POST.get('commentaire')
        diagnostic_id = request.POST.get('diagnostic')
        diagnostic = Diagnostic.objects.get(pk=diagnostic_id)
        
        devis = Devis(title=title, diagnostic=diagnostic, commentaire=commentaire)
        devis.save()

        labels = request.POST.getlist('field_label')
        types = request.POST.getlist('field_type')
        values = request.POST.getlist('field_value')
        prixs = request.POST.getlist('field_prix')

        total_prix = 0

        for label, field_type, value, prix in zip(labels, types, values, prixs):
            prix_value = float(prix) if prix else 0.0
            DevisField.objects.create(devis=devis, label=label, field_type=field_type, value=value, prix=prix_value)
            total_prix += prix_value

        devis.total_prix = total_prix
        devis.save()

        return redirect('/faire/devis/', devis_id=devis.id)

    diagnostics = Diagnostic.objects.all()
    return render(request, 'create_devis.html', {'diagnostics': diagnostics})



def faire_diagnostic(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    garage = get_object_or_404(Garage)

    if request.method == 'POST':
        solutions = request.POST.get('solutions')
        problems = request.POST.get('problems')
        duree_diagnostic = request.POST.get('duree_diagnostic')
        method_diagnostic = request.POST.get('method_diagnostic')

        newDiagnostic = Diagnostic(
            garage=garage,
            vehicule=voiture,
            solutions=solutions,
            problems=problems,
            duree_diagnostic=duree_diagnostic,
            method_diagnostic=method_diagnostic
        )
        newDiagnostic.save()

        # Mettre à jour le statut de la voiture
        voiture.statut = 'diagnostiquée'
        voiture.save()

        messages.success(request, 'Le diagnostic a été soumis avec succès.')
        return redirect('dashboard')

    context = {
        'voiture': voiture,
        
    }
    return render(request, 'diagnostic.html', context)


def get_diagnostic_details(request, diagnostic_id):
    diagnostic = Diagnostic.objects.get(id=diagnostic_id)
    data = {
        'garage_name': diagnostic.garage.name,
        'garage_email': diagnostic.garage.email,
        'garage_address': diagnostic.garage.adresse,
        'garage_telephone': diagnostic.garage.telephone,
        'garage_business_number': diagnostic.garage.telephone,
        'garage_logo': diagnostic.garage.logo_garage.url,
        'date_diagnostic': diagnostic.date_add,
    }
    return JsonResponse(data)


# @login_required
def display_recu(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)
    devis_fields = DevisField.objects.filter(devis=devis)
    context = {
        'devis': devis,
        'devis_fields': devis_fields,
    }
    return render(request, 'display_recu.html', context)

# @login_required
# def download_pdf(request, devis_id):
#     devis = get_object_or_404(Devis, id=devis_id)
#     devis_fields = DevisField.objects.filter(devis=devis)
#     context = {
#         'devis': devis,
#         'devis_fields': devis_fields,
#     }
#     html_string = render_to_string('display_recu.html', context)
#     html = HTML(string=html_string)
#     pdf_file = html.write_pdf()

#     response = HttpResponse(pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="recu_{devis.id}.pdf"'

#     return response