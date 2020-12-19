from rest_framework import serializers
from django.contrib.auth.models import User
from card.models import Card
from user.serializers import MiniUserSerializer
from activity.models import Activity
from activity.serializers import ActivitySerializer


class CardSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    activities = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = (
            'prev',
            'list'
            'name',
            'members',
            'description',
            'due_date',
            'activities'
        )

    def get_members(self, card):
        members = User.objects.filter(card_id=card.id)  # 조건..?
        return MiniUserSerializer(members, many=True, context=self.context).data

    def get_activities(self, card):
        activities = Activity.objects.filter(card_id=card.id)
        return ActivitySerializer(activities, many=True, context=self.context).data

    def create(self, validated_data):
        card = super(CardSerializer, self).create(validated_data)
        return card

    #member추가 어떻게 하면 좋을까..
    def update(self, card_id, validated_data):
        card = Card.objects.get(id=card_id)
        if validated_data.get('members'):
            members = validated_data.get('members')
            for member_id in members: #멤버가 리스트로 들어온다는 가정 하에..
                add_member = User.objects.get(id=member_id) #해당 멤버를 User에서 찾고
                add_member.card = card #해당 멤버의 card를 현재 카드로 설정한다.
                add_member.save()
        if validated_data.get('name'): card.name = validated_data.get('name')
        if validated_data.get('description'): card.description = validated_data.get('description')
        if validated_data.get('due_date'): card.due_date = validated_data.get('due_date')
        if validated_data.get('list') and validated_data.get('prev'):
            list=List.object.get(id=validated_data.get('list'))
            card.list=list
            prev_card = Card.objects.get() ##여기 작성하고있었습니당
        card.save()
        return

    #view에서 하는게 낫긴 한데, 일단 통일성을 위해..
    def delete(self, card_id):
        card = Card.objects.get(id=card_id)
        card.delete()



