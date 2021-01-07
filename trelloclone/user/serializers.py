from django.contrib.auth.models import User
from user.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

class UserProfile(serializers.ModelSerializer):
    user = serializers.ModelSerializer()

    class Meta:
        model = UserProfile
        fields = (
            'user',
            'grantType',
        )

    def get_user(self):
        user = self.data.user
        return UserSerializer(user, context=self.context).data


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

        # username = data.get('username') # In case of social login, special char. ought to be allowed.
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        # if bool(username.isalnum())==False:
        #     raise serializers.ValidationError("Username should not include special characters.")
        # if bool(first_name) ^ bool(last_name):
        #     raise serializers.ValidationError("First name and last name should appear together.")
        # if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
        #     raise serializers.ValidationError("First name or last name should not have number.")
        # 생성하는거면 email과 username 중복을 모두 확인하고, 업데이트하는거면 username중복만 체크한다.
        email = data.get('email')
        create = False
        if email: create=True
        if create:
            if (bool(data.get('username')) == False) or (data.get('username') == ""):
                raise serializers.ValidationError("Enter the username")
            if (bool(data.get('email')) == False) or (data.get('email') == ""):
                raise serializers.ValidationError("Enter the email")
            else:
                if data.get('email').find('@') == -1:
                    raise serializers.ValidationError("Invalid email form")
            email_error = False
            try:
                email_duplicate = User.objects.get(email=data.get('email'))
                if email_duplicate:
                    email_error = True
            except:
                pass
            if email_error:
                error_msg = "Given email is already in use. Use another email or another social account unless you have already signed up."
                raise serializers.ValidationError(error_msg)

        name_error = False
        try:
            name_duplicate = User.objects.get(username=data.get('username'))
            if name_duplicate:
                name_error = True
        except:
            pass

        if name_error:
            error_msg = "Given username is already in use. Use another username."
            raise serializers.ValidationError(error_msg)

        return data


    def update(self, user, data):
        if data.get('username'):
            username = data.get('username')
            user.username = username
            user.save()
        return

