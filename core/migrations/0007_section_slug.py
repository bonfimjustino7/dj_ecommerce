# Generated by Django 3.0.5 on 2020-05-04 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_compra_date_compra'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True, verbose_name='Slug'),
        ),
    ]
