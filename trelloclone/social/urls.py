from django.urls import include, path
from rest_framework.routers import SimpleRouter

from social.views import GoogleLogin

app_name = 'social'

router = SimpleRouter()
router.register('social', GoogleLogin, basename='social')  # /api/v1/user/

urlpatterns = [
    path('', include((router.urls))),
]