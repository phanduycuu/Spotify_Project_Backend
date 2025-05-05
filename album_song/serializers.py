# project/serializers.py
from rest_framework import serializers
from .models import AlbumSong
from song.serializers import SongReadSerializer

class AlbumSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumSong
        fields = '__all__'

class AlbumSongWithSongSerializer(serializers.ModelSerializer):
    song = SongReadSerializer()

    class Meta:
        model = AlbumSong
        fields = ['id', 'song', 'created_at']