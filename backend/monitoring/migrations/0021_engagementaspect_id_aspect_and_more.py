# Generated by Django 4.2.16 on 2025-02-13 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0020_remove_suivi_echeance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagementaspect',
            name='id_aspect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.aspect'),
        ),
        migrations.AddConstraint(
            model_name='engagementaspect',
            constraint=models.UniqueConstraint(fields=('id_aspect',), name='unique_engagement_aspect_aspect'),
        ),
    ]
