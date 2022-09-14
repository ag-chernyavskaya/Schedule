from rest_framework import generics
from api.schedule.serializer import ScheduleListSerializer
from schedule.models import Schedule


class ScheduleListView(generics.ListAPIView):
    """Вывод списка расписания"""
    serializer_class = ScheduleListSerializer

    def get_queryset(self):
        schedules = Schedule.objects.all()
        return schedules


class ScheduleDetailsView(generics.RetrieveAPIView):
    """Вывод полного описания курса"""
    queryset = Schedule.objects.filter()
    serializer_class = ScheduleListSerializer

# class CourseCreateView(generics.CreateAPIView):
#     """Добавление курса"""
#     serializer_class = CourseCreateSerializer
