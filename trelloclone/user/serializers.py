from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(allow_blank=False)
    access_type = serializers.ChoiceField(required=True, choices=['OAUTH', 'PASSWORD'])
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
            'last_name'
        )

class MiniUserSerializer(serializers.ModelSerializer) : # user/userlist  ,  board/userlist/  ,  card/ 등에 사용.

    username = serializers.CharField(required=True)
    email = serializers.EmailField(allow_blank=False)
    access_type = serializers.ChoiceField(required=True, choices=['OAUTH', 'PASSWORD'])
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
            'last_name'
        )