from django.shortcuts import render
from .models import User

def home(request):
    """
    Vista principal que muestra todos los usuarios registrados
    """
    users = User.objects.filter(is_active=True)
    context = {
        'users': users,
        'total_users': users.count(),
    }
    return render(request, 'users/home.html', context)
