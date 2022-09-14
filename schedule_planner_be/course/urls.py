from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('<int:pk>/delete', CourseDeleteView.as_view(), name='course_confirm_delete'),
    path('<int:pk>/edit', CourseUpdateView.as_view(), name='course_edit'),
    path('new/', CourseCreateView.as_view(), name='course_form'),
    path('comment/<int:pk>/detail', CourseDetailView.as_view(), name='course_detail'),
    path('export/courses-list/', views.csv_courses_list_write, name='csv_courses_list_write'),
    path('comment/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment_detail'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_edit'),
    path('comment/new/', CommentCreateView.as_view(), name='comment_form'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_confirm_delete'),
    path('lesson/morning/', LessonMorningListView.as_view(), name='lesson_morning_list'),
    path('lesson/morning/filter/', FilterMorningLessonView.as_view(), name='morning_filter'),
    path('lesson/evening/', LessonEveningListView.as_view(), name='lesson_evening_list'),
    path('lesson/evening/filter/', FilterEveningLessonView.as_view(), name='evening_filter'),
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/filter/', FilterLessonView.as_view(), name='filter'),
    path('lesson/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    path('lesson/new/', LessonCreateView.as_view(), name='lesson_form'),
    path('lesson/<int:pk>/delete/', LessonDeleteView.as_view(), name='lesson_confirm_delete'),
    path('lesson/export/lessons-list/', views.csv_lessons_list_write, name='csv_lessons_list_write'),
    path('course-lessons/<int:pk>/', course_by_lessons, name='course_by_lessons'),
    path('schedule/<int:pk>/', comments_by_lesson, name='comments_by_lesson'),
    path('comments/<int:pk>/', comments_by_course, name='comments_by_course'),
]

