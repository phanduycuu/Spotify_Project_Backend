# project/serializers.py
from rest_framework import serializers
from friend.models import Friend
from account.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'full_name', 'sex', 'birthday']
class FriendSerializer(serializers.ModelSerializer):
    sender = AccountSerializer(source='user1')
    class Meta:
        model = Friend
        fields = '__all__'
        read_only_fields = ['user1', 'created_at']
