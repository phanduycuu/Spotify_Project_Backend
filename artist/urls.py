from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet

router = DefaultRouter()
router.register(r'', ArtistViewSet, basename='artist')

urlpatterns = router.urls