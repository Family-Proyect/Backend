# Generated by Django 3.0.1 on 2020-10-27 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0005_contactanos_testimonios_tips'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consejeria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=150)),
                ('empieza', models.DateTimeField(blank=True)),
                ('termina', models.DateTimeField(blank=True)),
                ('tema', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=150)),
                ('estado', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
