from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet,AuthViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'', AccountViewSet)
router.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
