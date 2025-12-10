from django.db import models
from django.core.exceptions import ValidationError


def validar_rut_chileno(value: str):
    """Valida un RUT chileno (formato base con o sin puntos, con guión antes del dígito verificador).
    Algoritmo: Módulo 11.
    - Se limpia (remove puntos y guiones) exceptuando el DV final.
    - El DV puede ser número o 'K'.
    """
    if not value:
        return
    rut = value.upper().replace('.', '').replace('-', '')
    if len(rut) < 8 or len(rut) > 9:
        raise ValidationError('RUT debe tener 8 a 9 caracteres (sin puntos).')
    cuerpo, dv = rut[:-1], rut[-1]
    if not cuerpo.isdigit():
        raise ValidationError('Cuerpo del RUT debe ser numérico.')
    # Calcular DV esperado
    reversed_digits = map(int, reversed(cuerpo))
    factors = [2,3,4,5,6,7]
    acc = 0
    i = 0
    for d in reversed_digits:
        acc += d * factors[i]
        i = (i + 1) % len(factors)
    expected = 11 - (acc % 11)
    if expected == 11:
        expected_dv = '0'
    elif expected == 10:
        expected_dv = 'K'
    else:
        expected_dv = str(expected)
    if dv != expected_dv:
        raise ValidationError('RUT inválido: dígito verificador incorrecto.')


# Create your models here.

class Jugador(models.Model):
    CATEGORIAS = [
        ('AMATEUR', 'Amateur'),
        ('FEDERADO', 'Federado'),
    ]

    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    # Reemplaza la licencia: nuevo campo RUT único validado. Se deja licencia en BD para no perder datos previos.
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True, validators=[validar_rut_chileno], help_text="RUT chileno válido (ej: 12.345.678-5)")
    licencia = models.CharField(max_length=20, unique=True, null=True, blank=True)
    origen = models.CharField(max_length=80, null=True, blank=True, help_text="Ciudad/Región de procedencia")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


# -------------------- TORNEOS --------------------
class Torneo(models.Model):
    CATEGORIAS_TORNEO = [
        ('PENECA', 'Peneca'),
        ('PREINFANTIL', 'Preinfantil'),
        ('INFANTIL', 'Infantil'),
        ('JUVENIL', 'Juvenil'),
        ('TODO_COMPETIDOR', 'Todo Competidor'),
        ('PARALIMPICO', 'Paralímpico'),
        ('MASTER', 'Máster'),
    ]

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    fecha = models.DateField()
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_TORNEO)
    cupos_max = models.PositiveIntegerField(default=32)
    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('EN_CURSO', 'En Curso'),
        ('FINALIZADO', 'Finalizado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')
    total_rondas = models.PositiveIntegerField(null=True, blank=True)
    numero_grupos = models.PositiveIntegerField(default=0, help_text="Cantidad de grupos (0 = sin fase de grupos)")

    def __str__(self):
        return self.nombre

    def inscripciones_count(self):
        return self.inscripcion_set.filter(estado='INSCRITO').count()

    def tiene_cupos(self):
        return self.inscripciones_count() < self.cupos_max

    def calcular_total_rondas(self):
        inscritos = self.inscripcion_set.filter(estado='INSCRITO').count()
        r = 0
        n = 1 if inscritos == 0 else inscritos
        while n > 1:
            n = n // 2
            r += 1
        self.total_rondas = r or 1
        self.save()


# -------------------- RESULTADOS --------------------
class Resultado(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    jugador1 = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='jugador1_resultado')
    jugador2 = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='jugador2_resultado')
    marcador_j1 = models.IntegerField()
    marcador_j2 = models.IntegerField()

    def marcador(self):
        return f"{self.marcador_j1} - {self.marcador_j2}"

    def __str__(self):
        return f"{self.torneo} | {self.jugador1} vs {self.jugador2}"



# -------------------- CONTACTO --------------------
class Contacto(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    mensaje = models.TextField()

    def __str__(self):
        return self.nombre


# -------------------- INSCRIPCIONES --------------------
class Inscripcion(models.Model):
    ESTADOS = [
        ('INSCRITO', 'Inscrito'),
        ('ESPERA', 'Lista de Espera'),
        ('CANCELADO', 'Cancelado'),
    ]
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='INSCRITO')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('torneo', 'jugador')

    def __str__(self):
        return f"{self.jugador} -> {self.torneo} ({self.estado})"

    def save(self, *args, **kwargs):
        # Asignar estado automáticamente según cupos solo si es nuevo
        if self.pk is None and self.torneo.estado == 'ABIERTO':
            if self.torneo.tiene_cupos():
                self.estado = 'INSCRITO'
            else:
                self.estado = 'ESPERA'
        super().save(*args, **kwargs)


# -------------------- PARTIDOS (Fixtures) --------------------
class Grupo(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='grupos')
    nombre = models.CharField(max_length=5)
    jugadores = models.ManyToManyField('Jugador', related_name='grupos', blank=True)

    class Meta:
        unique_together = ('torneo','nombre')

    def __str__(self):
        return f"{self.torneo.nombre} - Grupo {self.nombre}"

    def estadisticas(self):
        """Devuelve dict por jugador: PJ, PG, PP, SA, SB (sets a favor/en contra)."""
        data = {}
        for j in self.jugadores.all():
            data[j.id] = {'jugador': j, 'PJ':0,'PG':0,'PP':0,'SA':0,'SB':0}
        from .models import Partido  # local import to avoid circular
        for p in Partido.objects.filter(torneo=self.torneo, etapa='GRUPOS', grupo=self.nombre):
            if p.sets_a is not None and p.sets_b is not None:
                # Jugador A stats
                da = data[p.jugador_a_id]
                db = data[p.jugador_b_id]
                da['PJ'] += 1
                db['PJ'] += 1
                da['SA'] += p.sets_a
                da['SB'] += p.sets_b
                db['SA'] += p.sets_b
                db['SB'] += p.sets_a
                if p.ganador_id == p.jugador_a_id:
                    da['PG'] += 1
                    db['PP'] += 1
                elif p.ganador_id == p.jugador_b_id:
                    db['PG'] += 1
                    da['PP'] += 1
        # Ordenar por PG, diferencia sets SA-SB
        orden = sorted(data.values(), key=lambda d: (d['PG'], d['SA']-d['SB']), reverse=True)
        return orden

class Partido(models.Model):
    ETAPAS = [
        ('ELIMINACION', 'Eliminación'),
        ('GRUPOS', 'Grupos'),
        ('FINAL', 'Final'),
    ]
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    ronda = models.IntegerField(default=1)
    etapa = models.CharField(max_length=15, choices=ETAPAS, default='ELIMINACION')
    grupo = models.CharField(max_length=10, null=True, blank=True, help_text="Identificador del grupo (ej: A, B, C)")
    jugador_a = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='partidos_jugador_a')
    jugador_b = models.ForeignKey(Jugador, on_delete=models.CASCADE, related_name='partidos_jugador_b')
    marcador_a = models.IntegerField(null=True, blank=True)
    marcador_b = models.IntegerField(null=True, blank=True)
    # Sets ganados (para fase grupos / final best-of)
    sets_a = models.IntegerField(null=True, blank=True)
    sets_b = models.IntegerField(null=True, blank=True)
    detalle_sets = models.CharField(max_length=120, null=True, blank=True, help_text="Formato: 11-7,8-11,11-9")
    best_of = models.PositiveIntegerField(default=3, help_text="Cantidad máxima de sets (3 ó 5). Se gana mayoría.")
    ganador = models.ForeignKey(Jugador, on_delete=models.SET_NULL, null=True, blank=True, related_name='partidos_ganados')

    def __str__(self):
        return f"{self.torneo} R{self.ronda}: {self.jugador_a} vs {self.jugador_b}"

    def calcular_ganador(self):
        # Prioridad a sets si existen
        if self.best_of > 1 and (self.sets_a is not None and self.sets_b is not None):
            if self.sets_a > self.sets_b:
                self.ganador = self.jugador_a
            elif self.sets_b > self.sets_a:
                self.ganador = self.jugador_b
            else:
                self.ganador = None
            self.save()
        elif self.marcador_a is not None and self.marcador_b is not None:
            if self.marcador_a > self.marcador_b:
                self.ganador = self.jugador_a
            elif self.marcador_b > self.marcador_a:
                self.ganador = self.jugador_b
            else:
                self.ganador = None
            self.save()

        # Puntos ranking según etapa
        if self.ganador:
            if self.etapa == 'GRUPOS':
                rk_g, _ = Ranking.objects.get_or_create(jugador=self.ganador)
                rk_g.agregar_puntos(2)
                perdedor = self.jugador_a if self.ganador == self.jugador_b else self.jugador_b
                rk_p, _ = Ranking.objects.get_or_create(jugador=perdedor)
                rk_p.agregar_puntos(1)
            elif self.etapa in ['ELIMINACION','FINAL']:
                base = 3
                bonus = self.ronda
                puntos = base + bonus
                if self.etapa == 'FINAL':
                    puntos += 5
                rk_g, _ = Ranking.objects.get_or_create(jugador=self.ganador)
                rk_g.agregar_puntos(puntos)
                perdedor = self.jugador_a if self.ganador == self.jugador_b else self.jugador_b
                rk_p, _ = Ranking.objects.get_or_create(jugador=perdedor)
                rk_p.agregar_puntos(1)

    def parsear_detalle_sets(self):
        """Convierte detalle_sets en sets ganados para cada jugador, asumiendo formato '11-7,8-11,...'."""
        if not self.detalle_sets:
            return
        sets_a = 0
        sets_b = 0
        import re
        pattern = re.compile(r'^\d{1,2}-\d{1,2}(,\d{1,2}-\d{1,2})*$')
        if not pattern.match(self.detalle_sets.replace(' ', '')):
            return  # formato inválido, ignorar
        for par in self.detalle_sets.split(','):
            par = par.strip()
            if not par:
                continue
            try:
                a,b = par.split('-')
                a = int(a)
                b = int(b)
            except ValueError:
                continue
            # Diferencia mínima de 2 puntos salvo que ninguno llegue a 11 (flexible)
            if a == b or (max(a,b) < 11) or (abs(a-b) < 2):
                continue
            if a > b:
                sets_a += 1
            else:
                sets_b += 1
        self.sets_a = sets_a
        self.sets_b = sets_b
        # Determinar ganador si alguien alcanzó mayoría
        objetivo = (self.best_of // 2) + 1
        if sets_a >= objetivo or sets_b >= objetivo:
            self.calcular_ganador()
        else:
            self.save()


# -------------------- RANKING --------------------
class Ranking(models.Model):
    jugador = models.OneToOneField(Jugador, on_delete=models.CASCADE)
    puntos = models.IntegerField(default=0)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.jugador} - {self.puntos} pts"

    def agregar_puntos(self, pts):
        self.puntos += pts
        self.save()