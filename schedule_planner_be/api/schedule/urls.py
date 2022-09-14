from django.urls import path
from . import views

urlpatterns = [
    path('', views.ScheduleListView.as_view()),
    path('<int:pk>/', views.ScheduleDetailsView.as_view()),
    #     # path('new/', views.UserCreateView.as_view()),
]
