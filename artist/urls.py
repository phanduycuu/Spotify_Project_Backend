from django.urls import path
from .views import ArtistListCreate, ArtistRetrieveUpdateDestroy

urlpatterns = [
    path('', ArtistListCreate.as_view()),
    path('<int:pk>/', ArtistRetrieveUpdateDestroy.as_view()),
]