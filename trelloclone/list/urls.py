from django.urls import include, path
from rest_framework.routers import SimpleRouter

from list.views import ListViewSet

app_name = 'list'

router = SimpleRouter()
router.register('list', ListViewSet, basename='list')

urlpatterns = [
    path('', include((router.urls))),
]