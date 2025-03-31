from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import User
import datetime

# Vista de función básica
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

# Vista con parámetro de ID
def user_detail(request, user_id):
    """
    Vista que muestra detalles de un usuario específico
    """
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/detail.html', {'user': user})

# Vista con parámetro de string
def user_profile(request, username):
    """
    Vista que muestra el perfil de un usuario por nombre de usuario
    """
    user = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'user': user})

# Vista basada en clase - ListView
class UserListView(ListView):
    """
    Vista basada en clase que muestra una lista de usuarios
    """
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    
    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios'
        return context

# Vista basada en clase - CreateView
class UserCreateView(CreateView):
    """
    Vista basada en clase para crear un nuevo usuario
    """
    model = User
    template_name = 'users/create.html'
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = reverse_lazy('users:user_list')

# Vista con múltiples parámetros
def user_archive(request, username, user_id):
    """
    Vista que muestra los usuarios con el username o id especificado
    """
    print(username, user_id)
    users = User.objects.filter(Q(username=username) | Q(id=user_id))
    context = {
        'users': users,
        'username': username,
        'user_id': user_id
    }
    return render(request, 'users/archive.html', context)

# Vista con conversor personalizado
def user_history(request, year):
    """
    Vista que muestra la historia de usuarios creados en un año específico
    """
    users = User.objects.filter(date_joined__year=year)
    return render(request, 'users/history.html', {
        'users': users,
        'year': year
    })

# Vista con expresión regular
def user_search(request, term):
    """
    Vista que busca usuarios por un término específico
    """
    users = User.objects.filter(username__contains=term)
    return render(request, 'users/search.html', {
        'users': users,
        'term': term
    })

# Vistas para grupos (ejemplo de URLs anidadas)
def group_list(request):
    """
    Vista que muestra todos los grupos
    """
    return render(request, 'users/groups/list.html', {})

def group_detail(request, group_id):
    """
    Vista que muestra los detalles de un grupo específico
    """
    return render(request, 'users/groups/detail.html', {'group_id': group_id})

def group_members(request, group_id):
    """
    Vista que muestra los miembros de un grupo específico
    """
    return render(request, 'users/groups/members.html', {'group_id': group_id})

# Vistas para demostración de templates
def template_demo(request):
    """
    Vista que muestra ejemplos de diferentes características de los templates de Django
    """
    context = {
        'name': 'Jean Pierre',
        'user': {
            'username': 'manduinca',
            'email': 'manduinca@escuela.it',
            'first_name': 'Jean',
            'last_name': 'Mandujano',
            'get_full_name': 'Jean Mandujano'
        },
        'description': 'Esta es una descripción larga para demostrar el filtro truncatechars.',
        'date_example': datetime.datetime.now(),
        'number': 10,
        'tags': ['Django', 'Templates', 'Python', 'Web'],
        'items': ['Elemento 1', 'Elemento 2', 'Elemento 3', 'Elemento 4'],
        'html_content': '<strong>Este texto está en negrita</strong> y <em>este en cursiva</em>.',
    }
    return render(request, 'users/template_demo.html', context)

def custom_tags_demo(request):
    """
    Vista que muestra ejemplos de tags y filtros personalizados
    """
    context = {
        'nombre': 'Usuario',
        'frutas': ['Manzana', 'Banana', 'Naranja', 'Pera', 'Uva'],
        'colores': ['Rojo', 'Azul', 'Verde', 'Amarillo']
    }
    return render(request, 'users/custom_tags_demo.html', context)
