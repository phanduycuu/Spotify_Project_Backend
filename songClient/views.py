from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import StreamingHttpResponse
import os
from song.models import Song
from .serializers import SongSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CaseInsensitiveSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        terms = super().get_search_terms(request)
        return [term.lower() for term in terms]

class SongViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Song.objects.filter(is_deleted=False).select_related('artist', 'video')
    serializer_class = SongSerializer
    filter_backends = [CaseInsensitiveSearchFilter]
    search_fields = ['name', 'artist__name', 'genre']
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def stream(self, request, pk=None):
        song = self.get_object()
        file_path = song.audio_url

        if not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=404)

        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(
            file_iterator(file_path),
            content_type='audio/mpeg'
        )
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        song = self.get_object()
        file_path = song.audio_url

        if not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=404)

        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(
            file_iterator(file_path),
            content_type='audio/mpeg'
        )
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    @action(detail=True, methods=['GET'])
    def stream_video(self, request, pk=None):
        song = self.get_object()
        if not song.video:
            return Response({'error': 'No video associated with this song'}, status=404)

        file_path = song.video.video_url

        if not os.path.exists(file_path):
            return Response({'error': 'Video file not found'}, status=404)

        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(
            file_iterator(file_path),
            content_type='video/mp4'
        )
        response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
        return response

    @action(detail=True, methods=['GET'])
    def download_video(self, request, pk=None):
        song = self.get_object()
        if not song.video:
            return Response({'error': 'No video associated with this song'}, status=404)

        file_path = song.video.video_url

        if not os.path.exists(file_path):
            return Response({'error': 'Video file not found'}, status=404)

        def file_iterator(file_path, chunk_size=8192):
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        response = StreamingHttpResponse(
            file_iterator(file_path),
            content_type='video/mp4'
        )
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response