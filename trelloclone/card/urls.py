from django.urls import include, path
from rest_framework.routers import SimpleRouter

from card.views import CardViewSet

app_name = 'card'

router = SimpleRouter()
router.register('card', CardViewSet, basename='card')

urlpatterns = [
    path('', include((router.urls))),
]