from rest_framework import viewsets, status,filters
from rest_framework.response import Response
from .models import Album
from .serializers import AlbumSerializer,SongSerializer
from song.models import Song
from song.serializers import SongReadSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.filter(is_deleted=False)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    serializer_class = AlbumSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        album = self.get_object()
        album.is_deleted = True
        album.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='get-songs/(?P<album_id>[^/.]+)')
    def get_songs(self, request, album_id=None):
        album = get_object_or_404(Album, pk=album_id, is_deleted=False)
        songs = album.album_songs.filter(is_deleted=False)
        serializer = SongSerializer(songs, many=True, context={'request': request})  # 👈 fix ở đây
        return Response({
            'count': songs.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)