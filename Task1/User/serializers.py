from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import  user,FriendRequest

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        
        if password:
            validated_data['password'] = make_password(password)
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['id', 'name', 'email']
        

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()
    to_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']