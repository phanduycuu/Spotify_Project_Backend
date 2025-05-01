# project/serializers.py
from rest_framework import serializers
from .models import Video
import tempfile 
from rest_framework import serializers
from moviepy import VideoFileClip
import os

class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.FileField(required=False)  # 👈 Không bắt buộc khi cập nhật

    class Meta:
        model = Video
        fields = '__all__'

    def create(self, validated_data):
        video_file = validated_data.get('video_url')
        if video_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                clip = VideoFileClip(temp_file_path)
                validated_data['duration'] = int(clip.duration)
                clip.close()
            except Exception as e:
                print(f"Lỗi khi đọc thời lượng video: {e}")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        video_file = validated_data.get('video_url', None)

        if video_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            try:
                clip = VideoFileClip(temp_file_path)
                validated_data['duration'] = int(clip.duration)
                clip.close()
            except Exception as e:
                print(f"Lỗi khi đọc thời lượng video: {e}")
        else:
            validated_data['video_url'] = instance.video_url
            validated_data['duration'] = instance.duration

        return super().update(instance, validated_data)