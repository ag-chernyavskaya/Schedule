# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.ClassroomListView.as_view()),
#     path('<str:pk>/', views.ClassroomDetailView.as_view()),
#     path('new/', views.ClassroomCreateView.as_view()),
# ]

from django.urls import path
from rest_framework import renderers
from api.classroom.views import ClassroomViewSet

classroom_list = ClassroomViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
classroom_detail = ClassroomViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', classroom_list, name='classroom-list'),
    path('<int:pk>/', classroom_detail, name='classroom-detail'),
]
