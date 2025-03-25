from django.urls import path
from .views import VideoListCreate, VideoRetrieveUpdateDestroy

urlpatterns = [
    path('', VideoListCreate.as_view()),
    path('<int:pk>/', VideoRetrieveUpdateDestroy.as_view()),
]