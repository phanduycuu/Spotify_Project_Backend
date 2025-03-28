# project_part/serializers.py
from rest_framework import serializers

from .models import Account
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role')
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()