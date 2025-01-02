# Generated by Django 5.1.4 on 2024-12-31 13:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ponto', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='funcionario',
            name='email',
        ),
        migrations.RemoveField(
            model_name='funcionario',
            name='nome',
        ),
        migrations.AddField(
            model_name='funcionario',
            name='telefone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='funcionario', to=settings.AUTH_USER_MODEL),
        ),
    ]
