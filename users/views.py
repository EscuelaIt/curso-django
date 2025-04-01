from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import User, Post
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

# Vistas para posts
class PostListView(ListView):
    """
    Vista basada en clase que muestra una lista de posts
    """
    model = Post
    template_name = 'users/posts/list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Posts'
        return context

class PostCreateView(CreateView):
    """
    Vista basada en clase para crear un nuevo post
    """
    model = Post
    template_name = 'users/posts/create.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('users:post_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para crear un post.')
            return redirect('users:post_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            # Get our custom User instance
            user = User.objects.get(username=self.request.user.username)
            form.instance.author = user
            form.instance.is_published = True  # Publicar automáticamente
            messages.success(self.request, 'Post creado exitosamente.')
            return super().form_valid(form)
        except User.DoesNotExist:
            messages.error(self.request, 'Error: Usuario no encontrado.')
            return self.form_invalid(form)

def post_detail(request, post_id):
    """
    Vista que muestra los detalles de un post específico
    """
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'users/posts/detail.html', {'post': post})

class PostUpdateView(UpdateView):
    """
    Vista basada en clase para actualizar un post existente
    """
    model = Post
    template_name = 'users/posts/update.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('users:post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Post actualizado exitosamente.')
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    """
    Vista basada en clase para eliminar un post
    """
    model = Post
    template_name = 'users/posts/delete.html'
    success_url = reverse_lazy('users:post_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Post eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

def post_like(request, post_id):
    """
    Vista para dar like a un post
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para dar like a un post.')
        return redirect('admin:index')
        
    try:
        post = get_object_or_404(Post, id=post_id)
        user = User.objects.get(username=request.user.username)
        post.like(user)
        messages.success(request, 'Te gusta este post.')
    except User.DoesNotExist:
        messages.error(request, 'Error: Usuario no encontrado.')
    return redirect('users:post_detail', post_id=post_id)

def post_unlike(request, post_id):
    """
    Vista para quitar like de un post
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para quitar like de un post.')
        return redirect('users:post_detail', post_id=post_id)
        
    try:
        post = get_object_or_404(Post, id=post_id)
        user = User.objects.get(username=request.user.username)
        post.unlike(user)
        messages.success(request, 'Ya no te gusta este post.')
    except User.DoesNotExist:
        messages.error(request, 'Error: Usuario no encontrado.')
    return redirect('users:post_detail', post_id=post_id)

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
