from django.forms import ModelForm
from .models import Schedule, Location, SubwayStation, Classroom


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'


class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = '__all__'


class SubwayStationForm(ModelForm):
    class Meta:
        model = SubwayStation
        fields = ['station', ]


class ClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'
