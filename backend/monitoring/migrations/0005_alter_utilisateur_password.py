# Generated by Django 4.2.16 on 2025-02-10 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0004_alter_utilisateur_password_echeance_suivi_echeance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$600000$bfvR3adQHm7hfelY0zjyq8$+MIRYnBIzpjbr32w8kg6BDdKskXScRrru/nKXrveASc=', max_length=100),
        ),
    ]
