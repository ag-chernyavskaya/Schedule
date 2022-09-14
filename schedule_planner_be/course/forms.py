from django.forms import ModelForm
from .models import Course, Lesson, Comment


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class LessonForm(ModelForm):
    class Meta:
        model = Lesson
        fields = '__all__'


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
