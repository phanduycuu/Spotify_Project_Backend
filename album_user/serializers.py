# project/serializers.py
from rest_framework import serializers
from .models import AlbumUser
from album_song.serializers import AlbumSongWithSongSerializer

class AlbumUserSerializer(serializers.ModelSerializer):
    album_user_song = AlbumSongWithSongSerializer(many=True, read_only=True)
    class Meta:
        model = AlbumUser
        fields = '__all__'
    def get_album_user_song(self, obj):
        request = self.context.get('request') 
        valid_album_songs = obj.album_user_song.filter(is_deleted=False,song__is_deleted=False).select_related('song')
        return AlbumSongWithSongSerializer(valid_album_songs, many=True, context={'request': request}).data