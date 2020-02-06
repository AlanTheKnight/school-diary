# Generated by Django 3.0.2 on 2020-02-06 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0008_auto_20200206_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='account_type',
            field=models.IntegerField(choices=[(0, 'Root'), (1, 'Администратор'), (2, 'Учитель'), (3, 'Ученик')], default=3, verbose_name='Тип аккаунта'),
        ),
    ]