from rest_framework import serializers
from rest_framework.authtoken.models import Token  # Importing Token
from django.contrib.auth import get_user_model  # Using get_user_model()

User = get_user_model()  # Correctly referencing the custom user model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Using get_user_model().objects.create_user to create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )
        # Token creation after user registration
        Token.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
