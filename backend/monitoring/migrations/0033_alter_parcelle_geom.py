# Generated by Django 4.2.16 on 2025-02-22 17:30

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0032_parcelle_entreprise_id_parcelle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcelle',
            name='geom',
            field=django.contrib.gis.db.models.fields.GeometryField(srid=4326),
        ),
    ]
