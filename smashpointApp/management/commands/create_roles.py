from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from smashpointApp.models import Jugador, Torneo, Resultado, Partido, Inscripcion

ROLE_DEFINITIONS = {
    'Admin': {
        'models': [Jugador, Torneo, Resultado, Partido, Inscripcion],
        'perms': ['add', 'change', 'delete', 'view']
    },
    'Arbitro': {
        'models': [Resultado, Partido],
        'perms': ['add', 'change', 'view']
    },
    'Jugador': {
        'models': [Jugador, Inscripcion, Torneo],
        'perms': ['view']
    }
}

class Command(BaseCommand):
    help = 'Crea grupos de roles y asigna permisos básicos.'

    def handle(self, *args, **options):
        for role_name, cfg in ROLE_DEFINITIONS.items():
            group, created = Group.objects.get_or_create(name=role_name)
            added = 0
            for model in cfg['models']:
                ct = ContentType.objects.get_for_model(model)
                for action in cfg['perms']:
                    codename = f'{action}_{model._meta.model_name}'
                    try:
                        perm = Permission.objects.get(content_type=ct, codename=codename)
                        group.permissions.add(perm)
                        added += 1
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Permiso no encontrado: {codename}'))
            self.stdout.write(self.style.SUCCESS(f'Grupo {role_name} listo (permisos asignados: {added})'))
        self.stdout.write(self.style.SUCCESS('Roles creados / actualizados correctamente.'))
