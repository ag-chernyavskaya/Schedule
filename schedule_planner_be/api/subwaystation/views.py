from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import viewsets, renderers

from User.models import User
from api.subwaystation.permissions import SubwayStationPermissionsMixin
from api.subwaystation.serializers import SubwayStationSerializer
from schedule.models import SubwayStation


class SubwayStationViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = SubwayStation.objects.all()
    serializer_class = SubwayStationSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated & SubwayStationPermissionsMixin]
        return [permission() for permission in permission_classes]





