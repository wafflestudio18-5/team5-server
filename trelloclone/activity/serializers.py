from rest_framework import serializers
from activity.models import Activity
from django.contrib.auth.models import User

class ActivitySerializer(serializers.ModelSerializer):

    content = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = (
            'creator'
            'content',
            'created_at',
            'card_name',
        )

    def get_content(self, activity): # 가장 기본.
        card = activity.card
        list = card.list
        content = activity.creator + " added this card to " + list.name
        return content

    def create(self, data):
        activity = super(ActivitySerializer, self).create(data)
        return activity

    def update(self, activity_id, data):
        activity = Activity.objects.get(id=activity_id)
        if data.get('member'):
            creator = activity.creator
            member = User.objects.get(id=data.get('member'))
            if creator == member:
                activity.content = creator + "joined this card"
            else:
                member = User.objects.get(id=data.get('member'))
                activity.content = creator + " added " + member + " to this card"

        elif data.get('content'):
                activity.content=data.get('content')

        activity.save()

        return activity

    def delete(self, activity_id):
        activity = Activity.objects.get(id=activity_id)
        activity.delete()

