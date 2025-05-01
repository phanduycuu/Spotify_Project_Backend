from rest_framework import viewsets
from rest_framework.response import Response
from .models import Artist
from .serializers import ArtistSerializer

class ArtistViewSet(viewsets.ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        })
    def destroy(self, request, *args, **kwargs):
        artist = self.get_object()
        artist.is_deleted = True
        artist.save()
        return Response(status=status.HTTP_204_NO_CONTENT)