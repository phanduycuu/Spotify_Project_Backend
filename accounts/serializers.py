# project_part/serializers.py
from rest_framework import serializers

from .models import Account
class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'email', 'password','full_name','sex','birthday', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role', None)  # Lấy role từ role_id
        user = Account.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=role,  # Bổ sung role vào đây để tránh lỗi NULL
        )
        return user
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])  # Dùng set_password()
            validated_data.pop('password')
        return super().update(instance, validated_data)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
class UpdateProfieSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    sex = serializers.ChoiceField(choices=[('male', 'Nam'), ('female', 'Nữ'), ('other', 'Khác')], required=False, allow_null=True)
    birthday = serializers.DateField(required=False, allow_null=True)