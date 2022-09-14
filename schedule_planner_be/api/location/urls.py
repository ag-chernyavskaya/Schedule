from rest_framework.routers import SimpleRouter
from api.location.views import LocationViewSet


router = SimpleRouter()
router.register('', LocationViewSet)
urlpatterns = router.urls
