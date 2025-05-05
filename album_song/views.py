from django.shortcuts import render
from .models import AlbumSong
from .serializers import AlbumSongSerializer
from rest_framework import filters,viewsets
# Create your views here.
class AlbumSongViewSet(viewsets.ModelViewSet):
    queryset = AlbumSong.objects.filter(is_deleted=False)
    serializer_class = AlbumSongSerializer