# project/serializers.py
from rest_framework import serializers
from .models import Video
import tempfile 
from rest_framework import serializers
from moviepy import VideoFileClip
import os

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def create(self, validated_data):
        video_file = validated_data.get('video_url')
        if video_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                # Ghi nội dung file tạm
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # Lấy thời lượng video
            clip = VideoFileClip(temp_file_path)
            validated_data['duration'] = int(clip.duration)
            clip.close()

        return super().create(validated_data)