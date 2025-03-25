from django.shortcuts import render
from rest_framework import generics
from .models import Video
from .serializers import VideoSerializer
# Create your views here.
class VideoListCreate(generics.ListCreateAPIView):
    queryset = Video.objects.filter(is_deleted=False)
    serializer_class = VideoSerializer

class VideoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer