from django.forms import ModelForm
from .models import Teacher


class TeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'fathers_name', 'specialization', 'course_name']
