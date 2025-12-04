from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class EmailConfirmationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Allow access to these paths without email confirmation
        allowed_paths = [
            reverse('login'),
            reverse('signup'),
            reverse('logout'),
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # Allow confirmation URLs
        if request.path.startswith('/accounts/confirm/'):
            return self.get_response(request)
        
        # Check if user is authenticated and email not confirmed
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile') and not request.user.profile.email_confirmed:
                # Allow access to allowed paths
                for path in allowed_paths:
                    if request.path.startswith(path):
                        return self.get_response(request)
                
                # Block access to other pages
                messages.warning(request, 'Por favor, confirme seu e-mail antes de acessar o sistema.')
                return redirect('login')
        
        return self.get_response(request)
