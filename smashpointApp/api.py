from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .permissions import WritePermissionByModelPerm
from .models import Jugador, Torneo, Resultado, Ranking, Partido, Inscripcion
from .serializers import (
    JugadorSerializer, TorneoSerializer, ResultadoSerializer,
    RankingSerializer, PartidoSerializer, InscripcionSerializer
)

class ReadOnlyModelViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    permission_classes = [AllowAny]

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all().order_by('id')
    serializer_class = JugadorSerializer
    permission_classes = [WritePermissionByModelPerm]

class TorneoViewSet(viewsets.ModelViewSet):
    queryset = Torneo.objects.all().order_by('-fecha')
    serializer_class = TorneoSerializer
    permission_classes = [WritePermissionByModelPerm]

class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.select_related('torneo','jugador1','jugador2').all().order_by('-id')
    serializer_class = ResultadoSerializer
    permission_classes = [WritePermissionByModelPerm]

class RankingViewSet(ReadOnlyModelViewSet):
    queryset = Ranking.objects.select_related('jugador').order_by('-puntos')
    serializer_class = RankingSerializer

class PartidoViewSet(ReadOnlyModelViewSet):
    queryset = Partido.objects.select_related('torneo','jugador_a','jugador_b','ganador').order_by('torneo','ronda')
    serializer_class = PartidoSerializer

class InscripcionViewSet(ReadOnlyModelViewSet):
    queryset = Inscripcion.objects.select_related('torneo','jugador').order_by('-fecha_inscripcion')
    serializer_class = InscripcionSerializer
