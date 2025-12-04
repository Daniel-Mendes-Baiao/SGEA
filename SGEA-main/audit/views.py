from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from .models import AuditLog

def _role(user):
    return getattr(getattr(user, 'profile', None), 'role', None)

@login_required
def audit_list(request):
    if _role(request.user) != 'organizador':
        messages.error(request, 'Acesso restrito a organizadores.')
        return redirect('home')
    
    logs = AuditLog.objects.all().select_related('user')
    
    # Filter by date
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            logs = logs.filter(timestamp__date=filter_date)
        except ValueError:
            pass
    
    # Filter by user
    user_filter = request.GET.get('user')
    user_filter_int = None
    if user_filter:
        try:
            user_filter_int = int(user_filter)
            logs = logs.filter(user__id=user_filter_int)
        except ValueError:
            pass
    
    # Get list of users for filter dropdown
    users = User.objects.all().order_by('username')
    
    return render(request, 'audit/audit_list.html', {
        'logs': logs,
        'users': users,
        'date_filter': date_filter or '',
        'user_filter_int': user_filter_int
    })
