from rest_framework.permissions import BasePermission


class ClassroomPermissionsMixin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Super Admin'
