from rest_framework.permissions import BasePermission


class LessonPermissionsMixin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Super Admin'
