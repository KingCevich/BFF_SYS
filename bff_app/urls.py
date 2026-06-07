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
]
