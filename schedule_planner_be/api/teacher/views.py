from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import *
from Teacher.models import Teacher
from .permissions import TeacherPermissionsMixin
from rest_framework.permissions import IsAuthenticated


class TeacherListView(generics.ListAPIView):
    """Вывод списка преподавателей"""
    serializer_class = TeacherListSerializer
    queryset = Teacher.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]


class TeacherDetailsView(generics.RetrieveAPIView):
    """Вывод полного описания преподавателя"""
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherDetailSerializer
    permission_classes = [IsAuthenticated & TeacherPermissionsMixin]


class TeacherCreateView(generics.CreateAPIView):
    """Добавление преподавателя"""
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherDetailSerializer
    permission_classes = [IsAuthenticated & TeacherPermissionsMixin]


class TeacherUpdateView(generics.UpdateAPIView):
    """Изменение преподавателя"""
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherUpdateSerializer
    permission_classes = [IsAuthenticated & TeacherPermissionsMixin]


class TeacherDeleteView(generics.DestroyAPIView):
    """Изменение статуса преподавателя на неактивный"""
    queryset = Teacher.objects.filter(is_active=True)
    serializer_class = TeacherDetailSerializer
    permission_classes = [IsAuthenticated & TeacherPermissionsMixin]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.save()
