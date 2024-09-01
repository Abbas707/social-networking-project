from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserDetails


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = UserDetails.objects.create_user(
            name=validated_data['name'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user


class UserDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('id', 'email', 'name')


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Serializer for vendor user to validate and obtain the token """

    default_error_messages = {
        'no_active_account': 'Your Username & Password do not match. Please try again.'
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user_details'] = UserDetailModelSerializer(self.user).data
        return data
