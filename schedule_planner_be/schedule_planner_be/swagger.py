from django.urls import path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


schema_view = get_schema_view(title='BelHard schedule API')

urlpatterns = [
    path('api_schema/', schema_view, name='api_schema'),
    path('swagger-ui/', TemplateView.as_view(template_name='docs.html',
                                             extra_context={'schema_url':'api_schema'}),
         name='swagger-ui')
]