# posts/urls.py

from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet)  # Only one registration
router.register(r'comments', CommentViewSet)  # Ensure this is not duplicated
router.register(r'feed', FeedView)

urlpatterns = router.urls
