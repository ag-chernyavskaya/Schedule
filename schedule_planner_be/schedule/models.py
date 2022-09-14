from datetime import time, datetime, timedelta, date
import time
# import pytz

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
# from django_agenda.models import AbstractTimeSlot, AbstractAvailabilityOccurrence, AbstractAvailability, AbstractBooking
# from django_agenda.time_span import TimeSpan

# from User.models import User
from User.models import User
from course.models import Course, Comment, Lesson, ClassroomAvailability


# from schedule_planner_be import settings


class SubwayStation(models.Model):
    """Creates model Subway station"""
    station = models.CharField('Subway station', max_length=50, default=None)

    def __str__(self):
        return f"с/м {self.station}"

    class Meta:
        verbose_name = 'Станция метро'
        verbose_name_plural = 'Станции метро'


class Location(models.Model):
    """"Creates model Location"""
    city = models.CharField('City', max_length=50)
    street = models.CharField('Street', max_length=50)
    building = models.CharField('Building', max_length=10, default=None)
    subway = models.ForeignKey(SubwayStation, on_delete=models.SET_NULL, null=True, verbose_name='Станции метро')

    def __str__(self):
        return f"{self.street}, {self.building}, {self.subway}, {self.city}"

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'


class Classroom(models.Model):
    """Creates model Classroom"""
    classroom = models.CharField('Classroom', max_length=10)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    seats_number = models.PositiveSmallIntegerField("Number of seats")
    pc_number = models.PositiveSmallIntegerField("Number of PCs")

    def __str__(self):
        return f"ауд. {self.classroom}, {self.location}"

    class Meta:
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        unique_together = ('classroom', 'location')


# class Availability(AbstractAvailability):
#     class AgendaMeta:
#         schedule_model = Classroom
#         schedule_field = "classroom"  # optional


# class AvailabilityOccurrence(AbstractAvailabilityOccurrence):
#     class AgendaMeta:
#         availability_model = Availability
#         schedule_model = Classroom
#         schedule_field = "classroom"  # optional
#
#
# class TimeSlot(AbstractTimeSlot):
#     class AgendaMeta:
#         availability_model = Availability
#         schedule_model = Classroom
#         booking_model = "ClassroomReservation"  # booking class, more details shortly
#         schedule_field = "classroom"  # optional


# class ClassroomReservation(AbstractBooking):
#     class AgendaMeta:
#         schedule_model = Classroom
#
#     owner = models.ForeignKey(
#         to=settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#         related_name="reservations",
#     )
#     start_time = models.DateTimeField(db_index=True)
#     end_time = models.DateTimeField(db_index=True)
#     approved = models.BooleanField(default=False)
#
#     def get_reserved_spans(self):
#         # we only reserve the time if the reservation has been approved
#         if self.approved:
#             yield TimeSpan(self.start_time, self.end_time)


# @receiver(post_save, sender=Classroom)
# def classroom_availability(sender, instance, **kwargs):
#     start_range_date = date(2022, 9, 1)
#     number_of_days = 365
#     date_list = []
#     for day in range(number_of_days):
#         a_date = (start_range_date + timedelta(days=day)).isoformat()
#         date_list.append(a_date)
#     start_time = time(8)
#     end_time = time(22)
#     tz = pytz.timezone("Europe/Minsk")
#     classroom = instance
#     for item in date_list:
#         # available from 8 AM to 22 PM
#         Availability.objects.create(
#             classroom=classroom,
#             start_date=item,
#             start_time=start_time,
#             end_time=end_time,
#             timezone=tz,
#         )


class Schedule(models.Model):
    """Создание модели Расписание"""

    title = models.TextField(default=None)
    courses = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='Курсы')
    locations = models.ForeignKey(Location, on_delete=models.DO_NOTHING, verbose_name='Локации')
    reviews = models.ForeignKey(Comment, on_delete=models.DO_NOTHING, verbose_name='Комментарии')
    url = models.SlugField(max_length=160, unique=True, default=None)

    def get_absolute_url(self):
        return reverse('course-detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.courses}"

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


# class ClassroomAvailability(models.Model):
#     date = models.DateField()
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     start_time = models.CharField('Время начала занятия', max_length=5)
#     is_free = models.BooleanField(default=True)
#
#     class Meta:
#         verbose_name_plural = 'Все слоты аудитории'
#
#     def __str__(self):
#         return f"{self.date} {self.classroom} {self.start_time} {self.is_free}"


@receiver(post_save, sender=Classroom)
def classroom_availability(sender, instance, **kwargs):
    start_range_date = date(2022, 9, 1)
    number_of_days = 90
    date_list = []
    for day in range(number_of_days):
        a_date = (start_range_date + timedelta(days=day)).isoformat()
        date_list.append(a_date)
    classroom = instance
    start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
                        "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
    for item in date_list:
        for start_time_option in start_time_range:
            # available from 8 AM to 22 PM
            ClassroomAvailability.objects.create(
                classroom=classroom,
                date=item,
                start_time=start_time_option,
            )


@receiver(post_save, sender=Lesson)
def reserve_classroom(sender, instance, **kwargs):
    lesson = instance
    date = lesson.date
    classroom = lesson.location
    print(classroom)
    start_time = lesson.start_time
    slot = ClassroomAvailability.objects.filter(date=date, classroom=classroom, start_time=start_time)
    print(slot)
    slot.update(is_free=False)
    print(slot)


@receiver(post_save, sender=Lesson)
def delete_old_classroomavailabilities(sender, instance, **kwargs):
    today = date.today()
    ClassroomAvailability.objects.filter(date__lt=today).delete()


@receiver(post_delete, sender=Lesson)
def make_classroomavailability_free(sender, instance, **kwargs):
    lesson = instance
    date = lesson.date
    classroom = lesson.location
    start_time = lesson.start_time
    slot = ClassroomAvailability.objects.filter(date=date, classroom=classroom, start_time=start_time)
    slot.update(is_free=True)


@receiver(post_delete, sender=Classroom)
def delete_classroomavailibility(sender, instance, **kwargs):
    classroom = instance
    location = classroom.location
    classroom = classroom.classroom
    address = f'ауд. {classroom}, {location}'
    ClassroomAvailability.objects.filter(classroom=address).delete()

# @receiver(post_save, sender=Lesson)
# def create_classroomreservation(sender, instance, **kwargs):
#     lesson = instance
#     user = lesson.created_by
#     print(user)
#     year = lesson.date.year
#     print(year, type(year))
#     month = lesson.date.month
#     day = lesson.date.day
#     print(day, type(day))
#     start_hour = int(lesson.start_time[:2])
#     print(start_hour, type(start_hour))
#     end_hour = lesson.end_time.hour
#     print(end_hour, type(end_hour))
#     tz = pytz.timezone("Europe/Minsk")
#     reservation = ClassroomReservation(
#         owner=user,
#         start_time=datetime(year=year, month=month, day=day, hour=start_hour, tzinfo=tz),
#         end_time=datetime(year=year, month=month, day=day, hour=end_hour, tzinfo=tz),
#     )
#     print(reservation, type(reservation))
#     reservation.clean()
#     reservation.save()


# def update():
#     while True:
#         now = datetime.now()
#         td = timedelta(days=1)
#         date = now + td
#         if now.hour == 10 and now.minute == 34:
#             all_classrooms = [classroom for classroom in Classroom.objects.all()]
#             print(all_classrooms)
#             for classroom in all_classrooms:
#                 start_time_range = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
#                                     "16:00", "17:00", "18:00", "19:00", "20:00", "21:00"]
#                 for start_time_option in start_time_range:
#                     ClassroomAvailability.objects.create(
#                         classroom=classroom,
#                         date=date,
#                         start_time=start_time_option,
#                     )
#             time.sleep(24 * 60 * 60 - 120)
#         else:
#             time.sleep(15)
