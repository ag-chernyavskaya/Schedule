from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    DAYS_OF_WEEK = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
    )
    days_of_week = serializers.MultipleChoiceField(choices=DAYS_OF_WEEK)

    class Meta:
        model = Course
        fields = '__all__'
        validators = [UniqueTogetherValidator(
            queryset=Course.objects.all(),
            fields=['start_date', 'start_time', 'location']
        )]

    def create(self, validated_data):
        return Course.objects.create(**validated_data)
