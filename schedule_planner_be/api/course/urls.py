from django.urls import path
from rest_framework import renderers
from api.course.views import CourseViewSet
from . import views

course_list = CourseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
course_detail = CourseViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', course_list, name='course-list'),
    path('<int:pk>/', course_detail, name='course-detail'),
    path('export/courses-list/', views.csv_courses_list_write, name='csv_courses_list_write'),
]
