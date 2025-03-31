from django.urls import path, re_path, register_converter
from . import views, converters

# Registrar conversores personalizados
register_converter(converters.YearConverter, 'year')

app_name = 'users'

urlpatterns = [
    # Vistas básicas
    path('', views.home, name='home'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/profile/<str:username>/', views.user_profile, name='user_profile'),
    path('users/archive/<str:username>/<int:user_id>/', views.user_archive, name='user_archive'),
    
    # Búsqueda y conversores personalizados
    path('users/history/<year:year>/', views.user_history, name='user_history'),
    re_path(r'^users/search/(?P<term>\w+)/$', views.user_search, name='user_search'),
    
    # URLs anidadas para grupos
    path('groups/', views.group_list, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail, name='group_detail'),
    path('groups/<int:group_id>/members/', views.group_members, name='group_members'),
    
    # Páginas de demostración de templates
    path('template-demo/', views.template_demo, name='template_demo'),
    path('custom-tags-demo/', views.custom_tags_demo, name='custom_tags_demo'),
] 