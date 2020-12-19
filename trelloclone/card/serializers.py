from rest_framework import serializers
from card.models import Card


class CardSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    due_date = serializers.DateTimeField()
    activities = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = (
            'prev',
            'next',
            'name',
            'members',
            'description',
            'due_date',
            'activities'
        )

    def get_members(self, card):
        if

    def create(self, validated_data):
        os, created = OperatingSystem.objects.get_or_create(name=validated_data.pop('os_name'))
        validated_data['os'] = os
        validated_data['user'] = self.context['request'].user
        return super(SurveyResultSerializer, self).create(validated_data)
