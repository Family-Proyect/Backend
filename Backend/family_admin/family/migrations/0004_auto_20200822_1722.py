# Generated by Django 3.0.1 on 2020-08-22 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0003_categoria_tema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria_tema',
            name='id_tema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='family.Tema'),
        ),
    ]
