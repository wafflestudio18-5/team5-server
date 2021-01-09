from rest_framework import status, viewsets
from django.contrib.auth.models import User
from card.models import UserCard, Card
from activity.models import Activity
from activity.serializers import ActivitySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import dateformat, timezone

class ActivityViewSet(viewsets.GenericViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        card_id=request.data.get('card_id')
        content=request.data.get('content')
        if not card_id or not content:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            cardobj=Card.objects.get(id=card_id)
        except Card.DoesNotExist:
            return Response({'error':'card not found'},status=status.HTTP_400_BAD_REQUEST)
        activity_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        newact=Activity.objects.create(creator=user,content=content,card=cardobj,is_comment=True, created_at=activity_date)
        return Response(ActivitySerializer(newact).data, status=status.HTTP_201_CREATED)

    ##############################################################

    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        activity_id=request.data.get('id')
        content=request.data.get('content')
        if not content or not activity_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            actobj=Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            return Response({'error':'activity not found'},status=status.HTTP_400_BAD_REQUEST)
        if not actobj.is_comment:
            return Response({'error':'this activity is not a comment'},status=status.HTTP_400_BAD_REQUEST)
        if actobj.creator != user:
            return Response({'error':'This is not your comment'},status=status.HTTP_403_FORBIDDEN)
        actobj.content=content
        actobj.save()
        return Response(ActivitySerializer(actobj).data,status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        id = request.data.get('id')
        try: activity = Activity.objects.get(id=id)
        except Activity.DoesNotExist: return Response({"error": "invalid activity id"}, status=status.HTTP_400_BAD_REQUEST)

        if activity.creator != user:
            return Response({'error': 'This is not your comment'}, status=status.HTTP_403_FORBIDDEN)

        activity.delete()
        return Response(status=status.HTTP_200_OK)




