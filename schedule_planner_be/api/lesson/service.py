from django_filters import rest_framework as filters, DateFromToRangeFilter
from course.models import Lesson


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class LessonFilter(filters.FilterSet):
    """Фильтрация по имени курса, учителю, локации, дате"""
    date = DateFromToRangeFilter(field_name='date')

    class Meta:
        model = Lesson
        fields = ['course', 'teacher', 'course__location', 'date']


class LessonTeacherFilter(filters.FilterSet):
    """Фильтрация по имени курса, учителю"""

    class Meta:
        model = Lesson
        fields = ['course', 'teacher']