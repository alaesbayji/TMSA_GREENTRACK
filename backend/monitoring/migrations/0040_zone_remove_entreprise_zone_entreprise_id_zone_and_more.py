# Generated by Django 4.2.16 on 2025-02-24 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0039_alter_entreprise_id_parcelle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id_zone', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='entreprise',
            name='zone',
        ),
        migrations.AddField(
            model_name='entreprise',
            name='id_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.zone'),
        ),
        migrations.AddField(
            model_name='parcelle',
            name='id_zone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitoring.zone'),
        ),
    ]
