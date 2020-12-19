from rest_framework import serializers
from activity.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        activity = super(ActivitySerializer, self).create(validated_data)
        return activity


