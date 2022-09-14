from rest_framework import serializers
from schedule.models import Schedule


class ScheduleListSerializer(serializers.ModelSerializer):
    """Список курсов"""
    class Meta:

        model = Schedule
        fields = '__all__'
