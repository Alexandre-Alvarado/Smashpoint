# SmashPoint - Sistema de Gestión de Torneos de Bádminton

![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema web integral para la administración de torneos de bádminton, desarrollado con Django. Permite gestionar jugadores, inscripciones, partidos, generación automática de brackets eliminatorios, fase de grupos, y ranking en tiempo real.

**🌐 Deployment en producción:** [https://smashpoint-7ofo.onrender.com](https://smashpoint-7ofo.onrender.com)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Tecnologías](#-tecnologías)
- [Requisitos](#-requisitos)
- [Instalación Local](#-instalación-local)
- [Configuración de Base de Datos](#-configuración-de-base-de-datos)
- [Deployment en Render](#-deployment-en-render)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso y Funcionalidades](#-uso-y-funcionalidades)
- [API REST](#-api-rest)
- [Variables de Entorno](#-variables-de-entorno)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🚀 Características

### Gestión de Jugadores
- **Registro con validación de RUT chileno** (algoritmo Módulo 11)
- Categorías: Amateur y Federado
- Campo de origen (ciudad/región)
- Importación masiva desde Excel
- Generación automática de QR para credenciales

### Gestión de Torneos
- **7 categorías**: Peneca, Preinfantil, Infantil, Juvenil, Todo Competidor, Paralímpico, Máster
- Control de cupos máximos
- Estados: Abierto, En Curso, Finalizado
- **Fase de grupos** configurable (distribución automática de jugadores)
- **Brackets eliminatorios** de potencia de 2 (8, 16, 32, 64 jugadores)
- Visualización horizontal de brackets estilo torneo

### Sistema de Partidos
- Registro de resultados con validación de sets (mejor de 3)
- Edición masiva de partidos pendientes
- Generación automática de rondas
- Control de bye (descanso automático en brackets impares)

### Ranking y Estadísticas
- Cálculo automático de puntos según resultados
- Ranking público sin autenticación
- Filtros por categoría de torneo
- Estadísticas de victorias/derrotas

### Características Técnicas
- **Auto-creación de superusuario** en primer despliegue (sin consola)
- **WhiteNoise** para servir archivos estáticos en producción
- **Django REST Framework** con API completa
- Middleware personalizado para restricción de acceso
- PWA ready (manifest.json + service-worker)

---

## 🛠 Tecnologías

### Backend
- **Django 4.2.7** - Framework web principal
- **Django REST Framework 3.14.0** - API REST
- **Gunicorn 23.0.0** - Servidor WSGI para producción
- **WhiteNoise 6.11.0** - Gestión de archivos estáticos

### Frontend
- **Bootstrap 5.3.8** - Framework CSS
- **JavaScript Vanilla** - Interactividad
- HTML5 + CSS3

### Base de Datos
- **SQLite** (desarrollo y producción actual en Render)
- **PostgreSQL** (recomendado para producción futura)
- **MySQL** (soportado, configuración legacy)

### Herramientas
- **openpyxl 3.1.2** - Importación de Excel
- **qrcode 7.4.2** - Generación de códigos QR
- **reportlab 4.0.9** - Generación de PDFs
- **pytest** + **coverage** - Testing

---

## 📦 Requisitos

- **Python 3.10+**
- **pip** (gestor de paquetes)
- **Virtual environment** (recomendado: venv)
- **Git** (para clonación y deploy)

---

## 💻 Instalación Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/Alexandre-Alvarado/Smashpoint.git
cd Smashpoint
```

### 2. Crear y activar entorno virtual
**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional en local)
```bash
python manage.py createsuperuser
```
*Nota: En producción (Render) se crea automáticamente con credenciales por defecto.*

### 6. Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

Accede a: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🗄 Configuración de Base de Datos

### SQLite (Actual en Producción)
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL (Recomendado para Producción)

#### 1. Instalar psycopg2
```bash
pip install psycopg2-binary dj-database-url
```

#### 2. Actualizar settings.py
```python
import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

#### 3. Variables de entorno en Render
```bash
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

#### 4. Migraciones
```bash
python manage.py migrate
```

#### 5. Actualizar requirements.txt
```bash
pip freeze > requirements.txt
```

### MySQL (Legacy)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'BD_smashpoint',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

---

## 🌐 Deployment en Render

### 1. Preparar el proyecto

**Archivo `requirements.txt`** (ya incluido):
```txt
Django==4.2.7
gunicorn==23.0.0
whitenoise==6.11.0
djangorestframework==3.14.0
psycopg2-binary==2.9.9  # Para PostgreSQL
dj-database-url==2.1.0  # Para DATABASE_URL
# ... resto de dependencias
```

**Archivo `runtime.txt`** (opcional):
```txt
python-3.11.0
```

### 2. Configurar Render

#### Build Command:
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

#### Start Command:
```bash
gunicorn SMASHPOINT.wsgi:application
```

### 3. Variables de Entorno en Render

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Versión de Python |
| `ADMIN_USER` | `admin` | Usuario admin por defecto |
| `ADMIN_PASSWORD` | `Admin123!` | Contraseña admin (cambiar) |
| `ADMIN_EMAIL` | `admin@example.com` | Email admin |
| `SECRET_KEY` | `tu_secret_key_aqui` | Clave secreta Django |
| `DEBUG` | `False` | Modo debug (producción) |
| `DATABASE_URL` | `postgresql://...` | URL PostgreSQL (futuro) |

### 4. Configurar ALLOWED_HOSTS

En `settings.py`:
```python
ALLOWED_HOSTS = [
    'smashpoint-7ofo.onrender.com',
    'localhost',
    '127.0.0.1',
]
```

### 5. Deploy automático
- Conecta tu repo de GitHub a Render
- Cada `git push` a `master` despliega automáticamente
- Render ejecuta `Build Command` → `Start Command`

---

## 📁 Estructura del Proyecto

```
SMASHPOINT/
├── manage.py                      # CLI de Django
├── requirements.txt               # Dependencias Python
├── README.md                      # Documentación
├── db.sqlite3                     # Base de datos (gitignored)
│
├── SMASHPOINT/                    # Configuración principal
│   ├── settings.py                # Configuración Django
│   ├── urls.py                    # URLs principales
│   ├── wsgi.py                    # Entry point WSGI
│   └── asgi.py                    # Entry point ASGI
│
├── smashpointApp/                 # Aplicación principal
│   ├── models.py                  # Modelos (Jugador, Torneo, Partido, etc.)
│   ├── views.py                   # Vistas y lógica de negocio
│   ├── forms.py                   # Formularios Django
│   ├── admin.py                   # Configuración del admin
│   ├── apps.py                    # Configuración de la app (auto-superuser)
│   ├── middleware.py              # Middleware personalizado
│   ├── api.py                     # ViewSets de DRF
│   └── migrations/                # Migraciones de BD
│
├── templates/                     # Plantillas HTML
│   ├── index.html                 # Dashboard principal
│   ├── login.html                 # Página de login
│   ├── contacto.html              # Formulario de contacto
│   ├── jugadores/                 # Templates de jugadores
│   │   ├── lista.html
│   │   ├── agregar.html
│   │   └── editar.html
│   ├── torneos/                   # Templates de torneos
│   │   ├── lista.html
│   │   ├── agregar.html
│   │   ├── editar.html
│   │   └── detalle_bracket.html
│   └── resultados/                # Templates de partidos
│       ├── lista.html
│       └── editar_partido.html
│
├── static/                        # Archivos estáticos
│   ├── css/
│   │   └── styles.css             # Estilos personalizados
│   ├── icons/                     # Iconos PWA
│   ├── manifest.json              # Manifest PWA
│   └── service-worker.js          # Service Worker
│
└── staticfiles/                   # Archivos estáticos recolectados (gitignored)
```

---

## 🎯 Uso y Funcionalidades

### Panel de Administración

Accede a `/admin/` con credenciales:
- **Usuario:** `admin` (configurable con `ADMIN_USER`)
- **Contraseña:** `Admin123!` (configurable con `ADMIN_PASSWORD`)

**Recomendación:** Cambiar contraseña inmediatamente después del primer login.

### Flujo de Trabajo

#### 1. Crear Jugadores
- Navega a **Jugadores → Agregar**
- Llena el formulario con RUT válido
- O importa desde Excel con formato:
  ```
  | Nombre | Apellido | Categoría | RUT | Origen |
  ```

#### 2. Crear Torneo
- **Torneos → Agregar**
- Define:
  - Nombre, fecha, dirección
  - Categoría (Peneca, Infantil, etc.)
  - Cupos máximos
  - Número de grupos (0 = sin fase de grupos)

#### 3. Inscribir Jugadores
- En el detalle del torneo, inscribe jugadores uno por uno
- O usa inscripción masiva desde Excel

#### 4. Generar Grupos (Opcional)
- Si configuraste `numero_grupos > 0`
- Click en **"Generar Grupos"**
- Los jugadores se distribuyen automáticamente

#### 5. Generar Bracket Eliminatorio
- Click en **"Generar Bracket"**
- Se crea un bracket de potencia de 2 (8, 16, 32, 64)
- Si sobran cupos, se asignan "bye" (pasan directo a siguiente ronda)

#### 6. Registrar Resultados
- **Partidos → Lista**
- Edita cada partido con sets ganados
- Validación automática: mejor de 3 sets
- Genera automáticamente siguiente ronda al completar todos los partidos

#### 7. Ver Ranking
- `/ranking/` (público, sin login)
- Ordenado por puntos acumulados
- Filtros por categoría de torneo

---

## 🔌 API REST

Base URL en producción: `https://smashpoint-7ofo.onrender.com/api/`

### Endpoints Disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/jugadores/` | GET, POST | Listar y crear jugadores |
| `/api/jugadores/{id}/` | GET, PUT, DELETE | Detalle, actualizar, eliminar jugador |
| `/api/torneos/` | GET, POST | Listar y crear torneos |
| `/api/torneos/{id}/` | GET, PUT, DELETE | Detalle, actualizar, eliminar torneo |
| `/api/partidos/` | GET, POST | Listar y crear partidos |
| `/api/partidos/{id}/` | GET, PUT, DELETE | Detalle, actualizar, eliminar partido |
| `/api/inscripciones/` | GET, POST | Listar y crear inscripciones |
| `/api/ranking/` | GET | Obtener ranking completo |

### Ejemplo de Uso

#### Obtener todos los jugadores
```bash
curl https://smashpoint-7ofo.onrender.com/api/jugadores/
```

#### Crear un jugador
```bash
curl -X POST https://smashpoint-7ofo.onrender.com/api/jugadores/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "categoria": "AMATEUR",
    "rut": "12345678-5",
    "origen": "Santiago"
  }'
```

#### Obtener ranking
```bash
curl https://smashpoint-7ofo.onrender.com/api/ranking/
```

**Nota:** La API tiene permisos `AllowAny` actualmente. Para producción, considera agregar autenticación con JWT.

---

## 🔐 Variables de Entorno

### Producción (Render)

| Variable | Valor por Defecto | Descripción |
|----------|-------------------|-------------|
| `DEBUG` | `True` | **Cambiar a `False` en producción** |
| `SECRET_KEY` | (insecure) | Generar con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `ADMIN_USER` | `admin` | Usuario administrador por defecto |
| `ADMIN_PASSWORD` | `Admin123!` | Contraseña administrador (cambiar) |
| `ADMIN_EMAIL` | `admin@example.com` | Email del administrador |
| `DATABASE_URL` | (SQLite) | URL de PostgreSQL en formato `postgresql://user:pass@host:port/db` |
| `ALLOWED_HOSTS` | (configurado) | Agregar más dominios si es necesario |

### Configuración de PostgreSQL (Futuro)

```bash
# Instalar driver
pip install psycopg2-binary dj-database-url

# Actualizar requirements.txt
pip freeze > requirements.txt

# Variable en Render
DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_bd

# settings.py
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

---

## 🧪 Testing

### Ejecutar tests
```bash
# Todos los tests
pytest

# Con coverage
pytest --cov=smashpointApp

# Test específico
pytest smashpointApp/tests/test_models.py
```

### Estructura de tests (recomendada)
```
smashpointApp/
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_api.py
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guía de estilo
- **PEP 8** para Python
- Comentarios en español
- Nombres de variables/funciones descriptivos
- Tests para nuevas funcionalidades

---

## 📝 Notas de Versión

### v1.0.0 - Despliegue Inicial en Render (Diciembre 2025)
- ✅ Gestión completa de jugadores, torneos y partidos
- ✅ Validación de RUT chileno
- ✅ Fase de grupos y brackets eliminatorios
- ✅ Ranking público
- ✅ API REST con DRF
- ✅ Auto-creación de superusuario en deploy
- ✅ WhiteNoise para archivos estáticos
- ✅ PWA ready (manifest + service worker)

### Próximas mejoras planificadas
- [ ] Migración a PostgreSQL
- [ ] Autenticación JWT para API
- [ ] Notificaciones por email
- [ ] Panel de estadísticas avanzadas
- [ ] Exportación de resultados a PDF
- [ ] Sistema de mensajería interna

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👤 Autor

**Alexandre Alvarado**
- GitHub: [@Alexandre-Alvarado](https://github.com/Alexandre-Alvarado)
- Proyecto: [SmashPoint](https://github.com/Alexandre-Alvarado/Smashpoint)

---

## 🙏 Agradecimientos

- Django Software Foundation
- Bootstrap Team
- Render Platform
- Comunidad de bádminton de Chile

---

## 📞 Soporte

Para reportar bugs o solicitar features, abre un [issue en GitHub](https://github.com/Alexandre-Alvarado/Smashpoint/issues).

**Deployment URL:** [https://smashpoint-7ofo.onrender.com](https://smashpoint-7ofo.onrender.com)

---

**Última actualización:** Diciembre 2025
