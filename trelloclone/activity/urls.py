from django.urls import include, path
from rest_framework.routers import SimpleRouter

from activity.views import ActivityViewSet

app_name = 'activity'

router = SimpleRouter()
router.register('activity', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include((router.urls))),
]