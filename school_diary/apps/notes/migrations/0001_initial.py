# Generated by Django 3.1.2 on 2021-02-17 20:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.notes.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='NotesGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_date', models.DateField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('public', models.BooleanField(default=False, verbose_name='Виден ученикам из других классов')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='notes.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Конспект',
                'verbose_name_plural': 'Конспекты',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.notes.models.upload_notes, verbose_name='Фото')),
                ('number', models.IntegerField(default=1, verbose_name='Номер')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notes.notesgroup', verbose_name='Группа')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
            },
        ),
    ]