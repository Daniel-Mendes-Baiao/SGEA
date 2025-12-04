from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .forms import SignUpForm
from .models import Profile

def _role(user):
    return getattr(getattr(user, 'profile', None), 'role', None)

@login_required
def register_participant(request):
    if _role(request.user) != 'organizador':
        messages.error(request, 'Apenas organizadores podem cadastrar usuários.')
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Role is handled by signal, but we can update it if needed or create a specific form
            # For now, using standard signup form which defaults to 'aluno' via signal
            # Ideally we should have a form field for role if organizer wants to create professors
            
            messages.success(request, f'Usuário {user.username} cadastrado com sucesso!')
            return redirect('register_participant')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/register_participant.html', {'form': form})

from django.db import transaction

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    profile = user.profile
                    
                    # Generate confirmation token
                    token = profile.generate_confirmation_token()
                    
                    # Build confirmation link
                    confirmation_link = request.build_absolute_uri(f'/accounts/confirm/{token}/')
                    
                    # Render email template
                    html_content = render_to_string('emails/welcome_email.html', {
                        'user_name': user.get_full_name() or user.username,
                        'confirmation_link': confirmation_link,
                        'confirmation_token': token,
                    })
                    
                    # Send email
                    subject = 'Bem-vindo ao SGEA - Confirme seu e-mail'
                    from_email = settings.DEFAULT_FROM_EMAIL
                    to_email = user.email
                    
                    email = EmailMultiAlternatives(subject, '', from_email, [to_email])
                    email.attach_alternative(html_content, "text/html")
                    
                    # Attach logo
                    try:
                        with open(settings.BASE_DIR / 'static' / 'logo.jpg', 'rb') as f:
                            email.attach('logo.jpg', f.read(), 'image/jpeg')
                            email.content_subtype = 'html'
                            email.mixed_subtype = 'related'
                            email.attach_alternative(html_content.replace('cid:logo', 'cid:logo.jpg'), "text/html")
                    except:
                        pass  # If logo not found, send without it
                    
                    email.send()
                    
                messages.success(request, 'Cadastro realizado! Verifique seu e-mail para confirmar sua conta.')
                return redirect('login')
                
            except Exception as e:
                messages.error(request, f'Erro ao realizar cadastro: {str(e)}')
                # Transaction will rollback automatically
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def confirm_email(request, token):
    profile = get_object_or_404(Profile, confirmation_token=token)
    
    if profile.email_confirmed:
        messages.info(request, 'Seu e-mail já foi confirmado anteriormente.')
    else:
        profile.email_confirmed = True
        profile.save()
        messages.success(request, 'E-mail confirmado com sucesso! Você já pode fazer login.')
    
    return redirect('login')

LoginView = auth_views.LoginView
LogoutView = auth_views.LogoutView
