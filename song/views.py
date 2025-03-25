from django.shortcuts import render
from .models import Song
from .serializers import SongSerializer
from rest_framework import filters,viewsets
# Create your views here.
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.filter(is_deleted=False).order_by('-created_at')
    serializer_class = SongSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
