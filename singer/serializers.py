# project/serializers.py
from rest_framework import serializers
from .models import Singer

class SingerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'