from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer

    def get_queryset(self):
        return Video.objects.filter(is_deleted=False).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)