# project/serializers.py
from rest_framework import serializers
from .models import Song

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

    def create(self, validated_data):
        audio_file = validated_data.get('audio_url')
        if audio_file:
            # Đọc file từ in-memory
            audio = File(audio_file)
            if audio is not None and audio.info.length:
                validated_data['duration'] = int(audio.info.length)
        return super().create(validated_data)

class SongReadSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    video = VideoSerializer()

    class Meta:
        model = Song
        fields = '__all__'