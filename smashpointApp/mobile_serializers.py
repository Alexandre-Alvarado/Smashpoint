"""
API Serializers para App Móvil con camelCase
Estos serializers están diseñados específicamente para la integración con React Native
"""
from rest_framework import serializers
from .models import Torneo, Jugador, Partido, Inscripcion, Resultado


class MobileTournamentSerializer(serializers.ModelSerializer):
    """Serializer para lista de torneos en app móvil"""
    registered_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Torneo
        fields = ['id', 'nombre', 'fecha', 'direccion', 'estado', 'registered_count']
    
    def get_registered_count(self, obj):
        """Retorna cantidad de jugadores inscritos"""
        return obj.inscripcion_set.filter(estado='INSCRITO').count()
    
    def to_representation(self, instance):
        """Convierte snake_case a camelCase"""
        ret = super().to_representation(instance)
        return {
            'id': str(ret['id']),
            'name': ret['nombre'],
            'date': str(ret['fecha']) if ret['fecha'] else '',
            'location': ret['direccion'],
            'status': ret['estado'],
            'registeredCount': ret['registered_count']
        }


class MobilePlayerSerializer(serializers.ModelSerializer):
    """Serializer para lista de jugadores en app móvil"""
    
    class Meta:
        model = Jugador
        fields = ['id', 'nombre', 'apellido', 'categoria', 'origen']
    
    def to_representation(self, instance):
        """Convierte a formato camelCase para app móvil"""
        ret = super().to_representation(instance)
        nombre_completo = f"{ret['nombre']} {ret['apellido']}"
        
        # Obtener puntos del ranking si existe
        from .models import Ranking
        ranking = Ranking.objects.filter(jugador=instance).first()
        puntos = ranking.puntos if ranking else 0
        
        return {
            'id': str(ret['id']),
            'name': nombre_completo,
            'category': ret['categoria'],
            'points': puntos,
            'club': ret.get('origen', 'Sin club')
        }


class MobileMatchSerializer(serializers.ModelSerializer):
    """Serializer para partidos en detalle de torneo"""
    
    class Meta:
        model = Partido
        fields = ['id', 'jugador_a', 'jugador_b', 'ronda', 'sets_a', 'sets_b', 'ganador']
    
    def to_representation(self, instance):
        """Convierte a formato camelCase"""
        ret = super().to_representation(instance)
        
        # Determinar estado del partido
        if instance.ganador:
            status = 'finished'
            time = 'Finalizado'
            score = f"{instance.sets_a or 0}-{instance.sets_b or 0}"
        elif instance.sets_a is not None or instance.sets_b is not None:
            status = 'live'
            time = 'En Juego'
            score = f"{instance.sets_a or 0}-{instance.sets_b or 0}"
        else:
            status = 'pending'
            time = 'Pendiente'
            score = "0-0"
        
        # Nombres de jugadores
        p1_name = instance.jugador_a.nombre if instance.jugador_a else "BYE"
        p2_name = instance.jugador_b.nombre if instance.jugador_b else "BYE"
        
        # Determinar fase
        fase_map = {
            1: 'Final',
            2: 'Semifinal',
            3: 'Cuartos',
            4: 'Octavos',
        }
        phase = fase_map.get(instance.ronda, f'Ronda {instance.ronda}')
        
        return {
            'id': str(ret['id']),
            'p1': p1_name,
            'p2': p2_name,
            'phase': phase,
            'status': status,
            'time': time,
            'score': score
        }


class MobileTournamentPlayerSerializer(serializers.ModelSerializer):
    """Serializer para jugadores inscritos en un torneo"""
    rank = serializers.SerializerMethodField()
    
    class Meta:
        model = Jugador
        fields = ['id', 'nombre', 'origen', 'rank']
    
    def get_rank(self, obj):
        """Obtener posición en ranking"""
        from .models import Ranking
        ranking = Ranking.objects.filter(jugador=obj).first()
        if ranking:
            # Calcular posición ordenando por puntos
            pos = Ranking.objects.filter(puntos__gt=ranking.puntos).count() + 1
            return pos
        return 0
    
    def to_representation(self, instance):
        """Convierte a formato camelCase"""
        ret = super().to_representation(instance)
        return {
            'id': str(ret['id']),
            'name': ret['nombre'],
            'club': ret.get('origen', 'Sin club'),
            'rank': ret['rank']
        }


class MobileResultSerializer(serializers.ModelSerializer):
    """Serializer para resultados históricos"""
    
    class Meta:
        model = Resultado
        fields = ['id', 'torneo', 'jugador1', 'jugador2', 'marcador_j1', 'marcador_j2']
    
    def to_representation(self, instance):
        """Convierte a formato camelCase"""
        ret = super().to_representation(instance)
        
        p1_name = instance.jugador1.nombre if instance.jugador1 else "Desconocido"
        p2_name = instance.jugador2.nombre if instance.jugador2 else "Desconocido"
        tournament_name = instance.torneo.nombre if instance.torneo else "Torneo"
        
        # Construir score
        score = f"{ret.get('marcador_j1', 0)} - {ret.get('marcador_j2', 0)}"
        
        # Fecha (asumiendo que Torneo tiene fecha)
        fecha = instance.torneo.fecha.strftime('%d/%m/%Y') if instance.torneo and instance.torneo.fecha else ""
        
        return {
            'id': str(ret['id']),
            'tournament': tournament_name,
            'p1': p1_name,
            'p2': p2_name,
            'score': score,
            'date': fecha
        }


class MobileMatchFinishSerializer(serializers.Serializer):
    """Serializer para guardar resultado de partido (POST)"""
    match_id = serializers.IntegerField(required=True)
    winner = serializers.CharField(required=True, max_length=100)
    score = serializers.CharField(required=True, max_length=20)
    
    def validate_score(self, value):
        """Valida formato de score (ej: 3-1)"""
        try:
            parts = value.split('-')
            if len(parts) != 2:
                raise serializers.ValidationError("Score debe tener formato '3-1'")
            int(parts[0])
            int(parts[1])
        except (ValueError, IndexError):
            raise serializers.ValidationError("Score inválido")
        return value
    
    def save(self):
        """Guarda el resultado del partido"""
        match_id = self.validated_data['match_id']
        winner_name = self.validated_data['winner']
        score = self.validated_data['score']
        
        try:
            partido = Partido.objects.get(id=match_id)
            sets_a, sets_b = map(int, score.split('-'))
            
            # Determinar ganador
            if partido.jugador_a and partido.jugador_a.nombre == winner_name:
                partido.ganador = partido.jugador_a
            elif partido.jugador_b and partido.jugador_b.nombre == winner_name:
                partido.ganador = partido.jugador_b
            else:
                raise serializers.ValidationError("Winner no coincide con jugadores del partido")
            
            partido.sets_a = sets_a
            partido.sets_b = sets_b
            partido.save()
            
            return partido
        except Partido.DoesNotExist:
            raise serializers.ValidationError("Partido no encontrado")
