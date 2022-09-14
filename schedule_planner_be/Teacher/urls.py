from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', TeacherListView.as_view(), name='teacher_list'),
    path('delete/<int:pk>/', TeacherDeleteView.as_view(), name='teacher_confirm_delete'),
    path('edit/<int:pk>/', TeacherUpdateView.as_view(), name='teacher_edit'),
    path('new/', TeacherCreateView.as_view(), name='teacher_form'),
    path('<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
    path('export/teachers-list/', views.csv_teachers_list_write, name='csv_teachers_list_write'),
]
