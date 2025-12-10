# 📋 Configuración del Entorno de Trabajo - SmashPoint

## 3.1.4.7. Configuración del entorno de trabajo

Esta guía proporciona instrucciones paso a paso para configurar completamente el entorno de desarrollo del sistema SmashPoint, desde la instalación de dependencias hasta la ejecución del proyecto.

---

## 📑 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación de Python](#instalación-de-python)
3. [Configuración de Base de Datos MySQL](#configuración-de-base-de-datos-mysql)
4. [Configuración del Proyecto Django](#configuración-del-proyecto-django)
5. [Instalación de Dependencias](#instalación-de-dependencias)
6. [Configuración de la Base de Datos](#configuración-de-la-base-de-datos)
7. [Migraciones y Datos Iniciales](#migraciones-y-datos-iniciales)
8. [Ejecución del Servidor de Desarrollo](#ejecución-del-servidor-de-desarrollo)
9. [Verificación de la Instalación](#verificación-de-la-instalación)
10. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

---

## 1. Requisitos Previos

### Software Necesario

- **Python**: Versión 3.8 o superior
- **MySQL/MariaDB**: Servidor de base de datos
- **Git**: Control de versiones (opcional pero recomendado)
- **Editor de código**: VS Code, PyCharm, o similar

### Conocimientos Recomendados

- Conceptos básicos de Python
- Fundamentos de Django
- Línea de comandos (CMD/PowerShell en Windows, Terminal en Linux/Mac)
- Consultas SQL básicas

---

## 2. Instalación de Python

### Windows

1. **Descargar Python**
   - Visitar [python.org/downloads](https://www.python.org/downloads/)
   - Descargar la última versión estable (recomendado: 3.11 o 3.12)

2. **Ejecutar el Instalador**
   ```
   ✅ Marcar "Add Python to PATH"
   ✅ Seleccionar "Install Now"
   ```

3. **Verificar la Instalación**
   ```powershell
   python --version
   # Salida esperada: Python 3.x.x
   
   pip --version
   # Salida esperada: pip x.x.x
   ```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

### macOS

```bash
# Usando Homebrew
brew install python3
python3 --version
```

---

## 3. Configuración de Base de Datos MySQL

### Opción A: XAMPP (Recomendado para Windows)

1. **Descargar XAMPP**
   - Visitar [apachefriends.org](https://www.apachefriends.org/)
   - Descargar versión para Windows
   - Ejecutar instalador

2. **Iniciar Servicios XAMPP**
   - Abrir XAMPP Control Panel
   - Hacer clic en "Start" para **Apache** y **MySQL**
   
   ![XAMPP Control Panel](https://via.placeholder.com/600x200?text=XAMPP+Control+Panel)

3. **Acceder a phpMyAdmin**
   - Abrir navegador
   - Ir a: `http://localhost/phpmyadmin`

4. **Crear Base de Datos**
   ```sql
   -- En phpMyAdmin, pestaña SQL:
   CREATE DATABASE smashpoint CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

5. **Crear Usuario (Opcional pero recomendado)**
   ```sql
   CREATE USER 'smashpoint_user'@'localhost' IDENTIFIED BY 'tu_contraseña_segura';
   GRANT ALL PRIVILEGES ON smashpoint.* TO 'smashpoint_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Opción B: MySQL Standalone

1. **Descargar MySQL**
   - Visitar [dev.mysql.com/downloads](https://dev.mysql.com/downloads/installer/)
   - Descargar MySQL Installer

2. **Instalar MySQL Server**
   - Ejecutar instalador
   - Seleccionar "Developer Default"
   - Configurar contraseña de root

3. **Crear Base de Datos**
   ```powershell
   # Abrir MySQL Command Line Client
   mysql -u root -p
   ```
   
   ```sql
   CREATE DATABASE smashpoint CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'smashpoint_user'@'localhost' IDENTIFIED BY 'tu_contraseña';
   GRANT ALL PRIVILEGES ON smashpoint.* TO 'smashpoint_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

### Verificar Conexión MySQL

```powershell
mysql -u smashpoint_user -p
# Ingresar contraseña
# Debe mostrar: mysql>
```

---

## 4. Configuración del Proyecto Django

### Clonar o Descargar el Proyecto

**Opción A: Con Git**
```powershell
cd C:\Users\TuUsuario\Documentos
git clone https://github.com/tu-repositorio/smashpoint.git
cd smashpoint
```

**Opción B: Descarga Manual**
1. Descargar ZIP del proyecto
2. Extraer en ubicación deseada
3. Abrir CMD/PowerShell en la carpeta del proyecto

### Estructura del Proyecto

```
SMASHPOINT/
├── manage.py                  # Script principal de Django
├── requirements.txt           # Dependencias Python
├── CONFIGURACION_ENTORNO.md   # Esta guía
├── README_TESTING.md          # Guía de pruebas
├── SMASHPOINT/                # Configuración del proyecto
│   ├── settings.py            # Configuración Django
│   ├── urls.py                # Rutas principales
│   └── wsgi.py                # Servidor WSGI
├── smashpointApp/             # Aplicación principal
│   ├── models.py              # Modelos de datos
│   ├── views.py               # Vistas/Controladores
│   ├── forms.py               # Formularios
│   ├── admin.py               # Panel de administración
│   └── migrations/            # Migraciones de BD
├── templates/                 # Plantillas HTML
│   ├── base.html              # Plantilla base
│   ├── index.html             # Página principal
│   ├── jugadores/             # Templates jugadores
│   ├── torneos/               # Templates torneos
│   ├── grupos/                # Templates grupos
│   └── bracket/               # Templates bracket
└── static/                    # Archivos estáticos
    ├── css/
    │   └── styles.css         # Estilos personalizados
    ├── icons/                 # Íconos PWA
    ├── manifest.json          # Manifest PWA
    └── service-worker.js      # Service Worker
```

---

## 5. Instalación de Dependencias

### Crear Entorno Virtual (Recomendado)

**Windows:**
```powershell
cd C:\Users\alexa\Downloads\SmashPoint (1)\SMASHPOINT

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate

# El prompt debe cambiar a: (venv) PS C:\...\SMASHPOINT>
```

**Linux/macOS:**
```bash
cd /ruta/a/SMASHPOINT

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# El prompt debe cambiar a: (venv) usuario@host:~/SMASHPOINT$
```

### Instalar Dependencias del Proyecto

```powershell
# Con el entorno virtual activado:
pip install --upgrade pip

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Dependencias Principales

El archivo `requirements.txt` incluye:

```txt
Django==4.2.7              # Framework web
mysqlclient==2.2.0         # Conector MySQL
djangorestframework==3.14.0 # API REST
reportlab==4.0.7           # Generación PDF
openpyxl==3.1.2            # Manejo Excel
qrcode==7.4.2              # Generación QR
Pillow==10.1.0             # Procesamiento imágenes
coverage==7.3.2            # Cobertura de pruebas
```

### Verificar Instalación de Dependencias

```powershell
pip list
# Debe mostrar todas las dependencias instaladas

django-admin --version
# Debe mostrar: 4.2.7 (o superior)
```

---

## 6. Configuración de la Base de Datos

### Editar archivo `settings.py`

Ubicación: `SMASHPOINT/settings.py`

**Buscar sección DATABASES:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smashpoint',              # Nombre de tu base de datos
        'USER': 'smashpoint_user',         # Usuario MySQL
        'PASSWORD': 'tu_contraseña',       # Contraseña MySQL
        'HOST': 'localhost',               # Host (localhost para local)
        'PORT': '3306',                    # Puerto MySQL (3306 por defecto)
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### Configuraciones Importantes

**Zona Horaria:**
```python
TIME_ZONE = 'America/Santiago'  # Ajustar según ubicación
USE_TZ = True
```

**Idioma:**
```python
LANGUAGE_CODE = 'es-cl'
```

**Archivos Estáticos:**
```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

**Seguridad (Desarrollo):**
```python
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

> ⚠️ **Importante**: En producción cambiar `DEBUG = False` y configurar `ALLOWED_HOSTS` con dominios reales.

---

## 7. Migraciones y Datos Iniciales

### Verificar Conexión a Base de Datos

```powershell
python manage.py dbshell
# Si conecta exitosamente, mostrará: mysql>
# Salir con: EXIT;
```

### Crear Migraciones

```powershell
# Crear archivos de migración para cambios en modelos
python manage.py makemigrations

# Salida esperada:
# Migrations for 'smashpointApp':
#   smashpointApp\migrations\0001_initial.py
#     - Create model Jugador
#     - Create model Torneo
#     - ...
```

### Aplicar Migraciones

```powershell
python manage.py migrate

# Salida esperada:
# Operations to perform:
#   Apply all migrations: admin, auth, contenttypes, sessions, smashpointApp
# Running migrations:
#   Applying contenttypes.0001_initial... OK
#   Applying auth.0001_initial... OK
#   ...
#   Applying smashpointApp.0001_initial... OK
```

### Crear Superusuario

```powershell
python manage.py createsuperuser

# Ingrese información solicitada:
# Username: admin
# Email: admin@smashpoint.cl
# Password: ******** (mínimo 8 caracteres)
# Password (again): ********
# Superuser created successfully.
```

### Cargar Datos de Prueba (Opcional)

**Crear Fixture de Jugadores:**

Crear archivo `smashpointApp/fixtures/jugadores_inicial.json`:

```json
[
  {
    "model": "smashpointApp.jugador",
    "pk": 1,
    "fields": {
      "nombre": "Juan",
      "apellido": "Pérez",
      "categoria": "FEDERADO",
      "rut": "12345678-5"
    }
  },
  {
    "model": "smashpointApp.jugador",
    "pk": 2,
    "fields": {
      "nombre": "María",
      "apellido": "González",
      "categoria": "AMATEUR",
      "rut": "23456789-6"
    }
  }
]
```

**Cargar Fixture:**
```powershell
python manage.py loaddata jugadores_inicial.json
# Installed 2 object(s) from 1 fixture(s)
```

---

## 8. Ejecución del Servidor de Desarrollo

### Iniciar Servidor

```powershell
python manage.py runserver

# Salida esperada:
# Watching for file changes with StatReloader
# Performing system checks...
#
# System check identified no issues (0 silenced).
# November 27, 2025 - 15:30:00
# Django version 4.2.7, using settings 'SMASHPOINT.settings'
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK.
```

### Acceder a la Aplicación

Abrir navegador en:

- **Aplicación Principal**: [http://localhost:8000/](http://localhost:8000/)
- **Panel Admin**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **Scoreboard Público**: [http://localhost:8000/public/scoreboard/](http://localhost:8000/public/scoreboard/)

### Iniciar en Puerto Diferente (Opcional)

```powershell
python manage.py runserver 8080
# Servidor en: http://localhost:8080/
```

### Permitir Acceso desde Red Local

```powershell
python manage.py runserver 0.0.0.0:8000
# Accesible desde: http://IP_LOCAL:8000/
```

---

## 9. Verificación de la Instalación

### Checklist de Verificación

| ✅ | Paso | Comando de Verificación |
|----|------|------------------------|
| ☐ | Python instalado | `python --version` |
| ☐ | MySQL funcionando | `mysql -u root -p` |
| ☐ | Base de datos creada | `SHOW DATABASES;` en MySQL |
| ☐ | Entorno virtual activo | Prompt con `(venv)` |
| ☐ | Dependencias instaladas | `pip list` |
| ☐ | Migraciones aplicadas | `python manage.py showmigrations` |
| ☐ | Superusuario creado | Login en `/admin/` |
| ☐ | Servidor corriendo | Abrir `http://localhost:8000/` |
| ☐ | Login exitoso | Usuario y contraseña correctos |
| ☐ | CRUD funcionando | Crear jugador desde admin |

### Pruebas Funcionales Básicas

#### 1. Probar Panel de Administración

```powershell
# Con el servidor corriendo, ir a:
http://localhost:8000/admin/

# Login:
# Username: admin
# Password: [contraseña creada]

# Verificar secciones:
✅ Jugadores
✅ Torneos
✅ Grupos
✅ Partidos
✅ Inscripciones
✅ Ranking
```

#### 2. Crear Jugador de Prueba

**Desde Admin:**
1. Ir a "Jugadores" → "Añadir Jugador"
2. Completar:
   - Nombre: `Carlos`
   - Apellido: `Rojas`
   - Categoría: `AMATEUR`
   - RUT: `19876543-2`
3. Guardar

**Desde Aplicación:**
1. Login en `http://localhost:8000/`
2. Ir a "Jugadores" → "Agregar"
3. Completar formulario
4. Verificar en lista

#### 3. Importar Jugadores desde Excel

**Crear archivo `jugadores_test.xlsx`:**

| nombre | apellido | categoria | rut |
|--------|----------|-----------|-----|
| Pedro | Silva | FEDERADO | 11222333-4 |
| Ana | Martínez | AMATEUR | 15666777-8 |

**Importar:**
1. Ir a "Jugadores" → "Importar Excel"
2. Seleccionar archivo
3. Verificar importación exitosa

#### 4. Crear Torneo con Grupos

```powershell
# Desde aplicación o admin, crear torneo:
- Nombre: Torneo de Prueba
- Fecha: [fecha futura]
- Categoría: ADULTO
- Cupos: 16
- Número de grupos: 2
- Estado: ABIERTO
```

#### 5. Probar Flujo Completo

```powershell
1. Crear 8 jugadores (mínimo)
2. Crear torneo con 2 grupos
3. Inscribir jugadores al torneo
4. Generar grupos desde vista torneos
5. Asignar resultados a partidos de grupos
6. Generar bracket de eliminación
7. Completar eliminación hasta final
8. Verificar ranking actualizado
```

### Ejecutar Suite de Pruebas

```powershell
# Ejecutar todas las pruebas
python manage.py test smashpointApp

# Ejecutar con verbosidad
python manage.py test smashpointApp -v 2

# Ejecutar prueba específica
python manage.py test smashpointApp.tests.TestRondasSiguiente

# Con cobertura
coverage run --source='.' manage.py test smashpointApp
coverage report
coverage html
# Abrir: htmlcov/index.html
```

---

## 10. Solución de Problemas Comunes

### Error: `No module named 'mysqlclient'`

**Causa**: Falta instalar conector MySQL

**Solución Windows:**
```powershell
# Opción 1: Instalar desde PyPI
pip install mysqlclient

# Si falla, instalar wheel precompilado:
pip install https://download.lfd.uci.edu/pythonlibs/archived/mysqlclient-2.1.1-cp311-cp311-win_amd64.whl
```

**Solución Linux:**
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

---

### Error: `Access denied for user`

**Causa**: Credenciales MySQL incorrectas

**Solución:**
```sql
-- Verificar usuario en MySQL:
mysql -u root -p

SELECT User, Host FROM mysql.user WHERE User = 'smashpoint_user';

-- Resetear contraseña si es necesario:
ALTER USER 'smashpoint_user'@'localhost' IDENTIFIED BY 'nueva_contraseña';
FLUSH PRIVILEGES;
```

**Actualizar `settings.py`:**
```python
'PASSWORD': 'nueva_contraseña',  # Usar la nueva contraseña
```

---

### Error: `Port 8000 is already in use`

**Causa**: Otra instancia del servidor corriendo

**Solución:**
```powershell
# Opción 1: Usar otro puerto
python manage.py runserver 8001

# Opción 2: Matar proceso en Windows
netstat -ano | findstr :8000
taskkill /PID [número_PID] /F

# Opción 3: Reiniciar terminal y volver a ejecutar
```

---

### Error: `Migration Error` al ejecutar migrate

**Causa**: Migraciones inconsistentes

**Solución:**
```powershell
# Listar migraciones
python manage.py showmigrations

# Resetear migraciones de la app (¡CUIDADO! Borra datos)
python manage.py migrate smashpointApp zero

# Eliminar archivos de migración (excepto __init__.py)
# En: smashpointApp/migrations/

# Recrear migraciones
python manage.py makemigrations
python manage.py migrate
```

---

### Error: `Static files not found`

**Causa**: Archivos estáticos no configurados

**Solución:**
```powershell
# Recolectar archivos estáticos
python manage.py collectstatic

# Verificar configuración en settings.py:
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

---

### Error: Importar Excel falla con `Invalid file format`

**Causa**: Archivo no es .xlsx válido

**Solución:**
1. Abrir archivo en Excel
2. "Guardar como" → formato `.xlsx` (no `.xls`)
3. Verificar encabezados exactos: `nombre`, `apellido`, `categoria`, `rut`
4. Asegurar datos completos en todas las filas

---

### MySQL no inicia en XAMPP

**Solución:**
```powershell
# 1. Verificar puerto 3306 libre
netstat -ano | findstr :3306

# 2. Cambiar puerto MySQL en XAMPP:
# - Abrir XAMPP Control Panel
# - Config (MySQL) → my.ini
# - Cambiar: port=3306 a port=3307
# - Reiniciar MySQL

# 3. Actualizar settings.py:
'PORT': '3307',
```

---

### RUT Inválido al crear jugador

**Causa**: RUT no pasa validación módulo 11

**Solución:**

Usar RUTs válidos de prueba:
- `12.345.678-5`
- `11.111.111-1`
- `22.222.222-0`

**Verificar formato:**
- Con o sin puntos: `12345678-5` o `12.345.678-5`
- Dígito verificador: número (0-9) o K

---

### Detalle de Sets no calcula ganador

**Causa**: Formato incorrecto o diferencia de puntos insuficiente

**Solución:**

**Formato válido:**
```
11-7,11-9,11-5       ✅ Correcto
11-7, 11-9, 11-5     ✅ Correcto (con espacios)
11-7,8-11,11-9       ✅ Correcto (best of 3)
```

**Formato inválido:**
```
11:7,11:9            ❌ Usar guión, no dos puntos
11-7 11-9            ❌ Separar con comas
11-10                ❌ Diferencia menor a 2
```

**Reglas:**
- Cada set debe tener diferencia mínima de 2 puntos
- Best of 3: gana quien llega a 2 sets
- Best of 5: gana quien llega a 3 sets

---

## 📊 Flujo de Trabajo Recomendado

### Desarrollo Diario

```powershell
# 1. Activar entorno
cd C:\Users\alexa\Downloads\SmashPoint (1)\SMASHPOINT
.\venv\Scripts\activate

# 2. Actualizar código (si usas Git)
git pull origin main

# 3. Aplicar migraciones nuevas
python manage.py migrate

# 4. Iniciar servidor
python manage.py runserver

# 5. Trabajar en navegador y editor de código

# 6. Al terminar, desactivar entorno
deactivate
```

### Antes de Commit (Control de Calidad)

```powershell
# Ejecutar pruebas
python manage.py test smashpointApp

# Verificar cobertura
coverage run --source='.' manage.py test smashpointApp
coverage report

# Linter (opcional, instalar flake8)
pip install flake8
flake8 smashpointApp/ --exclude=migrations

# Formatear código (opcional, instalar black)
pip install black
black smashpointApp/
```

---

## 🚀 Puesta en Producción (Resumen)

> **Nota**: Esta es una guía básica. Para producción real se requiere configuración adicional de seguridad y performance.

### Cambios Esenciales en `settings.py`

```python
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
SECRET_KEY = 'generar_clave_aleatoria_segura'  # No usar la del repositorio

# Configurar HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Base de datos en servidor remoto
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smashpoint_prod',
        'USER': 'usuario_produccion',
        'PASSWORD': os.environ.get('DB_PASSWORD'),  # Usar variable de entorno
        'HOST': 'db.tuservidor.com',
        'PORT': '3306',
    }
}
```

### Servidor WSGI (Gunicorn)

```bash
pip install gunicorn
gunicorn SMASHPOINT.wsgi:application --bind 0.0.0.0:8000
```

### Servidor Web (Nginx ejemplo)

```nginx
server {
    listen 80;
    server_name tudominio.com;
    
    location /static/ {
        alias /ruta/a/staticfiles/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **Django**: [docs.djangoproject.com](https://docs.djangoproject.com/)
- **Django REST Framework**: [django-rest-framework.org](https://www.django-rest-framework.org/)
- **MySQL**: [dev.mysql.com/doc](https://dev.mysql.com/doc/)
- **Python**: [docs.python.org](https://docs.python.org/3/)

### Tutoriales Recomendados

- Django Girls Tutorial: [tutorial.djangogirls.org](https://tutorial.djangogirls.org/)
- Real Python: [realpython.com/tutorials/django](https://realpython.com/tutorials/django/)
- Django for Beginners: [djangoforbeginners.com](https://djangoforbeginners.com/)

### Comunidad y Soporte

- Stack Overflow: Buscar `[django]` + tu pregunta
- Django Forum: [forum.djangoproject.com](https://forum.djangoproject.com/)
- Reddit: [r/django](https://www.reddit.com/r/django/)

---

## ✅ Checklist Final

Antes de considerar el entorno completamente configurado:

- [ ] Python instalado y verificado
- [ ] MySQL/XAMPP funcionando
- [ ] Base de datos `smashpoint` creada
- [ ] Usuario MySQL con permisos configurado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas desde `requirements.txt`
- [ ] Archivo `settings.py` configurado con credenciales correctas
- [ ] Migraciones aplicadas sin errores
- [ ] Superusuario creado
- [ ] Servidor de desarrollo corriendo
- [ ] Login en aplicación exitoso
- [ ] Panel de admin accesible
- [ ] CRUD de jugadores funcionando
- [ ] Importación Excel probada
- [ ] Creación de torneo con grupos exitosa
- [ ] Suite de pruebas pasa sin errores
- [ ] Documentación revisada y comprendida

---

## 🎯 Próximos Pasos

Una vez configurado el entorno, puedes:

1. **Explorar el Admin**: Familiarizarte con modelos y relaciones
2. **Leer README_TESTING.md**: Entender estrategia de pruebas
3. **Revisar código**: Estudiar `models.py`, `views.py`, `forms.py`
4. **Ejecutar fixtures**: Cargar datos de prueba para desarrollo
5. **Personalizar**: Adaptar templates y estilos según necesidades
6. **Desarrollar**: Agregar nuevas funcionalidades o mejoras

---

## 📝 Notas Finales

- **Seguridad**: En desarrollo es aceptable usar contraseñas simples. En producción siempre usar contraseñas seguras y variables de entorno.
- **Backups**: Realizar respaldos regulares de la base de datos durante desarrollo.
- **Versionado**: Usar Git para control de versiones y no commitear archivos sensibles (`.env`, `db.sqlite3`).
- **Documentación**: Mantener esta guía actualizada con cambios en el entorno.

---

**Versión**: 1.0  
**Fecha**: Noviembre 2025  
**Autor**: Equipo SmashPoint  
**Última actualización**: 27/11/2025

---

## 📞 Contacto y Soporte

Para dudas sobre la configuración del entorno:

- **Email**: soporte@smashpoint.cl
- **Repositorio**: [github.com/smashpoint/proyecto](https://github.com/smashpoint/proyecto)
- **Issues**: Reportar problemas en GitHub Issues

---

**¡Entorno configurado exitosamente! 🎉**

Ahora estás listo para comenzar a desarrollar en SmashPoint.
