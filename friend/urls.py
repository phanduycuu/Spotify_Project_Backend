from rest_framework.routers import DefaultRouter
from .views import FriendViewSet

router = DefaultRouter()
router.register(r'', FriendViewSet, basename='friend')

urlpatterns = router.urls