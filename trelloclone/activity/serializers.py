from rest_framework import serializers
from activity.models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'creator'
            'content',
            'created_at',
            'card',
            'is_comment',
        )
