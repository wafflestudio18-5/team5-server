from rest_framework import serializers
from django.contrib.auth.models import User
from card.models import Card
from list.models import List
from user.serializers import MiniUserSerializer
from activity.models import Activity
from activity.serializers import ActivitySerializer

class CardSerializer(serializers.ModelSerializer):
    activities = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = (
            'prev',
            'list'
            'name',
            'members',
            'description',
            'due_date',
            'activities',
            'created_at'
        )

    def get_members(self, card):
        try:
            members = User.objects.filter(card_id=card.id)
        except:
            return ""
        return MiniUserSerializer(members, many=True, context=self.context).data

    def get_activities(self, card):
        activities = Activity.objects.filter(card_id=card.id)
        return ActivitySerializer(activities, many=True, context=self.context).data

    def create(self, data):
        card = super(CardSerializer, self).create(data)
        return card

    def update(self, card_id, data):
        card = Card.objects.get(id=card_id)
        if data.get('members'):
            member_id = data.get('members')
            new_member = User.objects.get(id=member_id) #해당 멤버를 User에서 찾고
            new_member.card = card #해당 멤버의 card를 현재 카드로 설정한다.
            new_member.save()

        #create Activity -> view에서
        if data.get('name'): card.name = data.get('name')
        if data.get('description'): card.description = data.get('description')
        if data.get('due_date'): card.due_date = data.get('due_date')
        if data.get('list') and data.get('prev'):
            ##########################################################
            # 참고
            # List1 :  A <- B <- C
            # List2 :  E <- F <- G
            # 일 때, B를 F 앞으로 갖다놓는 로직을 주석으로 설명
            # 현재 data에는 바꿀 리스트와 prev의 id가 들어온 상황.
            ###########################################################

            list=List.objects.get(id=data.get('list')) # 옮길 리스트인 List2를 받아온다
            card.list=list # 리스트를 변경해준다
            beforeListNextCard = Card.objects.get(prev=card.id) # 다음 카드인 C 를 받아온다
            beforeListNextCard.prev=card.prev # C의 화살표를 A로 향하게 한다.
            afterListPrevCard = Card.objects.get(id=data.get('prev')) # E를 찾는다
            afterListNextCard = Card.objects.get(prev=afterListPrevCard) # F를 찾는다.
            afterListNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
            card.prev = afterListPrevCard # 마지막으로 B의 화살표를 E로 향하게 한다.
            afterListPrevCard.save()
            afterListNextCard.save()
        card.save()
        return

    #view에서 하는게 낫긴 한데, 일단 통일성을 위해..
    def delete(self, card_id):
        card = Card.objects.get(id=card_id)
        card.delete()


