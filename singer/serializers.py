# project/serializers.py
from rest_framework import serializers
from .models import Singer
from artist.serializers import ArtistSerializer

class SingerSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    class Meta:
        model = Singer
        fields = '__all__'
class SingerArtistSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    class Meta:
        model = Singer
        fields = ['artist']
