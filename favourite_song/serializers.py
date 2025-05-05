# project/serializers.py
from rest_framework import serializers
from .models import FavouriteSong
from song.serializers import SongReadSerializer

class FavouriteSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteSong
        fields = '__all__'

class FavouriteSongUserSerializer(serializers.ModelSerializer):
    song = SongReadSerializer()
    class Meta:
        model = FavouriteSong
        fields = '__all__'