# Generated by Django 3.0.5 on 2020-05-09 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('estoque', '0003_auto_20200509_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentacao',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='movimentacao',
            name='quantidade',
            field=models.IntegerField(verbose_name='Quantidade Adicionada'),
        ),
        migrations.AlterField(
            model_name='tipomovimentacao',
            name='tipo',
            field=models.CharField(choices=[('Entrada', 'E'), ('Saída', 'S'), ('Estorno Entrada', 'EE'), ('Estorno Saída', 'ES')], max_length=15),
        ),
    ]
