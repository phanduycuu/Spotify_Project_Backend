from rest_framework import serializers
from song.models import Song
from artist.models import Artist
from video.models import Video

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'img_url']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_url']

    def to_representation(self, instance):
        # Chỉ trả về video nếu is_deleted=False
        if instance.is_deleted:
            return None
        return super().to_representation(instance)

class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    video = VideoSerializer(read_only=True)

    class Meta:
        model = Song
        fields = ['id', 'name', 'artist', 'genre', 'audio_url', 'duration', 'lyrics', 'created_at', 'video']