# Generated by Django 3.0.1 on 2020-10-21 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0003_auto_20200912_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos_tema',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
