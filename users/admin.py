from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_full_name', 'is_active', 'created_at', 'get_posts_count')
    list_filter = ('is_active', 'created_at')
    search_fields = ('username', 'email')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    actions = ['activate_users', 'deactivate_users']
    list_per_page = 25  # Muestra 25 usuarios por página
    
    # Campos personalizados en la lista
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Nombre Completo'
    
    def get_posts_count(self, obj):
        return obj.posts.count()
    get_posts_count.short_description = 'Posts'
    
    # Acciones personalizadas
    
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} usuarios activados exitosamente')
    activate_users.short_description = "Activar usuarios seleccionados"
    
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} usuarios desactivados exitosamente')
    deactivate_users.short_description = "Desactivar usuarios seleccionados"
    
    # Vista personalizada
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('stats/', self.admin_site.admin_view(self.user_stats_view), name='user-stats'),
        ]
        return custom_urls + urls
    
    def user_stats_view(self, request):
        context = {
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count(),
            'users_with_posts': User.objects.filter(posts__isnull=False).distinct().count(),
        }
        return render(request, 'admin/users/user_stats.html', context)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at', 'published_at', 'get_likes_count')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    
    # Campos personalizados en la lista
    def get_likes_count(self, obj):
        return obj.likes.count()
    get_likes_count.short_description = 'Likes'
    
    # Campos personalizados en el formulario
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and not obj.is_published:
            form.base_fields['content'].widget.attrs['style'] = 'height: 1000px;'
        return form
    
    # Acciones personalizadas
    actions = ['publish_posts', 'unpublish_posts']
    
    def publish_posts(self, request, queryset):
        for post in queryset:
            post.publish()
        self.message_user(request, f'{queryset.count()} posts publicados exitosamente')
    publish_posts.short_description = "Publicar posts seleccionados"
    
    def unpublish_posts(self, request, queryset):
        for post in queryset:
            post.unpublish()
        self.message_user(request, f'{queryset.count()} posts despublicados exitosamente')
    unpublish_posts.short_description = "Despublicar posts seleccionados"
    
    # Agrupación de campos
    fieldsets = (
        ('Información básica', {
            'fields': ('title', 'content', 'author'),
            'classes': ('wide',)
        }),
        ('Estado', {
            'fields': ('is_published', 'published_at'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Interacciones', {
            'fields': ('likes',),
            'classes': ('collapse',)
        }),
    )
    
    # Filtros personalizados
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')
