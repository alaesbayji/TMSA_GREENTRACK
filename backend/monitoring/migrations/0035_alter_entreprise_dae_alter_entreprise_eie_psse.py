# Generated by Django 4.2.16 on 2025-02-22 21:56

from django.db import migrations, models
import monitoring.models.enterprise_models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0034_alter_parcelle_geom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entreprise',
            name='DAE',
            field=models.FileField(blank=True, null=True, upload_to=monitoring.models.enterprise_models.set_entreprise_file_path),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='EIE_PSSE',
            field=models.FileField(blank=True, null=True, upload_to=monitoring.models.enterprise_models.set_entreprise_file_path),
        ),
    ]
