# Generated by Django 4.2.16 on 2025-02-20 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0028_alter_sousaspecteau_est_pollution'),
    ]

    operations = [
        migrations.AddField(
            model_name='suivisousaspect',
            name='cloturer',
            field=models.BooleanField(default=False),
        ),
    ]
