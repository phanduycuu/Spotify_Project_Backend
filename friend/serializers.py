# project/serializers.py
from rest_framework import serializers
from friend.models import Friend
class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = '__all__'
        read_only_fields = ['user1', 'created_at']
