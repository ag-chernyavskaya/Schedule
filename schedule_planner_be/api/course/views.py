import csv

from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, viewsets, renderers, generics
from api.course.serializers import CourseSerializer
from course.models import Course
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import CoursePermissionsMixin


class CourseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    Additionally we also provide an extra `highlight` action.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & CoursePermissionsMixin]
        return [permission() for permission in permission_classes]


def csv_courses_list_write(request):
    """""Create a CSV file with teachers list"""
    # Get all data from Teacher Database Table
    courses = Course.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses_list.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';', dialect='excel')
    writer.writerow(['id', 'Название курса', 'Преподаватель', 'Дата старта', 'Время начала', 'Кол-во уроков'])

    for course in courses:
        writer.writerow([course.id, course.course_name, course.teacher, course.start_date, course. start_time,
                         course.number_of_lessons])

    return response
