# 📱 Integración App Móvil - SmashPoint

## 🎯 Resumen Ejecutivo

La API REST de SmashPoint está **lista para conectarse con React Native**. Todos los endpoints devuelven respuestas en **camelCase** automáticamente gracias a `djangorestframework-camel-case`.

---

## ✅ Estado Actual

### Implementado
- ✅ Conversión automática snake_case → camelCase
- ✅ 7 endpoints específicos para app móvil
- ✅ Documentación completa en `API_MOBILE.md`
- ✅ Validaciones de datos
- ✅ Sin autenticación requerida (desarrollo)
- ✅ Desplegado en producción: `https://smashpoint-7ofo.onrender.com`

### Archivos Creados
1. `smashpointApp/mobile_serializers.py` - Serializers con conversión camelCase
2. `smashpointApp/mobile_views.py` - Vistas API específicas
3. `API_MOBILE.md` - Documentación técnica completa
4. `INTEGRACION_MOBILE.md` - Este archivo (resumen)

---

## 🔌 Endpoints Disponibles

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `/api/tournaments` | Lista de torneos |
| GET | `/api/tournaments/{id}` | Detalle de torneo |
| GET | `/api/tournaments/{id}/matches` | Partidos del torneo |
| GET | `/api/tournaments/{id}/players` | Jugadores inscritos |
| GET | `/api/players` | Lista de jugadores |
| GET | `/api/results` | Resultados históricos |
| POST | `/api/matches/finish` | Guardar resultado |

**Base URL Producción:** `https://smashpoint-7ofo.onrender.com`

---

## 📋 Ejemplo de Respuesta (camelCase)

### GET `/api/tournaments`
```json
[
  {
    "id": "1",
    "name": "Gran Torneo",
    "date": "10/12/2025",
    "location": "Gimnasio A",
    "status": "Activo",
    "registeredCount": 32
  }
]
```

### GET `/api/tournaments/1/matches`
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
  }
]
```

### POST `/api/matches/finish`
**Request:**
```json
{
  "matchId": "101",
  "winner": "Juan",
  "score": "3-1"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Partido actualizado correctamente",
  "matchId": "101"
}
```

---

## 🚀 Cómo Usar en React Native

### Instalación
No requiere configuración adicional en el backend. Solo hacer `fetch()` desde React Native.

### Ejemplo Básico
```javascript
// Obtener torneos
const fetchTournaments = async () => {
  const response = await fetch('https://smashpoint-7ofo.onrender.com/api/tournaments');
  const data = await response.json();
  
  // Los datos YA vienen en camelCase
  console.log(data[0].registeredCount); // ✅ Funciona
};
```

### Ejemplo POST
```javascript
// Guardar resultado de partido
const finishMatch = async () => {
  const response = await fetch(
    'https://smashpoint-7ofo.onrender.com/api/matches/finish',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        matchId: "101",      // camelCase
        winner: "Juan",
        score: "3-1"
      })
    }
  );
  
  const result = await response.json();
  console.log(result.success); // true/false
};
```

---

## ⚠️ Consideraciones Importantes

### 1. Nombres de Campos (CRÍTICO)
La app móvil debe usar **exactamente** estos nombres:

| Backend (Django) | API Response (camelCase) | React Native |
|------------------|--------------------------|--------------|
| `registered_count` | `registeredCount` | ✅ `data.registeredCount` |
| `match_id` | `matchId` | ✅ `matchId` |
| `tournament_id` | `tournamentId` | ✅ `tournamentId` |

### 2. Validaciones
- **Score**: Formato `"3-1"`, `"2-0"`, etc. (mejor de 3)
- **Winner**: Debe coincidir con nombre exacto del jugador
- **Match Status**: `"pending"`, `"live"`, `"finished"`

### 3. Sin Autenticación (Por Ahora)
- Todos los endpoints son públicos
- No requiere headers de autenticación
- Para producción futura: considerar JWT

---

## 🧪 Testing Rápido

### Desde Terminal (cURL)
```bash
# Obtener torneos
curl https://smashpoint-7ofo.onrender.com/api/tournaments

# Obtener partidos del torneo 1
curl https://smashpoint-7ofo.onrender.com/api/tournaments/1/matches

# Guardar resultado
curl -X POST https://smashpoint-7ofo.onrender.com/api/matches/finish \
  -H "Content-Type: application/json" \
  -d '{"matchId":"101","winner":"Juan","score":"3-1"}'
```

### Desde Navegador
Abre directamente en Chrome/Firefox:
```
https://smashpoint-7ofo.onrender.com/api/tournaments
https://smashpoint-7ofo.onrender.com/api/players
```

---

## 📖 Documentación Completa

Para más detalles técnicos, consulta:
- **`API_MOBILE.md`**: Especificación completa de todos los endpoints
- **`README.md`**: Documentación general del proyecto

---

## 🔄 Próximos Pasos

### Desarrollo App Móvil
1. Configurar `fetch()` con base URL de producción
2. Crear modelos TypeScript/JavaScript para respuestas
3. Implementar manejo de errores (network, 400, 404)
4. Probar cada endpoint con datos reales

### Backend (Opcional)
- [ ] Agregar paginación a `/api/results` si crece mucho
- [ ] Implementar JWT para autenticación
- [ ] Agregar filtros (ej: torneos por estado)
- [ ] WebSockets para actualizaciones en tiempo real

---

## 🐛 Troubleshooting

### "No se muestran los datos"
✅ Verificar que los nombres de campos sean camelCase en React Native
✅ Revisar console.log del response completo
✅ Confirmar que la URL sea correcta (https, no http)

### "matchId is not defined"
✅ Enviar `matchId` (camelCase), no `match_id`

### "Winner no coincide"
✅ El nombre del ganador debe ser exactamente como aparece en `p1` o `p2`

---

## 📞 Contacto Desarrollo

**Backend (Django):** Alexandre Alvarado
- GitHub: [@Alexandre-Alvarado](https://github.com/Alexandre-Alvarado)
- Repo: [Smashpoint](https://github.com/Alexandre-Alvarado/Smashpoint)

**Issues:** [GitHub Issues](https://github.com/Alexandre-Alvarado/Smashpoint/issues)

---

## ✨ Changelog

### v1.1.0 (11 Diciembre 2025)
- ✅ API móvil implementada
- ✅ Conversión automática camelCase
- ✅ 7 endpoints funcionales
- ✅ Documentación completa
- ✅ Deploy en Render exitoso

---

**Estado:** 🟢 LISTO PARA INTEGRACIÓN

**URL Base:** `https://smashpoint-7ofo.onrender.com`

**Última actualización:** 11 de Diciembre 2025
