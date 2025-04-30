from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Album
from .serializers import AlbumSerializer
# Create your views here.
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.filter(is_deleted=False)
    serializer_class = AlbumSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)