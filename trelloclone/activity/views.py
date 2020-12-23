from rest_framework import status, viewsets
from django.contrib.auth.models import User
from card.models import UserCard, Card
from activity.models import Activity
from activity.serializers import ActivitySerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class ActivityViewSet(viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    ##############################################################

    def update(self, request, pk=None):
        card = self.get_object()
        # Q. 만약 다른 보드의 유저가 교체를 희망하는 경우도 넣어야 하나? 그게 사이트 입장에서 가능한가?
        # creator = request.user
        # if card.creator!=creator:
        #    return Response({"error": ""})
        data = request.data
        serializer = self.get_serializer(card, data=data, partial=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def delete(self, request):
        id = request.get('activity_id')
        try: activity = self.queryset.get(id=id)
        except: return Response({"error": "invalid activity id"}, status=status.HTTP_400_BAD_REQUEST)
        activity.delete()
        return Response(status=status.HTTP_200_OK)




