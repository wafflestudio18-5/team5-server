from rest_framework import serializers
from django.contrib.auth.models import User
from card.models import Card, UserCard
from list.models import List
from user.serializers import UserSerializer
from activity.models import Activity
from activity.serializers import ActivitySerializer

class CardSerializer(serializers.ModelSerializer):
    queryset = Card.objects.all()
    activities = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'created_at',
            'description',
            'due_date',
            'members',
            'activities',
        )

    def get_members(self, card):
        usercard_members = UserCard.objects.all().filter(card=card)
        members = []
        for usercard in usercard_members:
            members.append(usercard.user)
        return UserSerializer(members, many=True, context=self.context).data

    def get_activities(self, card):
        activities = Activity.objects.all().filter(card_id=card.id).order_by('id')
        return ActivitySerializer(activities, many=True, context=self.context).data
    

class BasicCardSerializer(CardSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'members',
            'key',
        )




