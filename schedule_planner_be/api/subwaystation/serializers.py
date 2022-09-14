from rest_framework import serializers
from schedule.models import SubwayStation


class SubwayStationSerializer(serializers.ModelSerializer):
    """Список курсов"""
    class Meta:

        model = SubwayStation
        fields = '__all__'

    def create(self, validated_data):
        return SubwayStation.objects.create(**validated_data)

