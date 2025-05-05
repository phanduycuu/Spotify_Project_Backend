from django.shortcuts import render
from .models import FavouriteSong
from .serializers import FavouriteSongSerializer
from rest_framework import filters,viewsets
# Create your views here.
class FavouriteSongViewSet(viewsets.ModelViewSet):
    queryset = FavouriteSong.objects.filter(is_deleted=False)
    serializer_class = FavouriteSongSerializer