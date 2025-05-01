# project/serializers.py
from rest_framework import serializers
from .models import Album
from song.models import Song

class AlbumSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
class SongSerializer(serializers.ModelSerializer):
    audio_url = serializers.SerializerMethodField()

    class Meta:
        model = Song
        exclude = ['is_deleted']

    def get_audio_url(self, obj):
        request = self.context.get('request')
        if obj.audio_url and hasattr(obj.audio_url, 'url') and request:
            return request.build_absolute_uri(obj.audio_url.url)
        return None
class AlbumSerializer(serializers.ModelSerializer):
    album_songs = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = '__all__'

    def get_album_songs(self, obj):
        request = self.context.get('request')  # 👈 lấy request từ context
        songs = obj.album_songs.filter(is_deleted=False)
        return SongSerializer(songs, many=True, context={'request': request}).data  # 👈 truyền request vào đây

