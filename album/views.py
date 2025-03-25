from django.shortcuts import render
from rest_framework import generics
from .models import Album
from .serializers import AlbumSerializer
# Create your views here.
class AlbumListCreate(generics.ListCreateAPIView):
    queryset = Album.objects.filter(is_deleted=False)
    serializer_class = AlbumSerializer

class AlbumRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer