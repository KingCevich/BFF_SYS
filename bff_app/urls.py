from django.urls import path
from . import views
from .views import entidades_list, entidades_detail

urlpatterns = [
    #Endpoints de AUTH_SERV para login y refresh de tokens
    path('login/', views.login_bff, name='login_bff'),
    path('refresh/', views.refresh_bff, name='refresh_bff'),

    #Endpoints de USUARIOS_SERV para usuarios, perfiles y preferencias
    path('usuarios/', views.usuarios_list, name='usuarios_list'),
    path('usuarios/<int:pk>/', views.usuarios_detail, name='usuarios_detail'),

    path('perfiles/', views.perfiles_list, name='perfiles_list'),
    path('perfiles/<int:pk>/', views.perfiles_detail, name='perfiles_detail'),
    
    path('preferencias/', views.preferencias_list, name='preferencias_list'),
    path('preferencias/<int:pk>/', views.preferencias_detail, name='preferencias_detail'),

    #Endpoints de MASCOTAS_SERV para reportes y contactos
    path('reportes/', views.reportes_list, name='reportes_list'),
    path('reportes/<int:pk>/', views.reportes_detail, name='reportes_detail'),

    path('contactos/', views.contactos_list, name='contactos_list'),
    path('contactos/<int:pk>/', views.contactos_detail, name='contactos_detail'),
    path('entidades/', entidades_list, name='entidades_list'),
    path('entidades/<int:pk>/', entidades_detail, name='entidades_detail'),

    #Endpoints de Noticias_serv para noticias
    path('noticias/', views.noticias_list, name='noticias_list'),
    path('noticias/<int:pk>/', views.noticias_detail, name='noticias_detail'),

    #Endpoints de Notificaciones_serv para notificaciones
    path('notificaciones/usuario/',                          views.notificaciones_usuario,            name='notificaciones_usuario'),
    path('notificaciones/no-leidas/',                        views.notificaciones_no_leidas,          name='notificaciones_no_leidas'),
    path('notificaciones/<int:pk>/marcar-leida/',            views.notificaciones_marcar_leida,       name='notificaciones_marcar_leida'),
    path('notificaciones/marcar-todas-leidas/',              views.notificaciones_marcar_todas_leidas, name='notificaciones_marcar_todas_leidas'),

    #Enpoint imgbb para subir fotos (usado por el frontend al crear reportes)
    path('upload/', views.upload_foto),
]
