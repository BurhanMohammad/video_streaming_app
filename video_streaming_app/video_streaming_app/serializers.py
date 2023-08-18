from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Video

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'video_path']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.video_path = validated_data.get('video_path', instance.video_path)
        instance.save()
        return instance


