# Generated by Django 3.1.7 on 2021-03-23 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AverageValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weights_x_values', models.IntegerField(verbose_name='Сумма произведений весов и значений оценок')),
                ('weights_sum', models.IntegerField(verbose_name='Сумма весов оценок')),
                ('grades_number', models.IntegerField(verbose_name='Количество оценок')),
                ('grades_sum', models.IntegerField(verbose_name='Сумма значений оценок')),
                ('missed', models.IntegerField(default=0, verbose_name='Количество пропущенных уроков')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='average', to='core.students')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subjects')),
            ],
            options={
                'verbose_name': 'Данные об оценках учеников',
                'unique_together': {('student', 'subject')},
            },
        ),
    ]