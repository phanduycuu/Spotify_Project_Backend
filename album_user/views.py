from django.shortcuts import render
from .models import AlbumUser
from .serializers import AlbumUserSerializer
from rest_framework import filters,viewsets
# Create your views here.
class AlbumUserViewSet(viewsets.ModelViewSet):
    queryset = AlbumUser.objects.filter(is_deleted=False)
    serializer_class = AlbumUserSerializer