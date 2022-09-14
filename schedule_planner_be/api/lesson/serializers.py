from rest_framework import serializers
from course.models import Lesson


class LessonListSerializer(serializers.ModelSerializer):
    """Список занятий"""
    class Meta:
        model = Lesson
        fields = ('id', 'date', 'topic')


class LessonDetailSerializer(serializers.ModelSerializer):
    """Полное описание занятия, добавление, изменение и удаление преподавателя"""
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
    start_time = serializers.MultipleChoiceField(choices=START_TIME_OPTIONS)

    class Meta:
        model = Lesson
        fields = '__all__'

