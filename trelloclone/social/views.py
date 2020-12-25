from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework import status, viewsets
from rest_framework.response import Response
from allauth.account.adapter import get_adapter
#from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import SocialLoginView
from django.contrib.auth.models import User
from social.serializers import SocialLoginSerializer
from user.models import UserProfile
from user.serializers import UserSerializer

class GoogleLogin(SocialLoginView):
    serializer_class=SocialLoginSerializer
    adapter_class=GoogleOAuth2Adapter
    client_class=OAuth2Client

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)
        user=self.user
        UserProfile.objects.get_or_create(user=user, access_type="OAUTH")
        print("came in everytime")
        #return Response(UserSerializer(user).data,status=status.HTTP_201_CREATED)