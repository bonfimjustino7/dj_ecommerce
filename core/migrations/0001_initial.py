# Generated by Django 3.0.5 on 2020-05-09 12:32

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('estoque', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Título')),
                ('header', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='*O conteúdo pré-inscrito foi baseado no produto selecionado', null=True, verbose_name='Chamada')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='*O conteúdo pré-inscrito foi baseado no produto selecionado.', null=True, verbose_name='Conteúdo')),
                ('dt_created', models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True, verbose_name='Slug')),
                ('publicated', models.BooleanField(default=False, help_text='Marque a caixa acima se quiser publicar este post.', verbose_name='Publicado')),
                ('dt_publication', models.DateTimeField(blank=True, null=True, verbose_name='Data de publicação')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='estoque.Produto')),
            ],
            options={
                'verbose_name': 'Artigo',
                'verbose_name_plural': 'Artigos',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=250, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Sessão',
                'verbose_name_plural': 'Sessões',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Nome')),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Article')),
            ],
            options={
                'verbose_name': 'Tag (Palavras Chaves)',
                'verbose_name_plural': 'Tags (Palavras Chaves)',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
                ('link', models.CharField(blank=True, max_length=250, null=True, verbose_name='URL')),
                ('is_active', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('article', smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='section', chained_model_field='section', default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Article', verbose_name='Artigo')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='core.Menu', verbose_name='Pai')),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Section', verbose_name='Seção')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade de produtos')),
                ('date_compra', models.DateTimeField(auto_now_add=True, verbose_name='Data da Compra')),
                ('comprador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Article')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Section', verbose_name='Sessão'),
        ),
    ]
