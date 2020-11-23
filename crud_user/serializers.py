from rest_framework import serializers
from rest_framework.authtoken.admin import User
import re


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)
    username = serializers.CharField(max_length=150, min_length=1, required=True)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    is_active = serializers.BooleanField(required=True)
    last_login = serializers.CharField(max_length=120, required=False, read_only=True)
    is_superuser = serializers.BooleanField(required=False, read_only=True)
    password = serializers.CharField(max_length=120, write_only=True, required=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

    def validate_password(self, value):
        if re.match('^(?=.*[A-Z])(?=.*\d).{8,}$', value) is None:
            raise serializers.ValidationError("Password should be 8+ characters, 1 capital, 1 numeric")
        return value

    def validate_username(self, value):
        if not not User.objects.filter(username=value):
            raise serializers.ValidationError("A user with that username already exists.")
        elif re.match('^[\w.@+-]+$', value) is None:
            raise serializers.ValidationError("150 characters or fewer. Letters, digits and @/./+/-/_ only.")
        return value


