from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from user.models import UserProfile
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from user.serializers import UserSerializer
import requests


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ('create', 'login'):
            return (AllowAny(),)
        return super(UserViewSet, self).get_permissions()

    def google(self, data):
        id_token = data.get('token')
        url = f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
        response = requests.get(url)
        if response.status_code != status.HTTP_200_OK:
            return False
        response_data = response.json()
        return response_data

    def facebook(self, data):
        # get id
        access_token = data.get('token')
        url_for_id = f"https://graph.facebook.com/v9.0/me?access_token={access_token}"
        response = requests.get(url_for_id)
        if response.status_code != status.HTTP_200_OK:
            return False
        response_data = response.json()
        user_id = response_data.get('id')
        # get info using id and access token
        url_for_info = f"https://graph.facebook.com/{user_id}?fields=name,email,first_name,last_name&access_token={access_token}"
        response = requests.get(url_for_info)
        if response.status_code != status.HTTP_200_OK:
            return False
        response_data = response.json()
        return response_data

    def fb_trans(self, data):
        data['username'] = data.get('name')
        data['password'] = "social"
        return data

    def gg_trans(self, data):
        data['username'] = data.get('name')
        data['first_name'] = data.get('given_name')
        data['last_name'] = data.get('family_name')
        data['password'] = "social"
        return data

    def create(self, request):
        data = request.data

        if data.get('access_type') == "OAUTH":
            provider = data.get('provider')
            if provider == "Google": data = self.google(data)
            else: data = self.facebook(data)
            if bool(data) == False: return Response({"error": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
            if provider == "Google": data = self.gg_trans(data)
            else: data = self.fb_trans(data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        data = serializer.validated_data
        data['token'] = user.auth_token.key

        type = request.data.get('access_type')
        UserProfile.objects.create(user=user, access_type=type)

        return Response(data, status=status.HTTP_201_CREATED)

    def pop_username(self, email):
        try:
            check_username = User.objects.get(email=email)
            if check_username: return check_username
        except:
            return False

    @action(detail=False, methods=['PUT'])
    def login(self, request):
        data = request.data
        user = None

        if data.get('access_type') == "OAUTH":
            provider = data.get('provider')
            if provider == "Google": data = self.google(data)
            else: data = self.facebook(data)
            if bool(data) == False: return Response({"error": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)
            else:
                email = data.get('email')
                if self.pop_username(email)==False:
                    return Response({"error": "No matching user found. Did you sign up?"}, status=status.HTTP_403_FORBIDDEN)
                else :
                    username = self.pop_username(email)
                    user = authenticate(request, username=username, email=email, password="social")

        else:
            email = data.get('email')
            password = data.get('password')

            if self.pop_username(email)==False:
                return Response({"error": "No matching user found. Did you sign up?"}, status=status.HTTP_403_FORBIDDEN)
            else :
                username = self.pop_username(email)
                user = authenticate(request, username=username, email=email, password=password)

        if user:
            type_check = UserProfile.objects.get(user=user)
            if type_check.access_type != request.data.get('access_type'):
                return Response({"error": "No matching user found. Re-check your account type."}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            data = self.get_serializer(user).data
            token, created = Token.objects.get_or_create(user=user)
            data['token'] = token.key
            return Response(data)

        return Response({"error": "No matching user found. Re-check your email and account type."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['PUT'])
    def logout(self, request):
        logout(request)
        return Response()

    def retrieve(self, request, pk=None):
        user = request.user
        token_error = False
        try:
            rst = self.get_serializer(user).data
        except:
            token_error = True
        if token_error:
            return Response({"error": "Provide proper token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(rst)

    def update(self, request, pk=None):
        if pk != 'me':
            return Response({"error": "No permission to other's info"}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        data = request.data
        data = self.add_created(data, True)
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data)
