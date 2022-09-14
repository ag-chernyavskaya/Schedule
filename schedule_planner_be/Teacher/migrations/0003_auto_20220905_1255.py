# Generated by Django 3.2.15 on 2022-09-05 09:55

import django.core.validators
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0002_alter_teacher_fathers_name_alter_teacher_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='course_name',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Управление и бизнес-анализ в сфере рзработки ПО', (('Бизнес-анализ', 'Бизнес-анализ'), ('UML для бизнес-анализа', 'UML для бизнес-анализа'), ('Управление проектами', 'Управление проектами'), ('2 в 1 : Бизнес-анализ + управление проектами', '2 в 1 : Бизнес-анализ + управление проектами'), ('People Management', 'People Management'), ('Product Manager', 'Product Manager'), ('Agile', 'Agile'))), ('Сопровождение IT-бизнеса', (('IT-юрист', 'IT-юрист'), ('IT-HR', 'IT-HR'), ('IT-Бухгалтер', 'IT-Бухгалтер'), ('Бухгалтерский учет для руководителей', 'Бухгалтерский учет для руководителей'), ('Бухгалтерский учет для ИП', 'Бухгалтерский учет для ИП'))), ('Разработка и тестирование ПО', (('Тестирование ПО', 'Тестирование ПО'), ('Автоматизированное тестирование ПО на Java', 'Автоматизированное тестирование ПО на Java'), ('Основы разработки сайтов', 'Основы разработки сайтов'), ('UX/UI Дизайн для новичков', 'UX/UI Дизайн для новичков'), ('Java', 'Java'), ('Python', 'Python'), ('C#', 'C#'), ('Современный Front-end', 'Современный Front-end'), ('Искусственный интеллект', 'Искусственный интеллект'), ('SQL', 'SQL'))), ('Разработка игр', (('Нарративный дизайн', 'Нарративный дизайн'),)), ('Маркетинг и продажи', (('Интернет-маркетинг', 'Интернет-маркетинг'), ('IT Sales', 'IT Sales'), ('Продвижение бизнеса в Telegram и Вконтакте', 'Продвижение бизнеса в Telegram и Вконтакте'))), ('Информацтонная безопасность и администрирование', (('Информационная безопасность', 'Информационная безопасность'), ('DevOps. Системный инженер', 'DevOps. Системный инженер'))), ('Soft Skills', (('Soft Skills', 'Soft Skills'), ('Управление командой в новых условиях', 'Управление командой в новых условиях'))), ('Курсы-интенсивы', (('Войти в IT', 'Войти в IT'), ('Поиск и организация удаленной работы', 'Поиск и организация удаленной работы'), ('UML для бизнес-анализа', 'UML для бизнес-анализа'), ('Agile', 'Agile'))), ('Стажировка', (('Java', 'Java'), ('Python', 'Python'), ('Тестирование ПО', 'Тестирование ПО'), ('Бизнес-анализ', 'Бизнес-анализ'), ('IT-рекрутер', 'IT-рекрутер')))], default=None, max_length=60, verbose_name='Course name'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='specialization',
            field=models.CharField(blank=True, max_length=250, validators=[django.core.validators.RegexValidator(code='invalid_specialization', message='Invalid specialization', regex="^[-!#$%&'*+./=?^_`{}|~A-Za-zА-яа-я-\\s]{1,250}$")], verbose_name='Teacher Specialization'),
        ),
    ]