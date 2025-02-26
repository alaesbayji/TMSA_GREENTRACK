# Generated by Django 4.2.16 on 2025-02-24 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0042_entreprise_avenue_entreprise_regime_entreprise_rue_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entreprise',
            old_name='Avenue',
            new_name='avenue',
        ),
        migrations.RenameField(
            model_name='entreprise',
            old_name='Regime',
            new_name='regime',
        ),
        migrations.RenameField(
            model_name='entreprise',
            old_name='Rue',
            new_name='rue',
        ),
        migrations.RenameField(
            model_name='entreprise',
            old_name='Secteur',
            new_name='secteur',
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='DAE',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='EIE_PSSE',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='entreprise',
            name='adresse',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
