from django.urls import path
from .views import AlbumListCreate, AlbumRetrieveUpdateDestroy

urlpatterns = [
    path('', AlbumListCreate.as_view()),
    path('<int:pk>/', AlbumRetrieveUpdateDestroy.as_view()),
]