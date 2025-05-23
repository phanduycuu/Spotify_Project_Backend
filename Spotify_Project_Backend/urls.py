"""
URL configuration for Spotify_Project_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings  # Import settings
from django.conf.urls.static import static  # Import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('api/albums/', include('album.urls')),
    path('api/videos/', include('video.urls')),
    path('api/artists/', include('artist.urls')),
    path('api/singers/', include('singer.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account/', include('account.urls')),
    path('api/roles/', include('role.urls')),
    path('api/favourite-albums/', include('favourite_album.urls')),
    path('api/favourite-songs/', include('favourite_song.urls')),
    path('api/', include('chat.urls')),
    path('api/client/songs/', include('songClient.urls')),  # API cho client
    path('api/songs/', include('song.urls')),
    path('api/album-songs/', include('album_song.urls')),
    path('api/album-users/', include('album_user.urls')),
    path('api/friends/', include('friend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
