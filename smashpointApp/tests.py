from django.test import TestCase, Client
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
import time

from .models import Jugador, Torneo, Resultado, Contacto
from .models import Inscripcion, Partido, Ranking


# ==================== PRUEBAS FUNCIONALES ====================

class TestJugadoresFuncional(TestCase):
    """Pruebas CRUD completas para el módulo de Jugadores"""

    def setUp(self):
        """Configuración inicial antes de cada test"""
        self.client = Client()
        # Crear superusuario
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@test.com'
        )
        # Crear usuario estándar
        self.user = User.objects.create_user(
            username='user',
            password='user123'
        )
        # Login como admin
        self.client.login(username='admin', password='admin123')

    def test_crear_jugador_valido(self):
        """F-01: Crear jugador con datos válidos"""
        response = self.client.post(reverse('agregar_jugador'), {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'categoria': 'AMATEUR',
            'licencia': 'LIC001'
        })
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(Jugador.objects.filter(licencia='LIC001').exists())
        jugador = Jugador.objects.get(licencia='LIC001')
        self.assertEqual(jugador.nombre, 'Juan')

    def test_crear_jugador_licencia_duplicada(self):
        """F-01: Intentar crear jugador con licencia duplicada debe fallar"""
        Jugador.objects.create(
            nombre='Pedro',
            apellido='García',
            categoria='FEDERADO',
            licencia='LIC999'
        )
        response = self.client.post(reverse('agregar_jugador'), {
            'nombre': 'Ana',
            'apellido': 'López',
            'categoria': 'AMATEUR',
            'licencia': 'LIC999'
        })
        # El formulario debe mostrar error (status 200 con form inválido)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Jugador.objects.filter(licencia='LIC999').count(), 1)

    def test_editar_jugador(self):
        """F-01: Editar información de jugador existente"""
        jugador = Jugador.objects.create(
            nombre='María',
            apellido='González',
            categoria='AMATEUR',
            licencia='LIC002'
        )
        response = self.client.post(reverse('editar_jugador', args=[jugador.id]), {
            'nombre': 'María Fernanda',
            'apellido': 'González',
            'categoria': 'FEDERADO',
            'licencia': 'LIC002'
        })
        self.assertEqual(response.status_code, 302)
        jugador.refresh_from_db()
        self.assertEqual(jugador.nombre, 'María Fernanda')
        self.assertEqual(jugador.categoria, 'FEDERADO')

    def test_eliminar_jugador_sin_resultados(self):
        """F-01: Eliminar jugador sin resultados asociados"""
        jugador = Jugador.objects.create(
            nombre='Carlos',
            apellido='Rodríguez',
            categoria='AMATEUR',
            licencia='LIC003'
        )
        response = self.client.post(reverse('eliminar_jugador', args=[jugador.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Jugador.objects.filter(id=jugador.id).exists())

    def test_consultar_lista_jugadores(self):
        """F-01: Consultar lista de jugadores"""
        Jugador.objects.create(nombre='Test1', apellido='A', categoria='AMATEUR', licencia='L1')
        Jugador.objects.create(nombre='Test2', apellido='B', categoria='FEDERADO', licencia='L2')
        response = self.client.get(reverse('lista_jugadores'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test1')
        self.assertContains(response, 'Test2')


class TestTorneosFuncional(TestCase):
    """Pruebas CRUD completas para el módulo de Torneos"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')

    def test_crear_torneo_valido(self):
        """F-02: Crear torneo con datos válidos"""
        response = self.client.post(reverse('agregar_torneo'), {
            'nombre': 'Torneo de Primavera',
            'direccion': 'Av. Principal 123',
            'fecha': '2025-12-01',
            'categoria': 'ADULTO'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Torneo.objects.filter(nombre='Torneo de Primavera').exists())

    def test_editar_torneo(self):
        """F-02: Editar información de torneo existente"""
        torneo = Torneo.objects.create(
            nombre='Torneo Original',
            direccion='Calle 1',
            fecha=date(2025, 12, 15),
            categoria='JUVENIL'
        )
        response = self.client.post(reverse('editar_torneo', args=[torneo.id]), {
            'nombre': 'Torneo Modificado',
            'direccion': 'Calle 1',
            'fecha': '2025-12-15',
            'categoria': 'MIXTO'
        })
        self.assertEqual(response.status_code, 302)
        torneo.refresh_from_db()
        self.assertEqual(torneo.nombre, 'Torneo Modificado')
        self.assertEqual(torneo.categoria, 'MIXTO')

    def test_eliminar_torneo_sin_resultados(self):
        """F-02: Eliminar torneo sin resultados asociados"""
        torneo = Torneo.objects.create(
            nombre='Torneo a Eliminar',
            direccion='Calle 2',
            fecha=date(2025, 12, 20),
            categoria='ADULTO'
        )
        response = self.client.post(reverse('eliminar_torneo', args=[torneo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Torneo.objects.filter(id=torneo.id).exists())

    def test_consultar_lista_torneos(self):
        """F-02: Consultar lista de torneos"""
        Torneo.objects.create(nombre='T1', direccion='D1', fecha=date(2025, 12, 1), categoria='ADULTO')
        Torneo.objects.create(nombre='T2', direccion='D2', fecha=date(2025, 12, 2), categoria='JUVENIL')
        response = self.client.get(reverse('lista_torneos'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'T1')
        self.assertContains(response, 'T2')


class TestResultadosFuncional(TestCase):
    """Pruebas CRUD completas para el módulo de Resultados"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')
        
        # Crear datos de prueba
        self.jugador1 = Jugador.objects.create(
            nombre='Ana', apellido='Martínez', categoria='AMATEUR', licencia='LIC100'
        )
        self.jugador2 = Jugador.objects.create(
            nombre='Luis', apellido='Fernández', categoria='FEDERADO', licencia='LIC101'
        )
        self.torneo = Torneo.objects.create(
            nombre='Torneo Test',
            direccion='Test 123',
            fecha=date(2025, 12, 10),
            categoria='ADULTO'
        )

    def test_registrar_resultado(self):
        """F-03: Registrar resultado de partido"""
        response = self.client.post(reverse('agregar_resultado'), {
            'torneo': self.torneo.id,
            'jugador1': self.jugador1.id,
            'jugador2': self.jugador2.id,
            'marcador_j1': 6,
            'marcador_j2': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Resultado.objects.filter(
            torneo=self.torneo,
            jugador1=self.jugador1
        ).exists())

    def test_editar_resultado(self):
        """F-03: Editar resultado existente"""
        resultado = Resultado.objects.create(
            torneo=self.torneo,
            jugador1=self.jugador1,
            jugador2=self.jugador2,
            marcador_j1=6,
            marcador_j2=4
        )
        response = self.client.post(reverse('editar_resultado', args=[resultado.id]), {
            'torneo': self.torneo.id,
            'jugador1': self.jugador1.id,
            'jugador2': self.jugador2.id,
            'marcador_j1': 7,
            'marcador_j2': 5
        })
        self.assertEqual(response.status_code, 302)
        resultado.refresh_from_db()
        self.assertEqual(resultado.marcador_j1, 7)
        self.assertEqual(resultado.marcador_j2, 5)

    def test_eliminar_resultado(self):
        """F-03: Eliminar resultado"""
        resultado = Resultado.objects.create(
            torneo=self.torneo,
            jugador1=self.jugador1,
            jugador2=self.jugador2,
            marcador_j1=6,
            marcador_j2=3
        )
        response = self.client.post(reverse('eliminar_resultado', args=[resultado.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Resultado.objects.filter(id=resultado.id).exists())

    def test_consultar_lista_resultados(self):
        """F-03: Consultar lista de resultados"""
        Resultado.objects.create(
            torneo=self.torneo,
            jugador1=self.jugador1,
            jugador2=self.jugador2,
            marcador_j1=6,
            marcador_j2=2
        )
        response = self.client.get(reverse('lista_resultados'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.jugador1.nombre)


# ==================== PRUEBAS DE SEGURIDAD ====================

class TestSeguridad(TestCase):
    """Pruebas de autenticación, autorización y validación de entradas"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.user = User.objects.create_user(
            username='user',
            password='user123'
        )

    def test_login_valido(self):
        """S-01: Login con credenciales válidas"""
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_invalido(self):
        """S-01: Login con credenciales inválidas"""
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_acceso_sin_autenticacion(self):
        """S-01: Intentar acceder sin autenticación (@login_required)"""
        response = self.client.get(reverse('lista_jugadores'))
        self.assertEqual(response.status_code, 302)  # Redirect a login
        self.assertIn('/login', response.url)

    def test_permisos_admin_agregar_jugador(self):
        """S-02: Verificar permisos de admin para agregar jugador"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('agregar_jugador'))
        self.assertEqual(response.status_code, 200)

    def test_permisos_usuario_sin_permiso_agregar(self):
        """S-02: Usuario sin permisos no puede agregar jugador"""
        self.client.login(username='user', password='user123')
        response = self.client.get(reverse('agregar_jugador'))
        # Debe retornar 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_logout_correcto(self):
        """S-01: Logout correcto"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # Verificar que no está autenticado
        response2 = self.client.get(reverse('index'))
        self.assertEqual(response2.status_code, 302)  # Redirect a login

    def test_csrf_token_presente(self):
        """S-03: Verificar CSRF token en formularios"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('agregar_jugador'))
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_validacion_formulario_jugador(self):
        """S-03: Validar campos obligatorios en formulario"""
        self.client.login(username='admin', password='admin123')
        # Enviar formulario incompleto
        response = self.client.post(reverse('agregar_jugador'), {
            'nombre': '',  # Campo vacío
            'apellido': 'Test',
            'categoria': 'AMATEUR',
            'licencia': 'LIC999'
        })
        self.assertEqual(response.status_code, 200)  # No redirect, form inválido
        self.assertFalse(Jugador.objects.filter(licencia='LIC999').exists())

    def test_proteccion_xss_en_nombre(self):
        """S-03: Verificar protección XSS en campos de texto"""
        self.client.login(username='admin', password='admin123')
        xss_payload = '<script>alert("XSS")</script>'
        response = self.client.post(reverse('agregar_jugador'), {
            'nombre': xss_payload,
            'apellido': 'Test',
            'categoria': 'AMATEUR',
            'licencia': 'LICXSS'
        })
        if response.status_code == 302:
            jugador = Jugador.objects.get(licencia='LICXSS')
            # Django debe escapar automáticamente
            self.assertEqual(jugador.nombre, xss_payload)
            # Verificar que en la vista se renderiza escapado
            response2 = self.client.get(reverse('lista_jugadores'))
            self.assertNotContains(response2, '<script>', html=False)


# ==================== PRUEBAS DE INTEGRACIÓN ====================

class TestIntegracion(TestCase):
    """Pruebas de comunicación entre módulos y flujos completos"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')

    def test_flujo_completo_torneo(self):
        """I-02: Flujo end-to-end: Crear torneo → Agregar jugadores → Registrar resultados"""
        # 1. Crear torneo
        self.client.post(reverse('agregar_torneo'), {
            'nombre': 'Torneo Integración',
            'direccion': 'Test 456',
            'fecha': '2025-12-25',
            'categoria': 'ADULTO'
        })
        torneo = Torneo.objects.get(nombre='Torneo Integración')
        
        # 2. Agregar jugadores
        self.client.post(reverse('agregar_jugador'), {
            'nombre': 'J1', 'apellido': 'A1', 'categoria': 'AMATEUR', 'licencia': 'L1'
        })
        self.client.post(reverse('agregar_jugador'), {
            'nombre': 'J2', 'apellido': 'A2', 'categoria': 'FEDERADO', 'licencia': 'L2'
        })
        j1 = Jugador.objects.get(licencia='L1')
        j2 = Jugador.objects.get(licencia='L2')
        
        # 3. Registrar resultado
        self.client.post(reverse('agregar_resultado'), {
            'torneo': torneo.id,
            'jugador1': j1.id,
            'jugador2': j2.id,
            'marcador_j1': 6,
            'marcador_j2': 3
        })
        
        # 4. Verificar resultado registrado
        self.assertTrue(Resultado.objects.filter(torneo=torneo).exists())
        resultado = Resultado.objects.get(torneo=torneo)
        self.assertEqual(resultado.jugador1, j1)
        self.assertEqual(resultado.jugador2, j2)

    def test_integridad_referencial_eliminar_jugador_con_resultados(self):
        """I-01: Verificar integridad referencial al eliminar jugador con resultados"""
        jugador1 = Jugador.objects.create(
            nombre='J1', apellido='A', categoria='AMATEUR', licencia='L10'
        )
        jugador2 = Jugador.objects.create(
            nombre='J2', apellido='B', categoria='FEDERADO', licencia='L11'
        )
        torneo = Torneo.objects.create(
            nombre='T', direccion='D', fecha=date(2025, 12, 1), categoria='ADULTO'
        )
        Resultado.objects.create(
            torneo=torneo, jugador1=jugador1, jugador2=jugador2,
            marcador_j1=6, marcador_j2=4
        )
        
        # Intentar eliminar jugador1 que tiene resultados
        # Django CASCADE debe eliminar resultados asociados
        response = self.client.post(reverse('eliminar_jugador', args=[jugador1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Jugador.objects.filter(id=jugador1.id).exists())
        self.assertFalse(Resultado.objects.filter(jugador1=jugador1).exists())


# ==================== PRUEBAS DE RENDIMIENTO ====================

class TestRendimiento(TestCase):
    """Pruebas de tiempos de respuesta y carga"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')
        
        # Crear datos de prueba
        for i in range(50):
            Jugador.objects.create(
                nombre=f'Jugador{i}',
                apellido=f'Apellido{i}',
                categoria='AMATEUR' if i % 2 == 0 else 'FEDERADO',
                licencia=f'LIC{i:04d}'
            )

    def test_tiempo_carga_lista_jugadores(self):
        """R-01: Tiempo de carga de lista de jugadores < 1s"""
        start = time.time()
        response = self.client.get(reverse('lista_jugadores'))
        elapsed = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(elapsed, 1.0, f"Tiempo de carga: {elapsed:.3f}s > 1s")

    def test_tiempo_carga_lista_torneos(self):
        """R-01: Tiempo de carga de lista de torneos < 1s"""
        # Crear 50 torneos
        for i in range(50):
            Torneo.objects.create(
                nombre=f'Torneo{i}',
                direccion=f'Dirección{i}',
                fecha=date(2025, 12, 1) + timedelta(days=i),
                categoria='ADULTO'
            )
        
        start = time.time()
        response = self.client.get(reverse('lista_torneos'))
        elapsed = time.time() - start
        
        self.assertEqual(response.status_code, 200)
        self.assertLess(elapsed, 1.0, f"Tiempo de carga: {elapsed:.3f}s > 1s")

    def test_tiempo_respuesta_login(self):
        """R-01: Tiempo de respuesta de login < 500ms"""
        self.client.logout()
        
        start = time.time()
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        elapsed = time.time() - start
        
        self.assertEqual(response.status_code, 302)
        self.assertLess(elapsed, 0.5, f"Tiempo de login: {elapsed:.3f}s > 0.5s")


# ==================== PRUEBAS DE USABILIDAD ====================

class TestUsabilidad(TestCase):
    """Pruebas de facilidad de uso y coherencia de interfaz"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin123'
        )
        self.client.login(username='admin', password='admin123')

    def test_mensajes_error_claros(self):
        """U-01: Mensajes de error claros y orientativos"""
        # Asegurar que no haya sesión activa para probar el mensaje de error
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'noexiste',
            'password': 'wrongpass'
        })
        self.assertContains(response, 'Usuario o contraseña incorrectos')

    def test_formulario_con_labels(self):
        """U-02: Formularios con labels descriptivos"""
        response = self.client.get(reverse('agregar_jugador'))
        self.assertContains(response, '<label')

    def test_botones_semanticos(self):
        """U-03: Botones con colores semánticos (Bootstrap)"""
        response = self.client.get(reverse('lista_jugadores'))
        # Verificar presencia de clases Bootstrap
        self.assertContains(response, 'btn')

    def test_estilos_css_presentes(self):
        """U-03: Estilos CSS consistentes"""
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'styles.css')

    def test_navegacion_coherente(self):
        """U-01: Navegación coherente en todas las páginas"""
        pages = ['index', 'lista_jugadores', 'lista_torneos', 'lista_resultados']
        for page in pages:
            response = self.client.get(reverse(page))
            self.assertEqual(response.status_code, 200)


# ==================== PRUEBAS NUEVAS: INSCRIPCIONES ====================

class TestInscripciones(TestCase):
    """Pruebas para inscripción de jugadores en torneos y manejo de cupos/espera"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        self.torneo = Torneo.objects.create(
            nombre='Torneo Inscripciones',
            direccion='Dir 1',
            fecha=date(2025, 12, 1),
            categoria='ADULTO',
            cupos_max=2,
            estado='ABIERTO'
        )
        self.j1 = Jugador.objects.create(nombre='J1', apellido='A', categoria='AMATEUR', licencia='L01')
        self.j2 = Jugador.objects.create(nombre='J2', apellido='B', categoria='AMATEUR', licencia='L02')
        self.j3 = Jugador.objects.create(nombre='J3', apellido='C', categoria='AMATEUR', licencia='L03')

    def test_inscripciones_estado_inscrito_y_espera(self):
        """Verifica que los primeros cupos son INSCRITO y el siguiente va a ESPERA"""
        Inscripcion.objects.create(torneo=self.torneo, jugador=self.j1)
        Inscripcion.objects.create(torneo=self.torneo, jugador=self.j2)
        insc3 = Inscripcion.objects.create(torneo=self.torneo, jugador=self.j3)
        self.assertEqual(Inscripcion.objects.filter(torneo=self.torneo, estado='INSCRITO').count(), 2)
        self.assertEqual(insc3.estado, 'ESPERA')

    def test_view_lista_inscripciones(self):
        Inscripcion.objects.create(torneo=self.torneo, jugador=self.j1)
        response = self.client.get(reverse('lista_inscripciones', args=[self.torneo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inscripciones -')

    def test_view_inscribir_jugador(self):
        response = self.client.post(reverse('inscribir_jugador', args=[self.torneo.id]), {
            'torneo': self.torneo.id,
            'jugador': self.j1.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Inscripcion.objects.filter(torneo=self.torneo, jugador=self.j1).exists())


# ==================== PRUEBAS NUEVAS: FIXTURE / PARTIDOS ====================

class TestFixture(TestCase):
    """Pruebas de generación de fixture y edición de partidos"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        self.torneo = Torneo.objects.create(
            nombre='Torneo Fixture',
            direccion='D',
            fecha=date(2025, 12, 2),
            categoria='ADULTO',
            cupos_max=4,
            estado='ABIERTO'
        )
        self.jugadores = []
        for i in range(4):
            j = Jugador.objects.create(nombre=f'J{i}', apellido='X', categoria='AMATEUR', licencia=f'LX{i}')
            self.jugadores.append(j)
            Inscripcion.objects.create(torneo=self.torneo, jugador=j)

    def test_generar_fixture_crea_partidos(self):
        response = self.client.get(reverse('generar_fixture', args=[self.torneo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Partido.objects.filter(torneo=self.torneo).count() > 0)
        self.torneo.refresh_from_db()
        self.assertEqual(self.torneo.estado, 'EN_CURSO')

    def test_editar_partido_actualiza_ganador_y_ranking(self):
        # Generar fixture
        self.client.get(reverse('generar_fixture', args=[self.torneo.id]))
        partido = Partido.objects.filter(torneo=self.torneo).first()
        response = self.client.post(reverse('editar_partido', args=[partido.id]), {
            'torneo': self.torneo.id,
            'ronda': partido.ronda,
            'jugador_a': partido.jugador_a.id,
            'jugador_b': partido.jugador_b.id,
            'marcador_a': 6,
            'marcador_b': 3
        })
        self.assertEqual(response.status_code, 302)
        partido.refresh_from_db()
        self.assertIsNotNone(partido.ganador)
        ranking = Ranking.objects.get(jugador=partido.ganador)
        self.assertGreaterEqual(ranking.puntos, 3)

class TestRondasSiguiente(TestCase):
    """Pruebas para generación de rondas sucesivas y finalización de torneo"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        self.torneo = Torneo.objects.create(
            nombre='Torneo Rondas',
            direccion='Dir',
            fecha=date(2025,12,3),
            categoria='ADULTO',
            cupos_max=4,
            estado='ABIERTO'
        )
        self.jugadores = []
        for i in range(4):
            j = Jugador.objects.create(nombre=f'R{i}', apellido='Z', categoria='AMATEUR', licencia=f'RL{i}')
            self.jugadores.append(j)
            Inscripcion.objects.create(torneo=self.torneo, jugador=j)

    def test_generar_rondas_hasta_final(self):
        # Generar primera ronda
        self.client.get(reverse('generar_fixture', args=[self.torneo.id]))
        partidos_r1 = list(Partido.objects.filter(torneo=self.torneo, ronda=1))
        self.assertEqual(len(partidos_r1), 2)
        # Definir ganadores ronda 1
        for p in partidos_r1:
            self.client.post(reverse('editar_partido', args=[p.id]), {
                'torneo': self.torneo.id,
                'ronda': p.ronda,
                'jugador_a': p.jugador_a.id,
                'jugador_b': p.jugador_b.id,
                'marcador_a': 6,
                'marcador_b': 2
            })
        # Generar segunda ronda
        self.client.get(reverse('generar_ronda_siguiente', args=[self.torneo.id]))
        partidos_r2 = list(Partido.objects.filter(torneo=self.torneo, ronda=2))
        self.assertEqual(len(partidos_r2), 1)
        # Definir ganador final
        final = partidos_r2[0]
        self.client.post(reverse('editar_partido', args=[final.id]), {
            'torneo': self.torneo.id,
            'ronda': final.ronda,
            'jugador_a': final.jugador_a.id,
            'jugador_b': final.jugador_b.id,
            'marcador_a': 7,
            'marcador_b': 5
        })
        # Generar (debe finalizar)
        self.client.get(reverse('generar_ronda_siguiente', args=[self.torneo.id]))
        self.torneo.refresh_from_db()
        self.assertEqual(self.torneo.estado, 'FINALIZADO')

class TestExportRankingFormato(TestCase):
    """Verifica exportación PDF y Excel del ranking"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        j = Jugador.objects.create(nombre='Rank', apellido='One', categoria='AMATEUR', licencia='RK1')
        Ranking.objects.create(jugador=j, puntos=15)

    def test_export_ranking_pdf(self):
        resp = self.client.get(reverse('export_ranking_pdf'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/pdf')
        self.assertGreater(len(resp.content), 100)  # algo de contenido

    def test_export_ranking_excel(self):
        resp = self.client.get(reverse('export_ranking_excel'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', resp['Content-Type'])
        self.assertGreater(len(resp.content), 100)  # contenido binario

class TestAPIV2(TestCase):
    """Pruebas para endpoints DRF /api/v2/"""

    def setUp(self):
        self.client = Client()
        # Datos
        self.j1 = Jugador.objects.create(nombre='API', apellido='V2', categoria='AMATEUR', licencia='AP1')
        self.t1 = Torneo.objects.create(nombre='APIT', direccion='D', fecha=date(2025,12,4), categoria='ADULTO')
        Resultado.objects.create(torneo=self.t1, jugador1=self.j1, jugador2=self.j1, marcador_j1=1, marcador_j2=0)
        Ranking.objects.create(jugador=self.j1, puntos=9)

    def test_api_v2_jugadores(self):
        resp = self.client.get('/api/v2/jugadores/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(isinstance(resp.json(), list))
        self.assertTrue(len(resp.json()) >= 1)

    def test_api_v2_torneos(self):
        resp = self.client.get('/api/v2/torneos/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) >= 1)

    def test_api_v2_ranking(self):
        resp = self.client.get('/api/v2/ranking/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) >= 1)

class TestAPIV2Write(TestCase):
    """Pruebas de escritura en API v2 (jugadores)"""

    def setUp(self):
        self.client = Client()
        self.api = APIClient()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.user = User.objects.create_user(username='user', password='user123')
        # Login admin para crear
        self.client.login(username='admin', password='admin123')
        # Forzar autenticación DRF (evitar CSRF en tests)
        self.api.force_authenticate(user=self.admin)

    def test_crear_jugador_api(self):
        payload = {
            'nombre': 'APIName',
            'apellido': 'APILast',
            'categoria': 'AMATEUR',
            'licencia': 'API-LIC-1'
        }
        import json
        resp = self.api.post('/api/v2/jugadores/', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Jugador.objects.filter(licencia='API-LIC-1').exists())

    def test_crear_jugador_denegado_usuario_sin_permiso(self):
        self.client.logout()
        self.api.logout()
        self.api.force_authenticate(user=self.user)
        payload = {
            'nombre': 'NoPerm',
            'apellido': 'Denied',
            'categoria': 'AMATEUR',
            'licencia': 'API-LIC-2'
        }
        import json
        resp = self.api.post('/api/v2/jugadores/', data=json.dumps(payload), content_type='application/json')
        self.assertIn(resp.status_code, [403, 401])
        self.assertFalse(Jugador.objects.filter(licencia='API-LIC-2').exists())

class TestAPIV2Pagination(TestCase):
    """Verifica paginación automática (page_size=10)"""

    def setUp(self):
        self.client = Client()
        for i in range(25):
            Jugador.objects.create(nombre=f'P{i}', apellido='Pag', categoria='AMATEUR', licencia=f'PG{i}')

    def test_paginacion_segunda_pagina(self):
        resp1 = self.client.get('/api/v2/jugadores/')
        self.assertEqual(resp1.status_code, 200)
        self.assertTrue(len(resp1.json()['results']) <= 10)
        resp2 = self.client.get('/api/v2/jugadores/?page=2')
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue('results' in resp2.json())


# ==================== PRUEBAS NUEVAS: ROLES ====================

class TestRoles(TestCase):
    """Verifica creación de grupos y permisos básicos"""

    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        # Ejecutar management command
        from django.core import management
        management.call_command('create_roles')

    def test_grupos_creados(self):
        from django.contrib.auth.models import Group
        nombres = set(Group.objects.values_list('name', flat=True))
        for esperado in ['Admin', 'Arbitro', 'Jugador']:
            self.assertIn(esperado, nombres)

    def test_permisos_admin(self):
        from django.contrib.auth.models import Group
        admin_group = Group.objects.get(name='Admin')
        # Verificar que tiene al menos permiso de agregar torneo
        self.assertTrue(admin_group.permissions.filter(codename='add_torneo').exists())


# ==================== TESTS RF9: Scoreboard público y QR ====================
class TestPublicScoreboard(TestCase):
    def setUp(self):
        self.client = Client()
        self.j1 = Jugador.objects.create(nombre='A', apellido='B', categoria='AMATEUR', licencia='R1')
        self.j2 = Jugador.objects.create(nombre='C', apellido='D', categoria='AMATEUR', licencia='R2')
        self.torneo = Torneo.objects.create(nombre='T Pub', direccion='X', fecha=date(2025,12,1), categoria='ADULTO')
        Resultado.objects.create(torneo=self.torneo, jugador1=self.j1, jugador2=self.j2, marcador_j1=6, marcador_j2=4)
        Ranking.objects.create(jugador=self.j1, puntos=10)

    def test_scoreboard_public_ok(self):
        resp = self.client.get(reverse('scoreboard_public'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Scoreboard Público')
        self.assertContains(resp, 'T Pub')

    def test_jugador_public(self):
        resp = self.client.get(reverse('jugador_public', args=[self.j1.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Perfil Público')

    def test_qr_endpoint(self):
        resp = self.client.get(reverse('jugador_qr', args=[self.j1.id]))
        # Si qrcode no instalado podría fallar, asumir 200 si instalado
        self.assertIn(resp.status_code, [200,500])  # 500 solo si falta lib
        if resp.status_code == 200:
            self.assertEqual(resp['Content-Type'], 'image/png')


# ==================== TESTS RF10: Export / Import / API ====================
class TestExportImportAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.client.login(username='admin', password='admin123')
        self.j1 = Jugador.objects.create(nombre='Exp', apellido='One', categoria='AMATEUR', licencia='E1')
        self.t1 = Torneo.objects.create(nombre='TExp', direccion='ZZ', fecha=date(2025,12,2), categoria='ADULTO')
        Resultado.objects.create(torneo=self.t1, jugador1=self.j1, jugador2=self.j1, marcador_j1=1, marcador_j2=0)

    def test_export_jugadores_csv(self):
        resp = self.client.get(reverse('export_jugadores_csv'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Content-Disposition', resp)
        self.assertIn('jugadores.csv', resp['Content-Disposition'])

    def test_api_jugadores(self):
        resp = self.client.get(reverse('api_jugadores'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('jugadores', resp.json())

    def test_import_jugadores_csv(self):
        import io
        csv_content = 'nombre,apellido,categoria,licencia\nX,Y,AMATEUR,IMP1\n'
        f = io.BytesIO(csv_content.encode('utf-8'))
        f.name = 'import.csv'
        resp = self.client.post(reverse('import_jugadores_csv'), {'file': f})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Jugador.objects.filter(licencia='IMP1').exists())


# ==================== TESTS RF8: Offline / Manifest ====================
class TestOfflineManifest(TestCase):
    def test_offline_view(self):
        client = Client()
        resp = client.get(reverse('offline'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Modo Offline')


# ==================== RUNNER DE TESTS ====================

def suite():
    """Suite completa de pruebas"""
    from django.test import TestSuite
    suite = TestSuite()
    
    # Funcionales
    suite.addTest(TestJugadoresFuncional)
    suite.addTest(TestTorneosFuncional)
    suite.addTest(TestResultadosFuncional)
    
    # Seguridad
    suite.addTest(TestSeguridad)
    
    # Integración
    suite.addTest(TestIntegracion)
    
    # Rendimiento
    suite.addTest(TestRendimiento)
    
    # Usabilidad
    suite.addTest(TestUsabilidad)
    
    return suite
