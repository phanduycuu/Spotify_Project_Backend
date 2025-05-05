# project/serializers.py
from rest_framework import serializers
from .models import AlbumUser
from album_song.serializers import AlbumSongWithSongSerializer

class AlbumUserSerializer(serializers.ModelSerializer):
    album_user_song = AlbumSongWithSongSerializer(many=True, read_only=True)
    class Meta:
        model = AlbumUser
        fields = '__all__'