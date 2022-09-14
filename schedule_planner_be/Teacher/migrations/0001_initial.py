# Generated by Django 4.1 on 2022-08-31 19:43

import datetime
import django.core.validators
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_surname', message='Write correct surname', regex='^[А-яа-я-\\s]{1,50}$')], verbose_name='Surname')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_name', message='Write correct name', regex='^[А-яа-я-\\s]{1,50}$')], verbose_name='Name')),
                ('fathers_name', models.CharField(blank=True, max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_fathers_name', message="Write correct father's name", regex='^[А-яа-я-\\s]{1,50}$')], verbose_name='Middle name')),
                ('age', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Age')),
                ('start_date', models.DateField(blank=True, default=datetime.date.today, verbose_name='Start date of teaching')),
                ('group_count', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Number of groups')),
                ('specialization', models.CharField(max_length=250, validators=[django.core.validators.RegexValidator(code='invalid_specialization', message='Write correct specialization', regex="^[-!#$%&'*+./=?^_`{}|~A-Za-zА-яа-я-\\s]{1,250}$")], verbose_name='Teacher Specialization')),
                ('course_name', multiselectfield.db.fields.MultiSelectField(choices=[('Управление и бизнес-анализ в сфере рзработки ПО', (('Бизнес-анализ', 'Бизнес-анализ'), ('UML для бизнес-анализа', 'UML для бизнес-анализа'), ('Управление проектами', 'Управление проектами'), ('2 в 1 : Бизнес-анализ + управление проектами', '2 в 1 : Бизнес-анализ + управление проектами'), ('People Management', 'People Management'), ('Product Manager', 'Product Manager'), ('Agile', 'Agile'))), ('Сопровождение IT-бизнеса', (('IT-юрист', 'IT-юрист'), ('IT-HR', 'IT-HR'), ('IT-Бухгалтер', 'IT-Бухгалтер'), ('Бухгалтерский учет для руководителей', 'Бухгалтерский учет для руководителей'), ('Бухгалтерский учет для ИП', 'Бухгалтерский учет для ИП'))), ('Разработка и тестирование ПО', (('Тестирование ПО', 'Тестирование ПО'), ('Автоматизированное тестирование ПО на Java', 'Автоматизированное тестирование ПО на Java'), ('Основы разработки сайтов', 'Основы разработки сайтов'), ('UX/UI Дизайн для новичков', 'UX/UI Дизайн для новичков'), ('Java', 'Java'), ('Python', 'Python'), ('C#', 'C#'), ('Современный Front-end', 'Современный Front-end'), ('Искусственный интеллект', 'Искусственный интеллект'), ('SQL', 'SQL'))), ('Разработка игр', (('Нарративный дизайн', 'Нарративный дизайн'),)), ('Маркетинг и продажи', (('Интернет-маркетинг', 'Интернет-маркетинг'), ('IT Sales', 'IT Sales'), ('Продвижение бизнеса в Telegram и Вконтакте', 'Продвижение бизнеса в Telegram и Вконтакте'))), ('Информацтонная безопасность и администрирование', (('Информационная безопасность', 'Информационная безопасность'), ('DevOps. Системный инженер', 'DevOps. Системный инженер'))), ('Soft Skills', (('Soft Skills', 'Soft Skills'), ('Управление командой в новых условиях', 'Управление командой в новых условиях'))), ('Курсы-интенсивы', (('Войти в IT', 'Войти в IT'), ('Поиск и организация удаленной работы', 'Поиск и организация удаленной работы'), ('UML для бизнес-анализа', 'UML для бизнес-анализа'), ('Agile', 'Agile'))), ('Стажировка', (('Java', 'Java'), ('Python', 'Python'), ('Тестирование ПО', 'Тестирование ПО'), ('Бизнес-анализ', 'Бизнес-анализ'), ('IT-рекрутер', 'IT-рекрутер')))], default=None, max_length=60, verbose_name='Course name')),
                ('phone', models.CharField(blank=True, max_length=25, verbose_name='Phone')),
                ('image', models.ImageField(blank=True, upload_to='Teachers/', verbose_name='Photo')),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
            ],
            options={
                'verbose_name': 'Преподаватель',
                'verbose_name_plural': 'Преподаватели',
                'db_table': 'teacher',
            },
        ),
    ]
