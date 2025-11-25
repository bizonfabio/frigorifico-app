"""
URL configuration for frigorifico_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.registro_inicial, name='registro_inicial'),
    path('registrar/gta/', views.registrar_gta, name='registrar_gta'),
    path('registrar/animais/', views.registrar_animais, name='registrar_animais'),
    path('lista-avaliacao/', views.lista_animais_para_avaliacao, name='lista_animais_para_avaliacao'),
    path('avaliar/<int:id>/', views.avaliar_animal, name='avaliar_animal'),
    path('lista-classificacao/', views.lista_animais_para_classificacao, name='lista_animais_para_classificacao'),
    path('classificar/<int:id>/', views.classificar_animal, name='classificar_animal'),
    path('lista-estoque/', views.lista_animais_para_estoque, name='lista_animais_para_estoque'),
    path('enviar-estoque/<int:id>/', views.enviar_para_estoque, name='enviar_para_estoque'),
    path('visualizar-estoque/', views.visualizar_estoque, name='visualizar_estoque'),
    path('pesquisar-estoque/', views.pesquisar_estoque, name='pesquisar_estoque'),
    path('resumo-estoque/', views.resumo_estoque, name='resumo_estoque'),
    path('ordem-abate/', views.ordem_abate, name='ordem_abate'),
    path('atualizar-ordem-abate/', views.atualizar_ordem_abate, name='atualizar_ordem_abate'),
    path('relatorio-diario/', views.relatorio_diario, name='relatorio_diario'),
]