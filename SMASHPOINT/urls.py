"""
URL configuration for SMASHPOINT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from smashpointApp import views
from smashpointApp import mobile_views
from rest_framework.routers import DefaultRouter
from smashpointApp.api import (
    JugadorViewSet, TorneoViewSet, ResultadoViewSet,
    RankingViewSet, PartidoViewSet, InscripcionViewSet
)

router = DefaultRouter()
router.register(r'jugadores', JugadorViewSet)
router.register(r'torneos', TorneoViewSet)
router.register(r'resultados', ResultadoViewSet)
router.register(r'ranking', RankingViewSet)
router.register(r'partidos', PartidoViewSet)
router.register(r'inscripciones', InscripcionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index, name='index'),

    # Jugadores
    path('jugadores/', views.lista_jugadores, name='lista_jugadores'),
    path('jugadores/agregar/', views.agregar_jugador, name='agregar_jugador'),
    path('jugadores/editar/<int:id>/', views.editar_jugador, name='editar_jugador'),
    path('jugadores/eliminar/<int:id>/', views.eliminar_jugador, name='eliminar_jugador'),
    path('jugadores/importar/excel/', views.importar_jugadores_excel, name='importar_jugadores_excel'),

    # Torneos
    path('torneos/', views.lista_torneos, name='lista_torneos'),
    path('torneos/agregar/', views.agregar_torneo, name='agregar_torneo'),
    path('torneos/editar/<int:id>/', views.editar_torneo, name='editar_torneo'),
    path('torneos/eliminar/<int:id>/', views.eliminar_torneo, name='eliminar_torneo'),

    # Contacto
    path('contacto/', views.contacto, name='contacto'),

    # Inscripciones
    path('torneos/<int:torneo_id>/inscripciones/', views.lista_inscripciones, name='lista_inscripciones'),
    path('torneos/<int:torneo_id>/inscribir/', views.inscribir_jugador, name='inscribir_jugador'),

    # Partidos / Fixture
    path('torneos/<int:torneo_id>/fixture/generar/', views.generar_fixture, name='generar_fixture'),
    path('torneos/<int:torneo_id>/partidos/', views.lista_partidos, name='lista_partidos'),
    path('partidos/editar/<int:partido_id>/', views.editar_partido, name='editar_partido'),
    path('torneos/<int:torneo_id>/ronda/siguiente/', views.generar_ronda_siguiente, name='generar_ronda_siguiente'),
    # Grupos y Bracket
    path('torneos/<int:torneo_id>/grupos/generar/', views.generar_grupos, name='generar_grupos'),
    path('torneos/<int:torneo_id>/grupos/', views.lista_grupos, name='lista_grupos'),
    path('torneos/<int:torneo_id>/bracket/generar/', views.generar_bracket, name='generar_bracket'),
    path('torneos/<int:torneo_id>/bracket/', views.lista_bracket, name='lista_bracket'),
    path('torneos/<int:torneo_id>/bracket/ronda/siguiente/', views.generar_eliminacion_siguiente, name='generar_eliminacion_siguiente'),
    path('torneos/<int:torneo_id>/bracket/visual/', views.bracket_visual, name='bracket_visual'),
    
    # Público
    path('ranking/', views.ranking_public, name='ranking_public'),
    path('public/registro/', views.registro_jugador, name='registro_jugador'),
    path('public/jugador/<int:jugador_id>/', views.jugador_public, name='jugador_public'),
    path('public/jugador/<int:jugador_id>/qr/', views.jugador_qr, name='jugador_qr'),

    # Export / Import
    path('export/jugadores/', views.export_jugadores_csv, name='export_jugadores_csv'),
    path('export/torneos/', views.export_torneos_csv, name='export_torneos_csv'),
    path('export/resultados/', views.export_resultados_csv, name='export_resultados_csv'),
    path('import/jugadores/', views.import_jugadores_csv, name='import_jugadores_csv'),
    path('export/ranking/pdf/', views.export_ranking_pdf, name='export_ranking_pdf'),
    path('export/ranking/excel/', views.export_ranking_excel, name='export_ranking_excel'),

    # API JSON (Legacy)
    path('api/jugadores/', views.api_jugadores, name='api_jugadores'),
    path('api/torneos/', views.api_torneos, name='api_torneos'),
    path('api/ranking/', views.api_ranking, name='api_ranking'),

    # API Mobile (React Native) - CamelCase
    path('api/tournaments/', mobile_views.mobile_tournaments, name='mobile_tournaments'),
    path('api/tournaments/<int:tournament_id>/', mobile_views.mobile_tournament_detail, name='mobile_tournament_detail'),
    path('api/tournaments/<int:tournament_id>/matches/', mobile_views.mobile_tournament_matches, name='mobile_tournament_matches'),
    path('api/tournaments/<int:tournament_id>/players/', mobile_views.mobile_tournament_players, name='mobile_tournament_players'),
    path('api/players/', mobile_views.mobile_players, name='mobile_players'),
    path('api/results/', mobile_views.mobile_results, name='mobile_results'),
    path('api/matches/finish/', mobile_views.mobile_finish_match, name='mobile_finish_match'),

    # Offline
    path('offline/', views.offline, name='offline'),
    # API V2 (DRF)
    path('api/v2/', include(router.urls)),
]
