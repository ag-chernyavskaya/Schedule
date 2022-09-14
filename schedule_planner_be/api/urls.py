from django.urls import path, include


urlpatterns = [
    path('', include('api.user.urls')),
    path('teachers/', include('api.teacher.urls')),
    path('courses/', include('api.course.urls')),
    path('locations/', include('api.location.urls')),
    path('classrooms/', include('api.classroom.urls')),
    path('subwaystations/', include('api.subwaystation.urls')),
    path('comments/', include('api.comment.urls')),
    path('lessons/', include('api.lesson.urls'))
]