from django.contrib import admin
from .models import Jugador, Torneo, Resultado, Inscripcion, Partido, Ranking, Grupo

@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','apellido','categoria','rut')
	search_fields = ('nombre','apellido','rut')
	list_filter = ('categoria',)

@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre','fecha','categoria','estado','cupos_max')
	list_filter = ('categoria','estado')
	search_fields = ('nombre',)

@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
	list_display = ('id','torneo','jugador1','jugador2','marcador_j1','marcador_j2')
	list_filter = ('torneo',)

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
	list_display = ('id','torneo','jugador','estado','fecha_inscripcion')
	list_filter = ('estado','torneo')

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
	list_display = ('id','torneo','etapa','grupo','ronda','jugador_a','jugador_b','ganador','best_of','sets_a','sets_b')
	list_filter = ('torneo','ronda','etapa','grupo')
	search_fields = ('jugador_a__nombre','jugador_b__nombre')

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('id','torneo','nombre','cantidad_jugadores')
    list_filter = ('torneo',)
    filter_horizontal = ('jugadores',)
    
    def cantidad_jugadores(self, obj):
        return obj.jugadores.count()
    cantidad_jugadores.short_description = 'Jugadores'

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
	list_display = ('jugador','puntos','actualizado_en')
	search_fields = ('jugador__nombre','jugador__apellido')
