# Generated by Django 4.2.16 on 2025-02-20 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0026_aspect_est_eau_sousaspecteau_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='engagementaspect',
            name='unique_engagement_aspect_aspect',
        ),
        migrations.AddConstraint(
            model_name='engagementaspect',
            constraint=models.UniqueConstraint(fields=('id_aspect', 'id_sous_aspect_eau'), name='unique_engagement_aspect_aspect'),
        ),
    ]
