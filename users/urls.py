from django.urls import path, re_path, register_converter
from . import views
from . import converters  # Importaremos los conversores personalizados que crearemos

# Registramos un conversor personalizado
register_converter(converters.YearConverter, 'year')

app_name = 'users'

urlpatterns = [
    # Vista básica con función
    path('', views.home, name='home'),
    
    # URLs con parámetros en la ruta
    path('detail/<int:user_id>/', views.user_detail, name='user_detail'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    
    # Vista basada en clase
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    
    # URL con múltiples parámetros
    path('archive/<str:username>/<int:user_id>/', views.user_archive, name='user_archive'),
    
    # URL con conversor personalizado - Temporalmente usando conversor int estándar
    path('history/<int:year>/', views.user_history, name='user_history'),
    
    # URL con expresión regular
    re_path(r'^search/(?P<term>\w+)/$', views.user_search, name='user_search'),
    
    # URLs anidadas para sub-recursos
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/members/', views.group_members, name='group_members'),
] 