from rest_framework import serializers
from activity.models import Activity


class ActivitySerializer(serializers.ModelSerializer):

    #added_member 받아오는 방식
    added_member = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = (
            'creator'
            'content',
            'created_at',
            'added_member',
            'card_name',
            'is_comment',
        )

    def get_added_member(self):
        return

    def create(self, validated_data):
        activity = super(ActivitySerializer, self).create(validated_data)
        return activity

    def update(self, activity_id, validated_data):
        activity = Activity.objects.get(id=activity_id)
        if (validated_data.get('is_comment')==True) and (validated_data.get('content')):
            activity.content=validated_data.get('content')
            activity.save()
        return activity

    def delete(self, activity_id):
        activity = Activity.objects.get(id=activity_id)
        activity.delete()

