# Generated by Django 3.0.5 on 2020-05-11 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0004_auto_20200509_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='imgs'),
        ),
    ]