# project/serializers.py
from rest_framework import serializers
from .models import Song
from mutagen.mp3 import MP3
from mutagen import File as MutagenFile

from album.serializers import AlbumSerializer
from video.serializers import VideoSerializer
import tempfile
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
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                from mutagen.mp3 import MP3
                audio = MP3(temp_file_path)
                validated_data['duration'] = int(audio.info.length)
            except Exception as e:
                print(f"Không đọc được file mp3: {e}")
        return super().create(validated_data)