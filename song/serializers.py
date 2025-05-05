# project/serializers.py
from rest_framework import serializers
from .models import Song
from mutagen.mp3 import MP3
from mutagen import File as MutagenFile

from album.serializers import AlbumSongSerializer
from video.serializers import VideoSerializer
from singer.serializers import SingerArtistSerializer
import tempfile


class SongReadSerializer(serializers.ModelSerializer):
    album = AlbumSongSerializer()
    video = VideoSerializer()
    song_singers = SingerArtistSerializer(many=True)

    class Meta:
        model = Song
        fields = '__all__'
        


class SongWriteSerializer(serializers.ModelSerializer):
    audio_url = serializers.FileField(required=False)
    img_url = serializers.FileField(required=False)

    class Meta:
        model = Song
        fields = '__all__'

    def get_audio_duration(self, file_path):
        """
        Ưu tiên dùng mutagen để đọc nhiều định dạng file, fallback sang ffprobe nếu thất bại
        """
        try:
            audio = MutagenFile(file_path)
            if audio is not None and audio.info.length:
                return int(audio.info.length)
            else:
                raise Exception("Không có thông tin length trong audio")
        except Exception as e:
            print(f"[mutagen] Lỗi khi đọc file audio: {e}")
            # Fallback: dùng ffprobe
            try:
                result = subprocess.run(
                    ['ffprobe', '-i', file_path, '-show_entries', 'format=duration',
                     '-v', 'quiet', '-of', 'csv=p=0'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=True
                )
                duration_str = result.stdout.strip()
                return int(float(duration_str))
            except Exception as fe:
                print(f"[ffprobe] Không đọc được file: {fe}")
                return None

    def create(self, validated_data):
        audio_file = validated_data.get('audio_url')

        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            duration = self.get_audio_duration(temp_file_path)
            if duration:
                validated_data['duration'] = duration

        return super().create(validated_data)

    def update(self, instance, validated_data):
        audio_file = validated_data.get('audio_url', None)
        img_file = validated_data.get('img_url', None)

        if audio_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".audio") as temp_file:
                for chunk in audio_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            duration = self.get_audio_duration(temp_file_path)
            if duration:
                validated_data['duration'] = duration
        else:
            validated_data['audio_url'] = instance.audio_url
            validated_data['duration'] = instance.duration

        if not img_file:
            validated_data['img_url'] = instance.img_url

        return super().update(instance, validated_data)