# project/serializers.py
from rest_framework import serializers
from .models import Song
from mutagen import File
class SongReadSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    video = VideoSerializer()

    class Meta:
        model = Song
        fields = '__all__'


class SongWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

    def create(self, validated_data):
        audio_file = validated_data.get('audio_url')
        if audio_file:
            audio = File(audio_file)
            if audio and audio.info.length:
                validated_data['duration'] = int(audio.info.length)
        return super().create(validated_data)