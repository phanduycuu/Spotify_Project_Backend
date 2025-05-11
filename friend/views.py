from django.shortcuts import render
from rest_framework import viewsets,status,filters
from rest_framework.response import Response
from .serializers import FriendAPISerializer
from .models import Friend
# Create your views here.
class FriendViewSet(viewsets.ModelViewSet):
    serializer_class = FriendAPISerializer
    queryset = Friend.objects.all()