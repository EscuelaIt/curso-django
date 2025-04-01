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
    
    # URLs para posts
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:post_id>/like/', views.post_like, name='post_like'),
    path('posts/<int:post_id>/unlike/', views.post_unlike, name='post_unlike'),
    
    # Páginas de demostración de templates
    path('template-demo/', views.template_demo, name='template_demo'),
    path('custom-tags-demo/', views.custom_tags_demo, name='custom_tags_demo'),
] 