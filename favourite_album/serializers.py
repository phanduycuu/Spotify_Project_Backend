# project/serializers.py
from rest_framework import serializers
from .models import FavouriteAlbum
from album.serializers import AlbumSerializer

class FavouriteAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteAlbum
        fields = '__all__'

class FavouriteAlbumUserSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    class Meta:
        model = FavouriteAlbum
        fields = '__all__'