from django.shortcuts import render
from .models import Singer
from .serializers import SingerSerializer
from rest_framework import filters,viewsets
# Create your views here.
class SingerViewSet(viewsets.ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerSerializer

