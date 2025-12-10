from rest_framework import serializers
from .models import Jugador, Torneo, Resultado, Ranking, Partido, Inscripcion

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jugador
        fields = ['id','nombre','apellido','categoria','licencia']

class TorneoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torneo
        fields = ['id','nombre','direccion','fecha','categoria','cupos_max','estado','total_rondas']

class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = ['id','torneo','jugador1','jugador2','marcador_j1','marcador_j2']

class RankingSerializer(serializers.ModelSerializer):
    jugador = JugadorSerializer(read_only=True)
    class Meta:
        model = Ranking
        fields = ['id','jugador','puntos']

class PartidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partido
        fields = ['id','torneo','ronda','jugador_a','jugador_b','marcador_a','marcador_b','ganador']

class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = ['id','torneo','jugador','estado','fecha_inscripcion']
