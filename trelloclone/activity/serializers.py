from rest_framework import serializers
from activity.models import Activity
from django.contrib.auth.models import User

class ActivitySerializer(serializers.ModelSerializer):

    card_name = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = (
            'creator',
            'content',
            'created_at',
            'card_name',
            'added_member',
            'comment_content'
        )

    def get_card_name(self, activity):
        card = activity.card
        card_name = card.name
        return card_name

    def create(self, data):
        activity = super(ActivitySerializer, self).create(data)
        return activity

    def update(self, activity_id, data):
        activity = Activity.objects.all().get(id=activity_id)
        if data.get('content'):
            activity.content=data.get('content')
        activity.save()
        return activity

