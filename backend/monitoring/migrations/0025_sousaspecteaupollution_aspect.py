# Generated by Django 4.2.16 on 2025-02-20 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0024_activiteindustrielle_engagementindicateursousaspect_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sousaspecteaupollution',
            name='aspect',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sous_aspects', to='monitoring.aspect'),
        ),
    ]
