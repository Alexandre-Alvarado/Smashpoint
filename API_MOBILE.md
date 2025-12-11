# API para App Móvil - SmashPoint

## 📱 Especificación para React Native

Esta API está diseñada específicamente para la integración con aplicaciones móviles desarrolladas en React Native. Todas las respuestas utilizan **camelCase** para coincidir con las convenciones de JavaScript.

---

## 🔧 Configuración Técnica

### Naming Convention
- **Backend (Django)**: snake_case (ej: `registered_count`)
- **Frontend (React Native)**: camelCase (ej: `registeredCount`)
- **Conversión automática**: `djangorestframework-camel-case`

### Base URL
- **Producción**: `https://smashpoint-7ofo.onrender.com`
- **Local**: `http://127.0.0.1:8000`

---

## 📋 Endpoints Disponibles

### 1. 🏆 Lista de Torneos
**GET** `/api/tournaments`

Obtiene todos los torneos con información básica.

**Respuesta (JSON):**
```json
[
  {
    "id": "1",
    "name": "Gran Torneo",
    "date": "10/12/2025",
    "location": "Gimnasio A",
    "status": "Activo",
    "registeredCount": 32
  },
  {
    "id": "2",
    "name": "Copa Verano",
    "date": "15/12/2025",
    "location": "Polideportivo B",
    "status": "Abierto",
    "registeredCount": 15
  }
]
```

**Campos:**
- `id` (string): ID del torneo
- `name` (string): Nombre del torneo
- `date` (string): Fecha en formato DD/MM/YYYY
- `location` (string): Dirección del evento
- `status` (string): Estado del torneo (Abierto, En Curso, Finalizado)
- `registeredCount` (number): Cantidad de jugadores inscritos

---

### 2. 👤 Lista de Jugadores
**GET** `/api/players`

Obtiene todos los jugadores registrados con sus puntos de ranking.

**Respuesta (JSON):**
```json
[
  {
    "id": "1",
    "name": "Juan Pérez",
    "category": "Amateur",
    "points": 1200,
    "club": "Club Central"
  },
  {
    "id": "2",
    "name": "María González",
    "category": "Federado",
    "points": 850,
    "club": "Club Norte"
  }
]
```

**Campos:**
- `id` (string): ID del jugador
- `name` (string): Nombre completo
- `category` (string): Categoría (Amateur, Federado)
- `points` (number): Puntos acumulados en ranking
- `club` (string): Club de origen

---

### 3. 📄 Detalle de Torneo
**GET** `/api/tournaments/<id>`

Obtiene información detallada de un torneo específico.

**Respuesta (JSON):**
```json
{
  "id": "1",
  "name": "Gran Torneo",
  "date": "10/12/2025",
  "location": "Gimnasio A",
  "status": "En Curso",
  "registeredCount": 32,
  "description": "Torneo de categoría Juvenil",
  "maxPlayers": 64,
  "currentRound": 3
}
```

---

### 4. 🎾 Partidos de un Torneo
**GET** `/api/tournaments/<id>/matches`

Obtiene todos los partidos de un torneo específico.

**Respuesta (JSON):**
```json
[
  {
    "id": "101",
    "p1": "Juan",
    "p2": "Pedro",
    "phase": "Final",
    "status": "live",
    "time": "En Juego",
    "score": "2-1"
  },
  {
    "id": "102",
    "p1": "María",
    "p2": "Ana",
    "phase": "Semifinal",
    "status": "finished",
    "time": "Finalizado",
    "score": "3-0"
  },
  {
    "id": "103",
    "p1": "Luis",
    "p2": "Carlos",
    "phase": "Cuartos",
    "status": "pending",
    "time": "Pendiente",
    "score": "0-0"
  }
]
```

**Campos:**
- `id` (string): ID del partido
- `p1` (string): Nombre del jugador 1
- `p2` (string): Nombre del jugador 2
- `phase` (string): Fase del torneo (Final, Semifinal, Cuartos, etc.)
- `status` (string): Estado del partido
  - `"pending"`: Pendiente
  - `"live"`: En juego
  - `"finished"`: Finalizado
- `time` (string): Descripción temporal
- `score` (string): Marcador en formato "X-Y"

---

### 5. 👥 Jugadores Inscritos en Torneo
**GET** `/api/tournaments/<id>/players`

Obtiene la lista de jugadores inscritos en un torneo.

**Respuesta (JSON):**
```json
[
  {
    "id": "1",
    "name": "Juan Pérez",
    "club": "Club Central",
    "rank": 1
  },
  {
    "id": "2",
    "name": "María González",
    "club": "Club Norte",
    "rank": 3
  }
]
```

**Campos:**
- `id` (string): ID del jugador
- `name` (string): Nombre completo
- `club` (string): Club de origen
- `rank` (number): Posición en ranking general

---

### 6. 📝 Resultados Históricos
**GET** `/api/results`

Obtiene los últimos 50 resultados de partidos finalizados.

**Respuesta (JSON):**
```json
[
  {
    "id": "50",
    "tournament": "Copa Verano",
    "p1": "Luis",
    "p2": "Ana",
    "score": "3 - 1",
    "date": "09/12/2025"
  },
  {
    "id": "49",
    "tournament": "Gran Torneo",
    "p1": "Juan",
    "p2": "Pedro",
    "score": "2 - 3",
    "date": "08/12/2025"
  }
]
```

**Campos:**
- `id` (string): ID del resultado
- `tournament` (string): Nombre del torneo
- `p1` (string): Nombre del jugador 1
- `p2` (string): Nombre del jugador 2
- `score` (string): Marcador final
- `date` (string): Fecha en formato DD/MM/YYYY

---

### 7. ✅ Guardar Resultado de Partido (POST)
**POST** `/api/matches/finish`

Registra el resultado final de un partido.

**Request Body (JSON):**
```json
{
  "matchId": "101",
  "winner": "Juan",
  "score": "3-1"
}
```

**Campos requeridos:**
- `matchId` (string): ID del partido a finalizar
- `winner` (string): Nombre del jugador ganador (debe coincidir con `p1` o `p2`)
- `score` (string): Marcador final en formato "X-Y" (mejor de 3, máximo 3-2)

**Respuesta exitosa (200 OK):**
```json
{
  "success": true,
  "message": "Partido actualizado correctamente",
  "matchId": "101"
}
```

**Respuesta con error (400 Bad Request):**
```json
{
  "success": false,
  "message": "Winner no coincide con jugadores del partido"
}
```

o

```json
{
  "success": false,
  "errors": {
    "score": ["Score debe tener formato '3-1'"]
  }
}
```

---

## 🔐 Autenticación

**Nota importante**: La API actual está configurada con `AllowAny`, por lo que **NO requiere autenticación** para ningún endpoint. Esto es adecuado para desarrollo, pero para producción se recomienda implementar autenticación JWT.

### Para futuras versiones (JWT):
```bash
pip install djangorestframework-simplejwt
```

---

## 📡 Ejemplos de Uso

### React Native (JavaScript/TypeScript)

#### 1. Obtener torneos
```javascript
const fetchTournaments = async () => {
  try {
    const response = await fetch('https://smashpoint-7ofo.onrender.com/api/tournaments');
    const data = await response.json();
    console.log(data);
    // data[0].registeredCount (camelCase automático)
  } catch (error) {
    console.error('Error:', error);
  }
};
```

#### 2. Obtener partidos de un torneo
```javascript
const fetchMatches = async (tournamentId) => {
  const response = await fetch(
    `https://smashpoint-7ofo.onrender.com/api/tournaments/${tournamentId}/matches`
  );
  const matches = await response.json();
  return matches;
};
```

#### 3. Guardar resultado de partido
```javascript
const finishMatch = async (matchId, winner, score) => {
  try {
    const response = await fetch(
      'https://smashpoint-7ofo.onrender.com/api/matches/finish',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          matchId: matchId,      // camelCase
          winner: winner,
          score: score
        })
      }
    );
    
    const result = await response.json();
    
    if (result.success) {
      console.log('Partido guardado:', result.matchId);
    } else {
      console.error('Error:', result.message);
    }
  } catch (error) {
    console.error('Error de red:', error);
  }
};

// Uso:
finishMatch("101", "Juan", "3-1");
```

---

## 🧪 Testing con cURL

### Obtener torneos
```bash
curl https://smashpoint-7ofo.onrender.com/api/tournaments
```

### Obtener jugadores
```bash
curl https://smashpoint-7ofo.onrender.com/api/players
```

### Obtener partidos de torneo ID 1
```bash
curl https://smashpoint-7ofo.onrender.com/api/tournaments/1/matches
```

### Guardar resultado de partido
```bash
curl -X POST https://smashpoint-7ofo.onrender.com/api/matches/finish \
  -H "Content-Type: application/json" \
  -d '{
    "matchId": "101",
    "winner": "Juan",
    "score": "3-1"
  }'
```

---

## ⚠️ Validaciones Importantes

### Score Format
- **Válidos**: `"3-1"`, `"2-0"`, `"3-2"`
- **Inválidos**: `"3:1"`, `"3-4"` (máximo 3 sets), `"abc"`

### Winner Name
- Debe coincidir **exactamente** con el nombre del jugador en el partido
- Case-sensitive: `"Juan"` ≠ `"juan"`

### Match Status
- Solo se pueden editar partidos en estado `"pending"` o `"live"`
- Partidos `"finished"` requieren edición manual desde el panel web

---

## 🚀 Deployment

### Variables de Entorno (Render)
No se requieren variables adicionales. La conversión camelCase está configurada automáticamente.

### Dependencias necesarias
```txt
Django==4.2.7
djangorestframework==3.14.0
djangorestframework-camel-case==1.4.2
```

---

## 📞 Soporte

Para reportar bugs o solicitar cambios en la API:
- **GitHub Issues**: [SmashPoint Issues](https://github.com/Alexandre-Alvarado/Smashpoint/issues)
- **Email**: Contactar al equipo de desarrollo

---

## 🔄 Changelog

### v1.1.0 (Diciembre 2025)
- ✅ Implementación de API móvil con camelCase
- ✅ 7 endpoints específicos para React Native
- ✅ Conversión automática de naming conventions
- ✅ Validación de resultados de partidos
- ✅ Documentación completa de API

---

**Última actualización:** 11 de Diciembre 2025
