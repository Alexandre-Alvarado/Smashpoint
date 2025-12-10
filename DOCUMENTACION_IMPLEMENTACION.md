# 📘 Documentación de la Implementación – SmashPoint

Este documento describe de forma precisa y operativa los cambios implementados en SmashPoint: qué se hizo, cómo funciona, cómo operarlo y cómo mantenerlo. Su objetivo es facilitar la repetición del proceso, el soporte y la evolución futura del sistema.


## 🧭 Alcance y Objetivos

- Incorporación de RUT chileno validado para jugadores y soporte de importación masiva desde Excel.
- Rediseño del módulo de torneos con fase de grupos y fase de eliminación hasta final.
- Reglas de juego por sets: grupos al mejor de 3; final al mejor de 5.
- Cálculo automático de ganadores, estadísticas de grupos y puntos de ranking.
- Mejoras de UX en plantillas, vistas auxiliares y panel de administración.
- Documentos de apoyo: guía de entorno (`CONFIGURACION_ENTORNO.md`) y esta guía de implementación.


## 🏗️ Arquitectura Técnica (resumen)

- Framework: Django 4.2.x
- BD: MySQL/MariaDB (recomendado vía XAMPP en Windows)
- App principal: `smashpointApp`
- Modelos principales: `Jugador`, `Torneo`, `Inscripcion`, `Grupo`, `Partido`, `Ranking`, `Resultado`
- Librerías: `openpyxl` (Excel), `reportlab` (PDF), `qrcode` (QR), DRF para API v2

Estructura de carpetas relevante en este repo:

```
SMASHPOINT/
├─ manage.py
├─ CONFIGURACION_ENTORNO.md
├─ DOCUMENTACION_IMPLEMENTACION.md   ← (este documento)
├─ SMASHPOINT/urls.py
├─ smashpointApp/
│  ├─ models.py
│  ├─ views.py
│  ├─ forms.py
│  ├─ admin.py
│  └─ migrations/
└─ templates/
   ├─ jugadores/, torneos/, grupos/, bracket/, partidos/, public/
   └─ base.html, index_mejorado.html
```


## 🔑 Cambios Clave

- Jugadores
  - Nuevo campo `Jugador.rut` (único, validado por módulo 11). Licencia queda opcional para compatibilidad.
  - Importación Excel con validación de encabezados y RUT.
- Torneos
  - Nuevo campo `Torneo.numero_grupos` para activar fase de grupos.
  - Nuevo modelo `Grupo` con M2M a jugadores y cálculo de tabla (PJ, PG, PP, SA, SB).
  - `Partido` extendido con `etapa` (`GRUPOS`, `ELIMINACION`, `FINAL`), `grupo` (identificador A/B/C…), `best_of`, `detalle_sets`, `sets_a`, `sets_b` y `ganador`.
  - Reglas de sets y determinación de ganador priorizando sets sobre marcadores simples.
  - Puntos de ranking por etapa (ver sección Reglas de Negocio).
- UX/Administración
  - Vistas para generar/listar grupos, generar/avanzar bracket y visualización tipo columnas.
  - Formularios y plantillas modernizadas (ayudas/contexto para sets).
  - Admin mejorado con filtros, búsquedas y conteos.


## 🗃️ Modelo de Datos (resumen funcional)

- `Jugador`: `nombre`, `apellido`, `categoria ∈ {AMATEUR,FEDERADO}`, `rut` único (validador RUT), `licencia` opcional.
- `Torneo`: datos básicos + `numero_grupos` (0 = sin fase de grupos).
- `Inscripcion`: vínculo jugador–torneo con estado; evita duplicados.
- `Grupo`: `torneo`, `nombre` (A,B,C,…), `jugadores` (M2M). Método `estadisticas()` calcula tabla a partir de `Partido`.
- `Partido`:
  - `etapa ∈ {GRUPOS, ELIMINACION, FINAL}`
  - `grupo` (texto, ej: "A") para partidos de fase de grupos
  - `best_of` (3 o 5), `detalle_sets` (ej: `11-7,8-11,11-9`)
  - `sets_a`, `sets_b` (derivados), `ganador`
  - Métodos `parsear_detalle_sets()` y `calcular_ganador()` encapsulan la lógica.
- `Ranking`: puntos acumulados por jugador.

Código fuente: `smashpointApp/models.py`.


## ⚙️ Reglas de Negocio

- Asignación a Grupos
  - Se crean `numero_grupos` y se distribuyen inscritos de forma balanceada (round-robin por índice).
  - Partidos de grupos: combinaciones únicas de todos contra todos, `best_of = 3`.
- Validación de Sets (`Partido.parsear_detalle_sets`)
  - Formato: `PuntosA-PuntosB` separados por comas, ej: `11-7,8-11,11-9`.
  - Reglas por set válido: diferencia mínima de 2 puntos; normalmente el ganador alcanza ≥ 11 (se permite flexibilidad si ninguno llega a 11, no se computa el set si empatan o no cumple regla de diferencia).
  - Se calcula `sets_a`/`sets_b` y, si alguien alcanza mayoría (objetivo = `(best_of // 2) + 1`), se fija `ganador`.
- Mejores de N
  - Grupos y eliminación: mejor de 3 (`best_of=3`).
  - Final: mejor de 5 (`best_of=5`).
- Tabla de Grupos
  - Orden: más partidos ganados (`PG`), luego diferencia de sets (`SA - SB`).
- Puntos de Ranking (`Partido.calcular_ganador`)
  - Fase de grupos: ganador +2, perdedor +1.
  - Eliminación: ganador +`3 + ronda`; perdedor +1.
  - Final: ganador +`3 + ronda + 5` (bono adicional de final); perdedor +1.


## 🧩 Vistas y URLs

Archivo: `SMASHPOINT/urls.py` (vistas en `smashpointApp/views.py`).

- Jugadores
  - `GET /jugadores/` listar; `POST /jugadores/agregar/`; `GET/POST /jugadores/editar/<id>/`
  - `POST /jugadores/importar/excel/` importar Excel (vista protegida por permiso)
- Torneos
  - `GET /torneos/` listar; CRUD básico.
  - Fase Grupos: `GET /torneos/<id>/grupos/generar/`, `GET /torneos/<id>/grupos/`
  - Bracket: `GET /torneos/<id>/bracket/generar/`, `GET /torneos/<id>/bracket/`, `GET /torneos/<id>/bracket/ronda/siguiente/`, `GET /torneos/<id>/bracket/visual/`
- Partidos
  - `GET /torneos/<id>/partidos/` listar; `GET/POST /partidos/editar/<id>/` editar.
- Público
  - `GET /public/scoreboard/` scoreboard; `GET /public/jugador/<id>/` ficha; `GET /public/jugador/<id>/qr/` QR.
- Exportación/Importación
  - CSV jugadores/torneos/resultados; PDF/Excel de ranking.
- API JSON simple
  - `GET /api/jugadores/`, `GET /api/torneos/`, `GET /api/ranking/`
- API v2 (DRF): `GET /api/v2/…` (ViewSets registrados).


## 🧾 Formularios Clave

- `FormJugador`: incluye `rut` obligatorio y placeholder de formato.
- `FormTorneo`: expone `numero_grupos` con ayuda contextual.
- `FormPartido`: expone `best_of`, `detalle_sets`, `sets_a`, `sets_b`; ayuda de formato.
- `BulkJugadorImportForm`: archivo Excel con encabezados `nombre`, `apellido`, `categoria`, `rut`.

Código fuente: `smashpointApp/forms.py`.


## 🖥️ Plantillas y UX

- Grupos: `templates/grupos/lista.html` muestra tabla por grupo y enlaces para generar/ver bracket.
- Bracket:
  - Lista: `templates/bracket/lista.html` (ronda, etapa, sets y ganador).
  - Visual: `templates/bracket/visual.html` (columnas por ronda, best_of y marcador).
- Partidos:
  - Editar: `templates/partidos/editar.html` con ayudas sobre `best_of` y formato de sets.
- Scoreboard público: `templates/public/scoreboard.html` (últimos resultados y ranking con QR).


## 🔐 Administración (Django Admin)

- Búsqueda por `rut` en jugadores, filtros por categoría.
- `Grupo` con `filter_horizontal` para jugadores y conteo en listado.
- `Partido` expone `etapa`, `grupo`, `best_of`, `sets_a/b` y filtros por torneo/ronda/etapa/grupo.

Código fuente: `smashpointApp/admin.py`.


## 📥 Importación de Jugadores (Excel)

Vista: `importar_jugadores_excel` (`/jugadores/importar/excel/`).

- Requisitos de encabezado: `nombre`, `apellido`, `categoria`, `rut`.
- Validaciones:
  - `rut` único y válido (validador en modelo). Duplicados se omiten con reporte.
  - `categoria` se normaliza a `AMATEUR` o `FEDERADO` (por defecto: `AMATEUR`).
  - Filas incompletas se reportan y omiten.
- Resultado: mensaje de éxito con conteo y reporte de incidencias por fila.

Código fuente: `views.importar_jugadores_excel` y plantilla `templates/jugadores/importar.html`.


## 🧪 Pruebas y Verificación

- Migraciones
  - Ejecutar: `python manage.py migrate`
- Pruebas unitarias (ejemplo ya usado):
  ```powershell
  python manage.py test smashpointApp.tests.TestAPIV2Write.test_crear_jugador_denegado_usuario_sin_permiso -v 2
  ```
- Comprobación rápida de flujo de torneo (shell): ver la sección siguiente.


## ▶️ Flujo Operativo Paso a Paso (ejemplo)

1) Crear torneo con grupos y registrar jugadores (desde UI o shell).
2) Generar grupos: combates round-robin `best_of=3` por grupo.
3) Editar partidos de grupos ingresando `detalle_sets` (ej: `11-7,8-11,11-9`).
4) Generar bracket de eliminación cuando todos los partidos de grupos tienen ganador.
5) Resolver rondas de eliminación (best-of-3) y avanzar con "Ronda siguiente".
6) Final (best-of-5): ingresar `detalle_sets` hasta que un jugador alcance 3 sets.
7) El sistema actualiza ranking automáticamente según reglas.

Ejemplo reproducible en PowerShell (usando superusuario existente):

```powershell
python manage.py shell -c "
from django.contrib.auth import get_user_model
User=get_user_model()
admin=User.objects.filter(is_superuser=True).first()
from smashpointApp.models import Torneo,Inscripcion,Jugador,Grupo,Partido
from smashpointApp.views import generar_grupos,generar_bracket,generar_eliminacion_siguiente
from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
rf=RequestFactory(); req=rf.get('/'); req.user=admin; setattr(req,'session',{}); setattr(req,'_messages',FallbackStorage(req))
# Crear torneo de prueba
jugs=list(Jugador.objects.all()[:6])
t=Torneo.objects.create(nombre='DocPipeline', direccion='Dir', fecha='2025-12-25', categoria='ADULTO', cupos_max=32, numero_grupos=2)
for j in jugs: Inscripcion.objects.create(torneo=t, jugador=j, estado='INSCRITO')
# Generar grupos
_ = generar_grupos(req, t.id)
print('Grupos:', Grupo.objects.filter(torneo=t).count(), 'Partidos grupos:', Partido.objects.filter(torneo=t, etapa='GRUPOS').count())
# Resolver fase de grupos (best-of-3)
for p in Partido.objects.filter(torneo=t, etapa='GRUPOS'):
    p.detalle_sets='11-7,11-9'; p.best_of=3; p.parsear_detalle_sets()
print('Ganadores en grupos:', Partido.objects.filter(torneo=t, etapa='GRUPOS', ganador__isnull=False).count())
# Generar bracket
_ = generar_bracket(req, t.id)
print('Partidos eliminación R1:', Partido.objects.filter(torneo=t, etapa='ELIMINACION', ronda=1).count())
# Resolver R1 eliminación
for p in Partido.objects.filter(torneo=t, etapa='ELIMINACION', ronda=1):
    p.detalle_sets='11-4,11-9'; p.best_of=3; p.parsear_detalle_sets()
_ = generar_eliminacion_siguiente(req, t.id)
print('Partidos R2:', Partido.objects.filter(torneo=t, ronda=2, etapa__in=['ELIMINACION','FINAL']).count())
# Resolver R2 y crear final
for p in Partido.objects.filter(torneo=t, ronda=2):
    p.detalle_sets='11-6,11-9'; p.best_of=(5 if p.etapa=='FINAL' else 3); p.parsear_detalle_sets()
_ = generar_eliminacion_siguiente(req, t.id)
print('Final creada:', Partido.objects.filter(torneo=t, etapa='FINAL').count())
# Resolver final (best-of-5: se requieren 3 sets ganados)
for p in Partido.objects.filter(torneo=t, etapa='FINAL'):
    p.detalle_sets='11-9,8-11,11-5,11-8'; p.best_of=5; p.parsear_detalle_sets()
print('Final resuelta:', Partido.objects.filter(torneo=t, etapa='FINAL', ganador__isnull=False).count())
"
```

Notas:
- Los sets solo cuentan si cumplen formato y regla de diferencia ≥ 2.
- En final, asegúrese de ingresar suficientes sets para alcanzar 3 ganados.


## 🧷 Mantenimiento y Extensión

- Desempates de grupos: hoy se ordena por `PG` y diferencia de sets. Se puede extender a head-to-head y/o ratio de puntos si se modela puntaje por set.
- Visual del bracket: actual es por columnas; se puede mejorar con líneas (SVG) y estados.
- Automatización: se pueden agregar acciones en Admin para avanzar rondas y cierre automático.
- Validaciones: endurecer reglas de `detalle_sets` o agregar feedback más detallado en la UI.


## 🆘 Solución de Problemas

- “No puedo generar bracket”: verifique que todos los partidos de grupos tienen `ganador`.
- “Final no se resuelve”: para best-of-5 un jugador debe alcanzar 3 sets válidos; revise el `detalle_sets`.
- “Importación Excel falla”: confirme encabezados `nombre`, `apellido`, `categoria`, `rut` y que los RUT sean válidos/únicos.
- “Ranking no cambia”: el ranking se actualiza cuando `ganador` queda definido; reabra y guarde el partido o valide `detalle_sets`.


## 📚 Referencias

- Entorno de trabajo y despliegue: `CONFIGURACION_ENTORNO.md`.
- Código fuente principal: `smashpointApp/models.py`, `views.py`, `forms.py`, `admin.py`.
- Rutas: `SMASHPOINT/urls.py`.
- Plantillas: `templates/` (subcarpetas por módulo).


---


 
## 🧩 Relaciones y Modelo Lógico (ERD textual)

- Torneo 1—N Inscripción N—1 Jugador
- Torneo 1—N Grupo; Grupo N—M Jugador
- Torneo 1—N Partido; Partido 1—1 (A/B) Jugador; Partido 1—0..1 Ganador
- Jugador 1—1 Ranking
- Resultado (histórico simple): Torneo 1—N Resultado; Jugador (j1/j2) N—N Resultado

Campos y claves relevantes:
- `Jugador.rut` único, validado; `Inscripcion` con `unique_together (torneo,jugador)`;
- `Grupo` con `unique_together (torneo,nombre)`; `Partido` referencia `torneo`, `jugador_a/b`, `ganador`.

## 🔒 Permisos y Roles

- Gestión de jugadores: `add/change/delete_jugador`
- Gestión de torneos: `add/change/delete_torneo`
- Gestión de resultados/partidos: `add/change/delete_resultado`, `add/change_partido`
- Acciones clave protegidas:
  - Importar Excel: requiere `add_jugador`
  - Generar grupos/bracket y avanzar rondas: requiere `add_partido`
  - Editar partidos (ingresar sets/marcadores): requiere `change_partido`

Sug. de roles:
- Administrador: todos los permisos de `smashpointApp.*`
- Operador de torneo: `add/change_partido`, `add_partido` y acceso a listas
- Consultas: sin permisos de escritura (solo vistas públicas y listados internos)

## 🌐 API y Endpoints

- API JSON simple (sin DRF):
  - `GET /api/jugadores/` → listado con `id,nombre,apellido,categoria,rut`
  - `GET /api/torneos/` → `id,nombre,fecha,categoria,estado,cupos_max`
  - `GET /api/ranking/` → `jugador__nombre, jugador__apellido, puntos`

- API v2 (DRF, router):
  - `GET/POST /api/v2/jugadores/`
  - `GET/POST /api/v2/torneos/`
  - `GET/POST /api/v2/resultados/`
  - `GET/POST /api/v2/ranking/`
  - `GET/POST /api/v2/partidos/`
  - `GET/POST /api/v2/inscripciones/`

Notas:
- Autenticación/permiso según configuración DRF por defecto; ajustar en `settings.py` si se requiere Token/Auth.
- Ejemplo rápido:
  ```powershell
  curl http://localhost:8000/api/jugadores/
  curl http://localhost:8000/api/ranking/
  ```

## 🧭 Runbook Operativo

- Crear torneo → Inscribir jugadores → Generar grupos → Registrar resultados de grupos → Generar bracket → Avanzar rondas → Final → Torneo `FINALIZADO`.
- Reglas: Grupos/Eliminación best-of-3; Final best-of-5. Ingresar `detalle_sets` para cálculo automático del ganador.
- Cierres: `generar_eliminacion_siguiente` cierra automáticamente si hay un solo ganador en ronda actual.

## 💾 Backup y Restore (MySQL)

Backup (dump):
```powershell
mysqldump -u smashpoint_user -p smashpoint > backup_smashpoint.sql
```

Restore:
```powershell
mysql -u smashpoint_user -p smashpoint < backup_smashpoint.sql
```

## 🧪 Datos de Ejemplo (CSV)

Archivo de muestra: `samples/jugadores_ejemplo.csv`

```
nombre,apellido,categoria,rut
Juan,Pérez,FEDERADO,11111111-1
María,González,AMATEUR,22222222-2
Pedro,Soto,AMATEUR,33333333-3
Ana,Rojas,FEDERADO,44444444-4
```

Importar desde UI: `Jugadores → Importar desde Excel` (puedes abrir el CSV en Excel y guardar como .xlsx)

## ⚠️ Limitaciones y Decisiones (ADRs breves)

- Desempate de grupos: por ahora `PG` y diferencia de sets; pendiente head-to-head/ratio de puntos.
- Visual de bracket: disposición por columnas sin líneas de conexión; se puede ampliar con SVG.
- `Resultado` convive con `Partido`: `Resultado` es histórico simple, `Partido` es la entidad reglamentaria con sets.

## ✅ Checklist de QA/Release

- [ ] Migraciones aplicadas: `python manage.py migrate`
- [ ] Importación de muestra OK
- [ ] Generación de grupos y cálculo de tabla OK
- [ ] Bracket generado y avance de rondas OK
- [ ] Final resuelta con best-of-5
- [ ] Ranking actualizado tras cada ganador
- [ ] Scoreboard público accesible y QR funcionando

## 🧪 Cobertura y Pruebas (sugerencias)

- Probar RUTs válidos/ inválidos (módulo 11) en `FormJugador`.
- Probar `parsear_detalle_sets` con casos: diferencia <2, sets insuficientes, best-of-3/5.
- Pruebas de flujo: generación grupos → bracket → final.
- Medir cobertura (si instalado `coverage`):
  ```powershell
  coverage run manage.py test
  coverage html
  ```

