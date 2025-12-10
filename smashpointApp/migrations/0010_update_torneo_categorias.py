from django.db import migrations


def forwards(apps, schema_editor):
    Torneo = apps.get_model('smashpointApp', 'Torneo')
    allowed = {
        'PENECA',
        'PREINFANTIL',
        'INFANTIL',
        'JUVENIL',
        'TODO_COMPETIDOR',
        'PARALIMPICO',
        'MASTER',
    }
    remap = {
        'ADULTO': 'TODO_COMPETIDOR',
        'MIXTO': 'TODO_COMPETIDOR',
    }

    for torneo in Torneo.objects.all():
        nuevo_valor = remap.get(torneo.categoria, torneo.categoria)
        if nuevo_valor not in allowed:
            nuevo_valor = 'TODO_COMPETIDOR'
        if nuevo_valor != torneo.categoria:
            torneo.categoria = nuevo_valor
            torneo.save(update_fields=['categoria'])


def noop_reverse(apps, schema_editor):
    # No revertimos porque los valores anteriores ya no son válidos.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('smashpointApp', '0009_update_best_of_eliminacion'),
    ]

    operations = [
        migrations.RunPython(forwards, noop_reverse),
    ]
