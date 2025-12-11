# 📨 Mensaje para el Desarrollador de la App Móvil (React Native)

---

## Asunto: API Lista para Integración con React Native ✅

Hola,

La API REST de **SmashPoint** está **completamente lista** para conectarse con tu app móvil. He implementado exactamente lo que solicitaste: todas las respuestas vienen en **camelCase** automáticamente.

---

## ✅ ¿Qué está Listo?

1. **✅ Conversión automática camelCase**
   - Django serializa en `snake_case` pero la API devuelve `camelCase`
   - Implementado con: `djangorestframework-camel-case`
   - No necesitas hacer conversiones manuales en React Native

2. **✅ 7 Endpoints específicos para tu app**
   - Todos documentados con ejemplos de código
   - Respuestas en el formato exacto que especificaste

3. **✅ Sin autenticación requerida**
   - Todos los endpoints son públicos (por ahora)
   - No necesitas headers de autenticación

4. **✅ Deploy en producción**
   - URL: `https://smashpoint-7ofo.onrender.com`
   - 100% funcional y disponible 24/7

---

## 🔌 Endpoints Disponibles

### A. 🏆 Torneos
**GET** `/api/tournaments`

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

### B. 👤 Jugadores
**GET** `/api/players`

```json
[
  {
    "id": "1",
    "name": "Juan Pérez",
    "category": "Amateur",
    "points": 1200,
    "club": "Club Central"
  }
]
```

### C. 📄 Detalle Torneo (Partidos)
**GET** `/api/tournaments/<id>/matches`

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

**Valores de `status`:**
- `"pending"`: Partido pendiente
- `"live"`: En juego
- `"finished"`: Finalizado

### D. 📄 Detalle Torneo (Jugadores Inscritos)
**GET** `/api/tournaments/<id>/players`

```json
[
  {
    "id": "1",
    "name": "Juan",
    "club": "Club Central",
    "rank": 1
  }
]
```

### E. 📝 Resultados Históricos
**GET** `/api/results`

```json
[
  {
    "id": "50",
    "tournament": "Copa Verano",
    "p1": "Luis",
    "p2": "Ana",
    "score": "3 - 1",
    "date": "09/12/2025"
  }
]
```

### F. 🏁 Guardar Partido (POST)
**POST** `/api/matches/finish`

**Request Body:**
```json
{
  "matchId": "101",
  "winner": "Juan",
  "score": "3-1"
}
```

**Response (Éxito):**
```json
{
  "success": true,
  "message": "Partido actualizado correctamente",
  "matchId": "101"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Winner no coincide con jugadores del partido"
}
```

---

## 🚀 Cómo Integrar en React Native

### 1. Configurar Base URL
```javascript
const API_BASE_URL = 'https://smashpoint-7ofo.onrender.com';
```

### 2. Ejemplo: Obtener Torneos
```javascript
const fetchTournaments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/tournaments`);
    const data = await response.json();
    
    // Los datos YA vienen en camelCase
    console.log(data[0].registeredCount); // ✅ Funciona
    console.log(data[0].name);            // ✅ Funciona
    
    return data;
  } catch (error) {
    console.error('Error:', error);
  }
};
```

### 3. Ejemplo: Obtener Partidos de un Torneo
```javascript
const fetchMatches = async (tournamentId) => {
  const response = await fetch(
    `${API_BASE_URL}/api/tournaments/${tournamentId}/matches`
  );
  const matches = await response.json();
  
  matches.forEach(match => {
    console.log(`${match.p1} vs ${match.p2} - ${match.score}`);
  });
  
  return matches;
};
```

### 4. Ejemplo: Guardar Resultado
```javascript
const finishMatch = async (matchId, winner, score) => {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/matches/finish`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          matchId: matchId,    // camelCase ✅
          winner: winner,
          score: score
        })
      }
    );
    
    const result = await response.json();
    
    if (result.success) {
      console.log('✅ Partido guardado');
      return true;
    } else {
      console.error('❌ Error:', result.message);
      return false;
    }
  } catch (error) {
    console.error('Error de red:', error);
    return false;
  }
};

// Uso:
await finishMatch("101", "Juan", "3-1");
```

---

## ⚠️ IMPORTANTE: Validaciones

### 1. Score Format
- **Válidos**: `"3-1"`, `"2-0"`, `"3-2"` (mejor de 3 sets)
- **Inválidos**: `"3:1"`, `"3-4"`, `"abc"`

### 2. Winner Name
- Debe coincidir **exactamente** con el nombre en `p1` o `p2`
- Case-sensitive: `"Juan"` ≠ `"juan"`
- Espacios importan: `"Juan Pérez"` ≠ `"JuanPérez"`

### 3. Match ID
- Debe ser un ID válido de partido existente
- Si el partido ya está finalizado, dará error

---

## 🧪 Testing Rápido

### Desde Terminal (cURL)
```bash
# Obtener torneos
curl https://smashpoint-7ofo.onrender.com/api/tournaments

# Obtener jugadores
curl https://smashpoint-7ofo.onrender.com/api/players
```

### Desde Navegador
Abre directamente:
```
https://smashpoint-7ofo.onrender.com/api/tournaments
https://smashpoint-7ofo.onrender.com/api/players
https://smashpoint-7ofo.onrender.com/api/results
```

Deberías ver el JSON con los datos en camelCase.

---

## 📖 Documentación Completa

He creado 2 documentos técnicos en el repositorio:

1. **`API_MOBILE.md`**: Especificación completa de todos los endpoints con ejemplos detallados
2. **`INTEGRACION_MOBILE.md`**: Resumen ejecutivo con troubleshooting

Puedes acceder aquí:
- Repo: https://github.com/Alexandre-Alvarado/Smashpoint
- Docs: Ver archivos en la raíz del proyecto

---

## 🔄 Lo Único que Necesitas

**Resumen:** Solo hacer `fetch()` a las URLs. Todo lo demás está configurado del lado del backend.

**Naming Convention:** 
- ✅ `registeredCount` (camelCase) - React Native
- ❌ `registered_count` (snake_case) - NO lo uses

**No Requieres:**
- ❌ Librerías de conversión snake_case/camelCase
- ❌ Headers de autenticación (por ahora)
- ❌ Configuración especial de fetch

---

## 🐛 Si Algo No Funciona

### Problema: "No se muestran los datos"
✅ Verificar console.log del response completo
✅ Confirmar que usas los nombres en camelCase
✅ Revisar que la URL sea https (no http)

### Problema: "matchId is not defined"
✅ Enviar `matchId` (camelCase), no `match_id`

### Problema: "Winner no coincide"
✅ El nombre debe ser exactamente como aparece en el partido

---

## 📞 Contacto

Si tienes dudas o encuentras algún problema:

**Backend:** Alexandre Alvarado
- GitHub: [@Alexandre-Alvarado](https://github.com/Alexandre-Alvarado)
- Issues: [GitHub Issues](https://github.com/Alexandre-Alvarado/Smashpoint/issues)

**Estado Actual:** 🟢 **LISTO PARA INTEGRACIÓN**

---

## ✅ Checklist para Ti

Antes de empezar a integrar, confirma:

- [ ] Puedes acceder a `https://smashpoint-7ofo.onrender.com/api/tournaments` desde el navegador
- [ ] Ves el JSON con campos en camelCase (`registeredCount`, no `registered_count`)
- [ ] Tienes configurado `fetch()` en tu proyecto React Native
- [ ] Conoces cómo hacer POST con `Content-Type: application/json`

Si todos están ✅, puedes empezar a integrar directamente.

---

**¡Listo para conectar!** 🚀

Cualquier duda, abre un issue en GitHub o contáctame directamente.

---

**Última actualización:** 11 de Diciembre 2025
