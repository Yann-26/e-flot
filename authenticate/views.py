from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
import uuid
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login, logout
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import views as auth_views



# Create your views here.
def connexion(request):
    return render(request, 'connexion.html')


# inscription 
def register(request):
    type_client = request.GET.get('type', 'particulier')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        termes_acceptes = request.POST.get('termes_accept') 
       
        
        if type_client == 'particulier':
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')
            password_confirm = request.POST.get('password_confirm')
            
            if password != password_confirm:
                messages.error(request, 'Passwords do not match.')
                return redirect(reverse('registerP') + f'?type={type_client}')
            # Convertir la valeur en booléen
            termes_acceptes = bool(termes_acceptes)

            # Vérifier si les termes ont été acceptés
            if not termes_acceptes:
                messages.error(request, 'Veuillez accepter les termes et conditions.')
                return redirect(reverse('registerP') + f'?type={type_client}')
            
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username is taken.')
                    return redirect(reverse('registerP') + f'?type={type_client}')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is taken.')
                    return redirect(reverse('registerP') + f'?type={type_client}')
                
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
                user.save()
                
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(
                    termes_accept =termes_acceptes,
                    user=user,
                    auth_token=auth_token
                )
                profile_obj.save()
                
                send_mail_after_registration(email, auth_token)
                
                return redirect('/token')
    
            except Exception as e:
                print(e)
                messages.error(request, 'An error occurred.')
                
        elif type_client == 'entreprise':
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')  
            addresse = request.POST.get('addresse')
            phone = request.POST.get('phone')  
            password_confirm = request.POST.get('password_confirm')

            # Convertir la valeur en booléen
            termes_acceptes = bool(termes_acceptes)

                # Vérifier si les termes ont été acceptés
            if not termes_acceptes:
                messages.error(request, 'Veuillez accepter les termes et conditions.')
                return redirect(reverse('registerP') + f'?type={type_client}')
            
            if password != password_confirm:
                messages.error(request, 'Les mots de passe ne correspondent pas!.')
                return redirect(reverse('registerP') + f'?type={type_client}')
            
            
            try:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Nom d\'entreprise déjà pris.')
                    return redirect(reverse('registerP') + f'?type={type_client}')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email déjà pris.')
                    return redirect(reverse('registerP') + f'?type={type_client}')
                
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)  
                user.save()
                
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(
                    termes_accept = termes_acceptes,
                    phone = phone,
                    addresse = addresse,
                    user=user,
                    auth_token=auth_token
                )
                profile_obj.save()
                
                send_mail_after_registration(email, auth_token)
                return redirect('/token')
            except Exception as e:
                print(e)
                messages.error(request, 'Une erreur s\'esr produite. Veuillez réessayez plus tard!')

                
    context = {'type_client': type_client}
    return render(request, 'register.html', context)




# fonction de connexion
def login_user(request):
    type_client = request.GET.get('type', 'particulier')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = None
        profile_obj = None
        
        if type_client == "particulier":
            user = User.objects.filter(username=username).first()
        elif type_client == "entreprise":
            user = User.objects.filter(email=email).first()
        
        if user is None:
            messages.error(request, f'{type_client.capitalize()} not found.')
            return redirect(reverse('login') + f'?type={type_client}')
        
        profile_obj = Profile.objects.filter(user=user).first()
        
        if not profile_obj:
            messages.error(request, 'Profil non trouvé.')
            return redirect(reverse('login') + f'?type={type_client}')
        
        if not profile_obj.is_verified:
            messages.error(request, 'Compte non verifié. Priere verifier votre boite mail.')
            return redirect(reverse('login') + f'?type={type_client}')
        
        user = authenticate(request, username=user.username, password=password)
        
        if user is None:
            messages.error(request, 'Wrong password.')
            return redirect(reverse('login') + f'?type={type_client}')
        
        login(request, user)
        return redirect('home')
    
    context = {'type_client': type_client}
    return render(request, 'login.html', context)



# page redirigée apres confirmation du compte
def success(request):
    return render(request , 'success.html')


# page affichée aux user pour dire que l'email a été envoyé
def token_send(request):
    return render(request , 'token_send.html')


# fonction de deconnexion
def signout(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    return redirect('home')


# verifier le profile
def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid verification link.')
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


# page d'erreur de creation de compte
def error_page(request):
    return render(request, 'error.html')


# fonction d'envoi de l'email de confirmation 
def send_mail_after_registration(email, token):
    subject = 'Votre compte doit être vérifier'
    email_template_name = "emailConfirmation.html"
    context = {'token': token}
    message = render_to_string(email_template_name, context)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# fonction de recuperation de mot de passe
def password_reset_request(request):
    type_client = request.GET.get('type', 'particulier')
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    context = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        'type_client': type_client,
                    }
                    email = render_to_string(email_template_name, context)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done", type_client=type_client)
    password_reset_form = PasswordResetForm()
   
    return render(request=request, template_name="password_reset.html",  context = {
        "password_reset_form": password_reset_form, 
        "type_client": type_client,
    })

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        user = form.save()
        # Récupérer le type_client depuis les arguments de la vue
        type_client = self.kwargs['type_client']
        # Construire l'URL pour password_reset_complete avec le type_client
        success_url = reverse('password_reset_complete', args=[type_client])
        # Rediriger vers l'URL construit
        return redirect(success_url)

def password_reset_done(request, type_client):
    context = {
        "type_client": type_client,
    }
    return render(request, 'password_reset_done.html', context)

def password_reset_complete(request, type_client):
    context = {
        'type_client': type_client,
    }
    return render(request, 'password_reset_complete.html', context)

