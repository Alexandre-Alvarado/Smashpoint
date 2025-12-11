"""
Script de Testing para API Móvil
Ejecutar: python test_mobile_api.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SMASHPOINT.settings')
django.setup()

from smashpointApp.models import Torneo, Jugador, Partido
from smashpointApp.mobile_serializers import (
    MobileTournamentSerializer,
    MobilePlayerSerializer,
    MobileMatchSerializer
)

def test_tournament_serializer():
    """Test serializer de torneos"""
    print("\n🏆 Testing Tournament Serializer...")
    torneos = Torneo.objects.all()[:2]
    
    if torneos:
        serializer = MobileTournamentSerializer(torneos, many=True)
        data = serializer.data
        
        print(f"✅ {len(data)} torneos serializados")
        if data:
            print(f"   Campos: {list(data[0].keys())}")
            print(f"   Ejemplo: {data[0]}")
    else:
        print("⚠️  No hay torneos en la BD")

def test_player_serializer():
    """Test serializer de jugadores"""
    print("\n👤 Testing Player Serializer...")
    jugadores = Jugador.objects.all()[:2]
    
    if jugadores:
        serializer = MobilePlayerSerializer(jugadores, many=True)
        data = serializer.data
        
        print(f"✅ {len(data)} jugadores serializados")
        if data:
            print(f"   Campos: {list(data[0].keys())}")
            print(f"   Ejemplo: {data[0]}")
    else:
        print("⚠️  No hay jugadores en la BD")

def test_match_serializer():
    """Test serializer de partidos"""
    print("\n🎾 Testing Match Serializer...")
    partidos = Partido.objects.all()[:2]
    
    if partidos:
        serializer = MobileMatchSerializer(partidos, many=True)
        data = serializer.data
        
        print(f"✅ {len(data)} partidos serializados")
        if data:
            print(f"   Campos: {list(data[0].keys())}")
            print(f"   Ejemplo: {data[0]}")
    else:
        print("⚠️  No hay partidos en la BD")

def test_camelcase_conversion():
    """Test conversión camelCase"""
    print("\n🔄 Testing CamelCase Conversion...")
    
    torneo = Torneo.objects.first()
    if torneo:
        serializer = MobileTournamentSerializer(torneo)
        data = serializer.data
        
        # Verificar que los campos estén en camelCase
        expected_fields = ['id', 'name', 'date', 'location', 'status', 'registeredCount']
        
        for field in expected_fields:
            if field in data:
                print(f"   ✅ {field}: {data[field]}")
            else:
                print(f"   ❌ {field}: MISSING")
        
        # Verificar que NO haya snake_case
        snake_case_fields = ['registered_count', 'tournament_id']
        for field in snake_case_fields:
            if field in data:
                print(f"   ⚠️  {field}: Encontrado (debería ser camelCase)")
    else:
        print("⚠️  No hay torneos para testear")

if __name__ == '__main__':
    print("="*50)
    print("Testing API Móvil - SmashPoint")
    print("="*50)
    
    try:
        test_tournament_serializer()
        test_player_serializer()
        test_match_serializer()
        test_camelcase_conversion()
        
        print("\n" + "="*50)
        print("✅ Tests completados")
        print("="*50)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
