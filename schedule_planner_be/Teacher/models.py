from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
import datetime


class Teacher(models.Model):
    """Преподаватели"""
    surname = models.CharField(_("Surname"), max_length=50, validators=[
        RegexValidator(
            regex="^[А-яа-я-\s]{1,50}$",
            message=_('Invalid surname'),
            code=_('invalid_surname')
        ),
    ])
    name = models.CharField(_("Name"), max_length=50, validators=[
        RegexValidator(
            regex="^[А-яа-я-\s]{1,50}$",
            message=_('Invalid name'),
            code=_('invalid_name')
        ),
    ])
    fathers_name = models.CharField(_("Middle name"), max_length=50, blank=True, validators=[
        RegexValidator(
            regex="^[А-яа-я-\s]{1,50}$",
            message=_("Invalid middle name"),
            code=_('invalid_middle_name')
        ),
    ])
    age = models.PositiveSmallIntegerField(_("Age"), default=0, blank=True)
    start_date = models.DateField(_('Start date of teaching'), blank=True, default=datetime.date.today)
    group_count = models.PositiveSmallIntegerField(_("Number of groups"), default=0, blank=True)
    specialization = models.CharField(_("Teacher Specialization"), max_length=250, validators=[
        RegexValidator(
            regex="^[-!#$%&'*+./=?^_`{}|~A-Za-zА-яа-я-\s]{1,250}$",
            message=_("Invalid specialization"),
            code=_('invalid_specialization')
        ),
    ], blank=True)
    COURSE_NAME = [('Управление и бизнес-анализ в сфере рзработки ПО',(
            ('Бизнес-анализ', 'Бизнес-анализ'),
            ('UML для бизнес-анализа', 'UML для бизнес-анализа'),
            ('Управление проектами', 'Управление проектами'),
            ('2 в 1 : Бизнес-анализ + управление проектами', '2 в 1 : Бизнес-анализ + управление проектами'),
            ('People Management', 'People Management'),
            ('Product Manager', 'Product Manager'),
            ('Agile', 'Agile'),
            )
    ),
    ('Сопровождение IT-бизнеса', (
        ('IT-юрист', 'IT-юрист'),
        ('IT-HR', 'IT-HR'),
        ('IT-Бухгалтер', 'IT-Бухгалтер'),
        ('Бухгалтерский учет для руководителей', 'Бухгалтерский учет для руководителей'),
        ('Бухгалтерский учет для ИП', 'Бухгалтерский учет для ИП'),
        )
    ),
    ('Разработка и тестирование ПО', (
        ('Тестирование ПО', 'Тестирование ПО'),
        ('Автоматизированное тестирование ПО на Java', 'Автоматизированное тестирование ПО на Java'),
        ('Основы разработки сайтов', 'Основы разработки сайтов'),
        ('UX/UI Дизайн для новичков', 'UX/UI Дизайн для новичков'),
        ('Java', 'Java'),
        ('Python', 'Python'),
        ('C#', 'C#'),
        ('Современный Front-end', 'Современный Front-end'),
        ('Искусственный интеллект', 'Искусственный интеллект'),
        ('SQL', 'SQL'),
        )
        ),
    ('Разработка игр', (
        ('Нарративный дизайн', 'Нарративный дизайн'),
        )
    ),
    ('Маркетинг и продажи', (
        ('Интернет-маркетинг', 'Интернет-маркетинг'),
        ('IT Sales', 'IT Sales'),
        ('Продвижение бизнеса в Telegram и Вконтакте', 'Продвижение бизнеса в Telegram и Вконтакте'),
        )
    ),
    ('Информацтонная безопасность и администрирование', (
        ('Информационная безопасность', 'Информационная безопасность'),
        ('DevOps. Системный инженер', 'DevOps. Системный инженер'),
        )
    ),
    ('Soft Skills', (
        ('Soft Skills', 'Soft Skills'),
        ('Управление командой в новых условиях', 'Управление командой в новых условиях'),
        )
    ),
    ('Курсы-интенсивы', (
        ('Войти в IT', 'Войти в IT'),
        ('Поиск и организация удаленной работы', 'Поиск и организация удаленной работы'),
        ('UML для бизнес-анализа', 'UML для бизнес-анализа'),
        ('Agile', 'Agile')
        )
    ),
    ('Стажировка', (
        ('Java', 'Java'),
        ('Python', 'Python'),
        ('Тестирование ПО', 'Тестирование ПО'),
        ('Бизнес-анализ', 'Бизнес-анализ'),
        ('IT-рекрутер', 'IT-рекрутер'),
        )
    ),
    ]
    course_name = MultiSelectField(_("Course name"), choices=COURSE_NAME, max_choices=7,
                                    max_length=60, default=None, blank=True)
    phone = models.CharField(_('Phone'), max_length=25, blank=True)
    image = models.ImageField(_("Photo"), upload_to='uploads/% Y/% m/% d/', blank=True)
    is_active = models.BooleanField(_('Status'), default=True)

    def __str__(self):
        return f"{self.surname} {self.name}"

    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = "teacher"
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"