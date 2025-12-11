"""
API Views para App Móvil
Endpoints diseñados específicamente para React Native con respuestas en camelCase
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Torneo, Jugador, Partido, Inscripcion, Resultado
from .mobile_serializers import (
    MobileTournamentSerializer,
    MobilePlayerSerializer,
    MobileMatchSerializer,
    MobileTournamentPlayerSerializer,
    MobileResultSerializer,
    MobileMatchFinishSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_tournaments(request):
    """
    GET /api/tournaments
    Lista de todos los torneos con información básica
    """
    torneos = Torneo.objects.all().order_by('-fecha')
    serializer = MobileTournamentSerializer(torneos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_players(request):
    """
    GET /api/players
    Lista de todos los jugadores con puntos y categoría
    """
    jugadores = Jugador.objects.all().order_by('apellido', 'nombre')
    serializer = MobilePlayerSerializer(jugadores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_tournament_matches(request, tournament_id):
    """
    GET /api/tournaments/<id>/matches
    Lista de partidos de un torneo específico
    """
    torneo = get_object_or_404(Torneo, pk=tournament_id)
    partidos = Partido.objects.filter(torneo=torneo).select_related(
        'jugador_a', 'jugador_b', 'ganador'
    ).order_by('ronda', 'id')
    
    serializer = MobileMatchSerializer(partidos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_tournament_players(request, tournament_id):
    """
    GET /api/tournaments/<id>/players
    Lista de jugadores inscritos en un torneo
    """
    torneo = get_object_or_404(Torneo, pk=tournament_id)
    inscripciones = Inscripcion.objects.filter(
        torneo=torneo, 
        estado='INSCRITO'
    ).select_related('jugador')
    
    jugadores = [insc.jugador for insc in inscripciones]
    serializer = MobileTournamentPlayerSerializer(jugadores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_results(request):
    """
    GET /api/results
    Resultados históricos de todos los torneos
    """
    resultados = Resultado.objects.select_related(
        'torneo', 'jugador1', 'jugador2'
    ).all().order_by('-id')[:50]  # Últimos 50 resultados
    
    serializer = MobileResultSerializer(resultados, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_finish_match(request):
    """
    POST /api/matches/finish
    Guardar resultado de un partido
    
    Body esperado (camelCase):
    {
        "matchId": "101",
        "winner": "Juan",
        "score": "3-1"
    }
    """
    # Convertir camelCase a snake_case manualmente
    data = {
        'match_id': request.data.get('matchId'),
        'winner': request.data.get('winner'),
        'score': request.data.get('score')
    }
    
    serializer = MobileMatchFinishSerializer(data=data)
    
    if serializer.is_valid():
        try:
            partido = serializer.save()
            return Response({
                'success': True,
                'message': 'Partido actualizado correctamente',
                'matchId': str(partido.id)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def mobile_tournament_detail(request, tournament_id):
    """
    GET /api/tournaments/<id>
    Detalle completo de un torneo
    """
    torneo = get_object_or_404(Torneo, pk=tournament_id)
    serializer = MobileTournamentSerializer(torneo)
    
    # Agregar información adicional
    data = serializer.data
    data['description'] = f"Torneo de categoría {torneo.categoria}"
    data['maxPlayers'] = torneo.cupos_max
    data['currentRound'] = torneo.total_rondas or 0
    
    return Response(data)
