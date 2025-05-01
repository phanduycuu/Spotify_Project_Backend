from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Album
from .serializers import AlbumSerializer,SongSerializer
from song.models import Song
from song.serializers import SongReadSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    
    def get_queryset(self):
        # Chỉ trả về album chưa bị xóa
        return Album.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='get-songs/(?P<album_id>[^/.]+)')
    def get_songs(self, request, album_id=None):
        album = get_object_or_404(Album, pk=album_id, is_deleted=False)
        songs = album.album_songs.filter(is_deleted=False)
        serializer = SongSerializer(songs, many=True, context={'request': request})  # 👈 fix ở đây
        return Response({
            'count': songs.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)