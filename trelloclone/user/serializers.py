from django.contrib.auth.models import User
from user.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token


class SocialSerializer(serializers.Serializer):
    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)

class UserProfile(serializers.ModelSerializer):
    user = serializers.ModelSerializer()
    class Meta:
        model = UserProfile
        fields = (
            'user',
            'access_type',
        )
    def get_user(self):
        user = self.data.user
        print(user)
        return UserSerializer(user, context= self.context).data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(allow_blank=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
        )

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        Token.objects.create(user=user)

        return user

    def validate_password(self, value):
        return make_password(value)

    def validate(self, data):
        if (bool(data.get('username')) == False) or (data.get('username') == ""):
            raise serializers.ValidationError("Enter the username")
        if (bool(data.get('email')) == False) or (data.get('email') == ""):
            raise serializers.ValidationError("Enter the email")
        else:
            if data.get('email').find('@') == -1:
                raise serializers.ValidationError("Invalid email form")

        return data

    def update(self, user, data):
        if data.get('username'):
            username = data.get('username')
            user.username = username
            user.save()
        return

# class MiniUserSerializer(serializers.ModelSerializer) : # user/userlist  ,  board/userlist/  ,  card/ 등에 사용.
#
#     username = serializers.CharField(required=True)
#     email = serializers.EmailField(allow_blank=False)
#     access_type = serializers.ChoiceField(required=True, choices=['OAUTH', 'PASSWORD'])
#     first_name = serializers.CharField(required=False)
#     last_name = serializers.CharField(required=False)
#
#     class Meta:
#         model = User
#         fields = (
#             'id',
#             'username',
#             'password',
#             'email',
#             'first_name',
#             'last_name'
#         )
