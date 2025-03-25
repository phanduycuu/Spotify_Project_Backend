from django.shortcuts import render
from rest_framework import generics
from .models import Artist
from .serializers import ArtistSerializer
# Create your views here.
class ArtistListCreate(generics.ListCreateAPIView):
    queryset = Artist.objects.filter(is_deleted=False)
    serializer_class = ArtistSerializer

class ArtistRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer