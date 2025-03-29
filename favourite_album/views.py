from django.shortcuts import render
from .models import Singer
from .serializers import FavouriteAlbumSerializer
from rest_framework import filters,viewsets
# Create your views here.
class FavouriteAlbumViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = FavouriteAlbumSerializer

