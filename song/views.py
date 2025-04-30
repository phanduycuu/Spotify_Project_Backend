from django.shortcuts import render
from .models import Song
from .serializers import SongReadSerializer,SongWriteSerializer
from rest_framework import filters,viewsets
from rest_framework.response import Response

# Create your views here.
class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.filter(is_deleted=False).order_by('-created_at')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SongReadSerializer
        return SongWriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
