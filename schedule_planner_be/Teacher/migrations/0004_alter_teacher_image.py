# Generated by Django 3.2.15 on 2022-09-09 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teacher', '0003_auto_20220905_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(blank=True, upload_to='uploads/% Y/% m/% d/', verbose_name='Photo'),
        ),
    ]
