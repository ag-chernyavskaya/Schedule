import itertools
from datetime import date, time, datetime
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from django_currentuser.db.models import CurrentUserField
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.db import models
from django.utils.datetime_safe import date
from django.core.validators import MaxValueValidator
from multiselectfield import MultiSelectField
from Teacher.models import Teacher
from User.models import User


class ClassroomAvailability(models.Model):
    date = models.DateField()
    classroom = models.CharField('Аудитория', max_length=100)
    start_time = models.CharField('Время начала занятия', max_length=5)
    is_free = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Все слоты аудитории'

    def __str__(self):
        return f"{self.date} {self.classroom} {self.start_time} {self.is_free}"


class Course(models.Model):
    """Creates model Course"""
    # prepopulated_fields = {"course_type": ("start_time", )}
    course_name = models.CharField("Course name", max_length=50)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField("Course start date", default=date.today)
    start_day_of_week = models.CharField("Start day of week", max_length=200, default="", blank=True,
                                         help_text="The field will be filled in automatically after saving")

    @property
    def start_day_isoweekday(self):
        """Returns start date day of the week"""
        dw1 = self.start_date.isoweekday()
        dct = {1: "Monday",
               2: "Tuesday",
               3: "Wednesday",
               4: "Thursday",
               5: "Friday",
               6: "Saturday",
               7: "Sunday",
               }
        return dct.get(dw1)

    DAYS_OF_WEEK = (
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
        (7, "Sunday"),
    )
    days_of_week = MultiSelectField("Days of the week", choices=DAYS_OF_WEEK, default="",
                                    max_choices=7, max_length=63, blank=True)

    LESSON_DURATION = (
        (1, 1),
        (2, 2),
        (3, 3),
    )
    lesson_duration = models.SmallIntegerField("Lesson duration", choices=LESSON_DURATION, null=True,
                                               blank=True, help_text="hour(s)")

    @property
    def all_course_days(self):
        """Returns all course days"""
        days_of_week = [float(item) for item in self.days_of_week]
        days_of_week_in_chosen_order = []
        for i in days_of_week:
            if i != self.start_day_isoweekday:
                days_of_week_in_chosen_order.append(int(i))
            if i == self.start_day_isoweekday:
                days_of_week_in_chosen_order.insert(0, int(i))
        all_course_days_days_of_week = []
        count = 1
        for i in itertools.cycle(days_of_week_in_chosen_order):
            if count > (self.number_of_lessons + 2):
                break
            all_course_days_days_of_week.append(i)
            count += 1
        all_course_days = []
        all_course_days.append(self.start_date)
        ind = 0
        for _ in all_course_days_days_of_week:
            if ind > self.number_of_lessons:
                break
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] > 0:
                days = all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind]
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] == -1:
                days = 6
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] == -2:
                days = 5
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] == -3:
                days = 4
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] == -4:
                days = 3
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] == -5:
                days = 2
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            if all_course_days_days_of_week[ind + 1] - all_course_days_days_of_week[ind] == -6:
                days = 1
                td = timedelta(days=days)
                all_course_days.append(all_course_days[ind] + td)
            ind += 1
        all_course_days = [i for i in all_course_days]
        return all_course_days

    location = models.ForeignKey("schedule.Classroom", on_delete=models.SET_NULL, null=True)

    START_TIME_OPTIONS = [
        ("08:00", "08:00"),
        ("09:00", "09:00"),
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("13:00", "13:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
        ("18:00", "18:00"),
        ("19:00", "19:00"),
        ("20:00", "20:00"),
        ("21:00", "21:00"),
    ]

    # @property
    # def start_time_options(self):
    #     # import pickle
    #     # location = self.location
    #     # lessons = Lesson.objects.filter(course__location=location).values('date', 'start_time')
    #     all_start_time_options = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00",
    #                               "17:00", "18:00", "19:00", "20:00", "21:00"]
    #     all_reserved_options = [str(item) for item in
    #                             Lesson.objects.filter(date=self.start_date, location=self.location)]
    #     # print(course)
    #     for a in all_reserved_options:
    #         for i in all_start_time_options:
    #             if i in a:
    #                 all_start_time_options.remove(i)
    #     # start_time_options = [(i, i) for i in all_start_time_options]
    #     start_time_options = [i for i in all_start_time_options]
    #     return start_time_options
    #     # return print(lessons)

    start_time_options = models.ForeignKey(ClassroomAvailability, on_delete=models.SET_NULL, null=True, default='',
                                           blank=True)
    # choices = models.CharField("Start time options", max_length=200, default="", null=True, blank=True)
    start_time = models.CharField("Start time", choices=START_TIME_OPTIONS, max_length=9)
    end_time = models.TimeField("End time", null=True, blank=True,
                                help_text="The field will be filled in automatically after saving")
    number_of_lessons = models.PositiveSmallIntegerField("Number of lessons", validators=[MaxValueValidator(50)])

    @property
    def find_end_time(self):
        start_time = self.start_time
        hour = int(start_time[:2])
        minute = int(start_time[3:])
        start_time_time = time(hour=hour, minute=minute)
        hours = float(self.lesson_duration)
        td = timedelta(hours=hours)
        end_time = (datetime.combine(date.today(), start_time_time) + td).time()
        return end_time

    @property
    def find_course_type(self):
        """Returns the course type"""
        morning_course = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
        evening_course = ["17:00", "18:00", "19:00", "20:00", "21:00"]
        if self.start_time in morning_course:
            return "Morning schedule"
        if self.start_time in evening_course:
            return "Evening schedule"

    course_type = models.CharField("Course type", max_length=16, blank=True, default="",
                                   help_text="The field will be filled in automatically after saving")

    # all_course_dates = models.CharField("All course days", max_length=200, blank=True, default="",
    #                                     help_text="The field will be filled in automatically after saving")
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.start_day_of_week = self.start_day_isoweekday
        self.course_type = self.find_course_type
        # self.choices = self.start_time_options
        self.all_course_dates = self.all_course_days
        self.end_time = self.find_end_time
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.course_name}, {self.start_date}, {self.start_time}, {self.location}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        unique_together = ('start_date', 'location', 'start_time')


@receiver(post_save, sender=Course)
def validate_days_of_week(sender, instance, **kwargs):
    course = instance
    if str(course.start_date.isoweekday()) not in course.days_of_week:
        raise ValidationError(
            _('Chosen days of week do not include start day of week'),
        )


@receiver(post_save, sender=Course)
def create_lessons(sender, instance, **kwargs):
    course = instance
    if Lesson.objects.filter(course=course):
        Lesson.objects.filter(course=course).delete()
    if not Lesson.objects.filter(course=course):
        teacher = course.teacher
        location = course.location
        start_time = course.start_time
        end_time = course.end_time
        number = 1
        for dates in course.all_course_days:
            index = course.all_course_days.index(dates)
            if number == len(course.all_course_dates) + 1:
                break
            else:
                if index == 0:
                    if course.lesson_duration == 1:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_start_day=True)
                    if course.lesson_duration == 2:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_start_day=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, for_time_slot=True)
                    if course.lesson_duration == 3:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_start_day=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, end_time=end_time,
                                                      for_time_slot=True)
                                start_time3 = start_time_range[start_time_range.index(i) + 2]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time3, for_time_slot=True)
                if index == len(course.all_course_dates) - 3:
                    if course.lesson_duration == 1:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_end_day=True)
                    if course.lesson_duration == 2:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_end_day=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, for_time_slot=True)
                    if course.lesson_duration == 3:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_end_day=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, end_time=end_time,
                                                      for_time_slot=True)
                                start_time3 = start_time_range[start_time_range.index(i) + 2]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time3, for_time_slot=True)
                if index == len(course.all_course_dates) - 2:
                    if course.lesson_duration == 1:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_transit_day_1=True)
                    if course.lesson_duration == 2:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_transit_day_1=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, for_time_slot=True)
                    if course.lesson_duration == 3:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_transit_day_1=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, end_time=end_time,
                                                      for_time_slot=True)
                                start_time3 = start_time_range[start_time_range.index(i) + 2]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time3, for_time_slot=True)
                if index == len(course.all_course_dates) - 1:
                    if course.lesson_duration == 1:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_transit_day_2=True)
                    if course.lesson_duration == 2:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_transit_day_2=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, for_time_slot=True)
                    if course.lesson_duration == 3:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time,
                                              is_transit_day_2=True)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, end_time=end_time,
                                                      for_time_slot=True)
                                start_time3 = start_time_range[start_time_range.index(i) + 2]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time3, for_time_slot=True)
                if dates in course.all_course_dates[1:len(course.all_course_dates) - 3]:
                    if course.lesson_duration == 1:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time)
                    if course.lesson_duration == 2:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, for_time_slot=True)
                    if course.lesson_duration == 3:
                        Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                              date=dates, start_time=start_time, end_time=end_time)
                        start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                                            "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
                        for i in start_time_range:
                            if i == course.start_time:
                                start_time2 = start_time_range[start_time_range.index(i) + 1]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time2, end_time=end_time,
                                                      for_time_slot=True)
                                start_time3 = start_time_range[start_time_range.index(i) + 2]
                                Lesson.objects.create(number=number, course=course, teacher=teacher, location=location,
                                                      date=dates, start_time=start_time3, for_time_slot=True)
                number += 1


class Comment(models.Model):
    """Creates model Comment"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default='')
    body = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created']

    def __str__(self):
        return f'{self.body}'


class Lesson(models.Model):
    """Создание модели занятия"""
    START_TIME_OPTIONS = [
        ("08:00", "08:00"),
        ("09:00", "09:00"),
        ("10:00", "10:00"),
        ("11:00", "11:00"),
        ("12:00", "12:00"),
        ("13:00", "13:00"),
        ("14:00", "14:00"),
        ("15:00", "15:00"),
        ("16:00", "16:00"),
        ("17:00", "17:00"),
        ("18:00", "18:00"),
        ("19:00", "19:00"),
        ("20:00", "20:00"),
        ("21:00", "21:00"),
    ]
    number = models.PositiveSmallIntegerField("Number")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    location = models.ForeignKey("schedule.Classroom", on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name="Преподаватель", on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    description = models.TextField("Description", blank=True)
    date = models.DateField("Date", default=date.today)
    start_time = models.CharField("Start time", choices=START_TIME_OPTIONS, max_length=9)
    end_time = models.TimeField("End time", null=True, blank=True)
    comment = models.ManyToManyField(Comment, blank=True, default=None)
    is_start_day = models.BooleanField(default=False, blank=True)
    is_end_day = models.BooleanField(default=False, blank=True)
    is_transit_day_1 = models.BooleanField(default=False, blank=True)
    is_transit_day_2 = models.BooleanField(default=False, blank=True)
    created_by = CurrentUserField()
    for_time_slot = models.BooleanField(default=False, blank=True)
    was_held = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"
        unique_together = ('location', 'date', 'start_time')

    def __str__(self):
        return f"{self.number} {self.course} {self.topic}"
