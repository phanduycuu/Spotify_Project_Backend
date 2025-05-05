from django.shortcuts import render
from .models import FavouriteAlbum
from .serializers import FavouriteAlbumSerializer
from rest_framework import filters,viewsets
# Create your views here.
class FavouriteAlbumViewSet(viewsets.ModelViewSet):
    queryset = FavouriteAlbum.objects.filter(is_deleted=False)
    serializer_class = FavouriteAlbumSerializer

