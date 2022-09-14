from django.urls import path
from rest_framework import renderers
from api.subwaystation.views import SubwayStationViewSet

subwaystation_list = SubwayStationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
subwaystation_detail = SubwayStationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', subwaystation_list, name='subwaystation-list'),
    path('<int:pk>/', subwaystation_detail, name='subwaystation-detail'),
]
