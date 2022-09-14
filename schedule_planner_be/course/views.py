import csv
import datetime
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from .models import Course, Comment, Lesson
from Teacher.models import Teacher
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .permissions import LessonPermissionsMixin
from .forms import LessonForm, CommentForm
from django.urls import reverse_lazy


class CourseListView(ListView):
    """Вывод списка курсов"""
    model = Course
    template_name = 'course/course_list.html'


class CourseDetailView(DetailView):
    """Вывод полного описания курса"""
    model = Course
    template_name = 'course/course_detail.html'


class CourseCreateView(CreateView):
    """Создание нового курса"""
    model = Course
    template_name = 'course/course_form.html'
    fields = '__all__'
    success_url = reverse_lazy('course_list')


class CourseUpdateView(UpdateView):
    """Изменение курса"""
    model = Course
    template_name = 'course/course_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('course_detail', args=(self.object.id,))


class CourseDeleteView(DeleteView):
    """Удаление курса"""
    model = Course
    template_name = 'course/course_confirm_delete.html'
    fields = '__all__'
    success_url = reverse_lazy('course_list')


class CommentListView(ListView):
    """Вывод списка комментариев"""
    model = Comment
    template_name = 'course/comment_list.html'


class CommentCreateView(CreateView):
    """Создание нового комментария"""
    template_name = 'course/comment_form.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('comment_detail', args=(self.object.id,))


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    """Удаление комментария"""
    template_name = 'course/comment_confirm_delete.html'
    model = Comment
    success_url = reverse_lazy('comment_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    """Изменение курса"""
    model = Comment
    template_name = 'course/comment_edit.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('comment_detail', args=(self.object.id,))

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class CommentDetailView(DetailView):
    """Вывод полного описания курса"""
    model = Comment
    template_name = 'course/comment_detail.html'


class GetValuesFoFilters:
    """Получение всех полей фильтрации"""

    def get_teacher(self):
        return Teacher.objects.filter(is_active=True).values('surname')

    def get_course(self):
        return Course.objects.all().values('course_name')

    def get_morning_course(self):
        return Course.objects.filter(course_type='Morning schedule').values('course_name')

    def get_evening_course(self):
        return Course.objects.filter(course_type='Evening schedule').values('course_name')

    def get_morning_location(self):
        return Course.objects.filter(course_type='Morning schedule').values('location__location__street').distinct()

    def get_evening_location(self):
        return Course.objects.filter(course_type='Evening schedule').values('location__location__street').distinct()

    # def get_date(self):
    #     return Lesson.objects.all().get.values('data')


class LessonListView(LoginRequiredMixin, GetValuesFoFilters, ListView):
    """Вывод списка занятий"""
    model = Lesson, Comment
    template_name = 'course/lesson_list.html'

    def get_queryset(self):
        queryset = Lesson.objects.all().filter(for_time_slot=False)
        return queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['lesson_list'] = Lesson.objects.all().filter(for_time_slot=False)
    #     context['comments'] = Comment.objects.all()
    #     return context


class LessonMorningListView(LoginRequiredMixin, GetValuesFoFilters, ListView):
    """Вывод утренних занятий"""
    model = Lesson
    template_name = 'course/lesson_morning_list.html'

    def get_queryset(self):
        morning_lessons = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
        queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons)
        return queryset


class LessonEveningListView(LoginRequiredMixin, GetValuesFoFilters, ListView):
    """Вывод вечерних занятий"""
    model = Lesson
    template_name = 'course/lesson_evening_list.html'

    def get_queryset(self):
        evening_lessons = ["17:00", "18:00", "19:00", "20:00", "21:00"]
        queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons)
        return queryset


class LessonDetailView(LoginRequiredMixin, DetailView):
    """Вывод полного описания зантятия"""
    model = Lesson
    template_name = 'course/lesson_detail.html'


class LessonCreateView(LoginRequiredMixin, LessonPermissionsMixin, CreateView):
    """Создание нового занятия"""
    model = Lesson
    template_name = 'course/lesson_form.html'
    form_class = LessonForm
    success_url = "/courses/lesson/"


class LessonUpdateView(LoginRequiredMixin, LessonPermissionsMixin, UpdateView):
    """Изменение занятия"""
    model = Lesson
    template_name = 'course/lesson_edit.html'
    fields = '__all__'
    success_url = "/courses/lesson/"


class LessonDeleteView(LoginRequiredMixin, LessonPermissionsMixin, DeleteView):
    """Удаление занятия"""
    model = Lesson
    template_name = 'course/lesson_confirm_delete.html'
    fields = '__all__'
    success_url = "/courses/lesson/"


class FilterLessonView(LoginRequiredMixin, GetValuesFoFilters, ListView):
    """Фильтр занятий"""
    template_name = 'course/lesson_list.html'

    def get_queryset(self):
        surname = self.request.GET.getlist("surname")
        course_name = self.request.GET.getlist("course_name")
        if surname and course_name:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(
                Q(teacher__surname__in=self.request.GET.getlist("surname")) &
                Q(course__course_name__in=self.request.GET.getlist("course_name"))
            )
            return queryset
        else:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(
                Q(teacher__surname__in=self.request.GET.getlist("surname")) |
                Q(course__course_name__in=self.request.GET.getlist("course_name"))
            )
            return queryset


class FilterMorningLessonView(LoginRequiredMixin, GetValuesFoFilters, ListView):
    """Фильтр утренних занятий"""
    template_name = 'course/lesson_morning_list.html'

    def get_queryset(self):
        surname = self.request.GET.getlist("surname")
        course_name = self.request.GET.getlist("course_name")
        location = self.request.GET.getlist("location")
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")
        morning_lessons = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
        if surname and course_name and location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif surname and course_name and location:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location)
            )
            return queryset
        elif surname and course_name and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif surname and location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name) &
                Q(date__range=(start, end))
            )
            return queryset
        elif course_name and location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif surname and course_name:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name)
            )
            return queryset
        elif surname and location:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__location__location__street__in=location)
            )
            return queryset
        elif surname and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(date__range=(start, end))
            )
            return queryset
        elif course_name and location:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location)
            )
            return queryset
        elif course_name and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(course__course_name__in=course_name) &
                Q(date__range=(start, end))
            )
            return queryset
        elif location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(date__range=(start, end))
            )
            return queryset
        else:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=morning_lessons).filter(
                Q(teacher__surname__in=surname) |
                Q(course__course_name__in=course_name) |
                Q(course__location__location__street__in=location)
            )
            return queryset


class FilterEveningLessonView(LoginRequiredMixin, GetValuesFoFilters, ListView):
    """Фильтр вечерних занятий"""
    template_name = 'course/lesson_evening_list.html'

    def get_queryset(self):
        surname = self.request.GET.getlist("surname")
        course_name = self.request.GET.getlist("course_name")
        location = self.request.GET.getlist("location")
        start = self.request.GET.get("start")
        end = self.request.GET.get("end")
        evening_lessons = ["17:00", "18:00", "19:00", "20:00", "21:00"]
        if surname and course_name and location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif surname and course_name and location:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location)
            )
            return queryset
        elif surname and course_name and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif surname and location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name) &
                Q(date__range=(start, end))
            )
            return queryset
        elif course_name and location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif surname and course_name:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__course_name__in=course_name)
            )
            return queryset
        elif surname and location:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(course__location__location__street__in=location)
            )
            return queryset
        elif surname and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) &
                Q(date__range=(start, end))
            )
            return queryset
        elif course_name and location:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(course__course_name__in=course_name) &
                Q(course__location__location__street__in=location)
            )
            return queryset
        elif course_name and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(course__course_name__in=course_name) &
                Q(date__range=(start, end))
            )
            return queryset
        elif location and start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(course__location__location__street__in=location) &
                Q(date__range=(start, end))
            )
            return queryset
        elif start and end:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(date__range=(start, end))
            )
            return queryset
        else:
            queryset = Lesson.objects.all().filter(for_time_slot=False).filter(start_time__in=evening_lessons).filter(
                Q(teacher__surname__in=surname) |
                Q(course__course_name__in=course_name) |
                Q(course__location__location__street__in=location)
            )
            return queryset


def csv_courses_list_write(request):
    """""Create a CSV file with teachers list"""
    # Get all data from Teacher Database Table
    courses = Course.objects.all()

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="courses_list.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';', dialect='excel')
    writer.writerow(['Название курса', 'Преподаватель', "Локация", 'Дата старта', 'Время начала', 'Кол-во уроков'])

    for course in courses:
        writer.writerow([course.course_name, course.teacher, course.location, course.start_date, course.start_time,
                         course.number_of_lessons])

    return response


def csv_lessons_list_write(request):
    """""Create a CSV file with teachers list"""
    # Get all data from Lesson Database Table
    lessons = Lesson.objects.filter(for_time_slot=False)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lessons_list.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';', dialect='excel')
    writer.writerow(['Номер занятия в курсе', 'Курс', 'Преподаватель', 'Тема занятия', 'Краткое описание',
                     'Дата занятия', 'Время занятия', 'Комментарий'])

    for lesson in lessons:
        writer.writerow([lesson.number, lesson.course.course_name, lesson.teacher, lesson.topic, lesson.description,
                         lesson.date, lesson.start_time, lesson.comment])

    return response


def course_by_lessons(request, pk):
    lesson_list = Lesson.objects.filter(course=pk)
    current_course = Course.objects.get(pk=pk)
    context = {'lesson_list': lesson_list, 'current_course': current_course}
    return render(request, 'course/course_by_lessons.html', context)


def comments_by_lesson(request, pk):
    comment_list = Comment.objects.filter(lesson=pk)
    current_lesson = Lesson.objects.get(pk=pk)
    context = {'comment_list': comment_list, 'current_lesson': current_lesson}
    return render(request, 'course/comments_by_lesson.html', context)


def comments_by_course(request, pk):
    comment_list = Comment.objects.filter(course=pk)
    current_course = Course.objects.get(pk=pk)
    context = {'comment_list': comment_list, 'current_course': current_course}
    return render(request, 'course/comments_by_lesson.html', context)
