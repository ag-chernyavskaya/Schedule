# Generated by Django 3.2.15 on 2022-09-09 07:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'The email has been already registered. Please, sign in using this email'}, help_text='Enter email in format example@gmail.ru', max_length=150, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_email', message='Invalid email', regex="^([A-Za-z0-9]{1}[-!#$%&'*+./=?^_`{}|~A-Za-z0-9]{1,63})@([A-za-z0-9]{1,}\\.){1,2}[A-za-z0-9-]{2,63}$")], verbose_name='Email'),
        ),
    ]