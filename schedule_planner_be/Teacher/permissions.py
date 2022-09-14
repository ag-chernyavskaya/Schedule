from django.contrib.auth.mixins import AccessMixin
from django.http import Http404


class TeacherPermissionsMixin(AccessMixin):
    def has_permissions(self):
        return self.request.user.role == 'Super Admin'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise Http404
        return super().dispatch(request, *args, **kwargs)
