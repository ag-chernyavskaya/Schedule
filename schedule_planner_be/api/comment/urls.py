from rest_framework.routers import SimpleRouter
from api.comment.views import CommentViewSet

router = SimpleRouter()
router.register('', CommentViewSet)
urlpatterns = router.urls
