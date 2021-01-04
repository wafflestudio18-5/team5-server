from rest_framework import serializers
from activity.models import Activity
from django.contrib.auth.models import User

class ActivitySerializer(serializers.ModelSerializer):

    creator = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = (
            'id',
            'creator',
            'created_at',
            'content',
            'is_comment',
        )
    def get_creator(self,activityobj):
        return activityobj.creator.username
    

    
