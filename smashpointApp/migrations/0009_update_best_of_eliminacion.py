# Generated migration to update best_of for elimination matches

from django.db import migrations

def update_best_of(apps, schema_editor):
    Partido = apps.get_model('smashpointApp', 'Partido')
    # Update all ELIMINACION and FINAL matches to best_of=3
    Partido.objects.filter(etapa__in=['ELIMINACION', 'FINAL']).update(best_of=3)

def reverse_update_best_of(apps, schema_editor):
    # Reverse operation (optional)
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('smashpointApp', '0008_alter_partido_best_of'),
    ]

    operations = [
        migrations.RunPython(update_best_of, reverse_update_best_of),
    ]
