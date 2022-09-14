# Generated by Django 3.2.15 on 2022-09-07 07:15

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20220907_1015'),
        ('course', '0003_auto_20220905_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='all_course_dates',
        ),
        migrations.RemoveField(
            model_name='course',
            name='choices',
        ),
        migrations.RemoveField(
            model_name='course',
            name='url',
        ),
        migrations.AddField(
            model_name='lesson',
            name='for_time_slot',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='course',
            name='days_of_week',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default='', max_length=63, verbose_name='Days of the week'),
        ),
        migrations.CreateModel(
            name='ClassroomAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.CharField(max_length=5, verbose_name='Время начала занятия')),
                ('is_free', models.BooleanField(default=True)),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.classroom')),
            ],
            options={
                'verbose_name_plural': 'Все слоты аудитории',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='start_time_options',
            field=models.ForeignKey(blank='', default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='course.classroomavailability'),
        ),
    ]
