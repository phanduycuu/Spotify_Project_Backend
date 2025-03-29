# project/serializers.py
from rest_framework import serializers
from .models import FavouriteAlbum

class FavouriteAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteAlbum
        fields = '__all__'