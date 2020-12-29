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
        activities = Activity.objects.all().filter(card_id=card.id).order_by('created_at')
        return ActivitySerializer(activities, many=True, context=self.context).data

    # def change_list_of_card(self, card, data):
    #     ##########################################################
    #     # 참고
    #     # List1 :  A <- B <- C
    #     # List2 :  E <- F <- G
    #     # 일 때, B를 F 앞으로 갖다놓는 로직을 주석으로 설명
    #     # 현재 data에는 바꿀 리스트와 prev의 id가 들어온 상황.
    #     ###########################################################
    #     list = List.objects.all().get(id=data.get('list'))  # 옮길 리스트인 List# 2를 받아온다
    #     card.list = list  # 리스트를 변경해준다
    #     beforeListNextCard = Card.objects.all().get(prev=card)  # 다음 카드인 C 를 받아온다
    #     beforeListNextCard.prev = card.prev  # C의 화살표를 A로 향하게 한다.
    #     if (data.get('prev')==None) or (data.get('prev')==""): # 받아온 prev가 없으면
    #         head = Card.objects.all().get(is_head=True)
    #         card.prev = head
    #         afterListNextCard = Card.objects.all().get(list=list, prev=head) # 원래 head에 있던 카드를 찾는다
    #         afterListNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
    #     else: # 받아온 prev가 있으면
    #         afterListPrevCard = Card.objects.all().get(id=data.get('prev'))  # E를 찾는다
    #         afterListNextCard = Card.objects.all().get(prev=afterListPrevCard)  # F를 찾는다.
    #         afterListNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
    #         card.prev = afterListPrevCard  # 마지막으로 B의 화살표를 E로 향하게 한다.
    #         afterListPrevCard.save()
    #     beforeListNextCard.save()
    #     afterListNextCard.save()

    # def change_order_of_card(self, card, data):
    #     beforeNextCard = Card.objects.all().get(prev=card.id)  # 다음 카드인 C 를 받아온다
    #     beforeNextCard.prev = card.prev  # C의 화살표를 A로 향하게 한다.
    #     afterPrevCard = Card.objects.all().get(id=data.get('prev'))  # E를 찾는다
    #     afterNextCard = Card.objects.all().get(prev=afterPrevCard)  # F를 찾는다.
    #     afterNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
    #     card.prev = afterPrevCard  # 마지막으로 B의 화살표를 E로 향하게 한다.
    #     beforeNextCard.save()
    #     afterPrevCard.save()
    #     afterNextCard.save()

    # def update(self, card_id, data):
    #     card = Card.objects.all().get(id=card_id)
    #     creator = card.creator
    #     #create activity.
    #     if data.get('name'): card.name = data.get('name')
    #     if data.get('description'): card.description = data.get('description')
    #     if data.get('due_date'): card.due_date = data.get('due_date')
    #     if data.get('list') and data.get('prev'):
    #         self.change_list_of_card(self, card, data)
    #     elif data.get('prev') and not(data.get('list')):
    #         self.change_order_of_card(self, card, data)
    #     if data.get('member'):
    #         self.create_activity(self, card, data) # activity만들어주기
    #     card.save()

    # def create_activity(self, card, data):
    #     creator = card.creator
    #     member = User.objects.all().get(id=data.get('member'))
    #     UserCard.objects.all().create(user=member, card=card)
    #     if card.creator==member:
    #         content = creator.username + "joined this card"
    #     else:
    #         content = creator + " added " + member.username + " to this card"

    #     Activity.objects.all().create(creator=creator, content=content, card=card, is_comment=False)


    # def create_activity(self, card):
    #     creator = card.creator
    #     content = creator.username + " added this card to " + card.list.name
    #     Activity.objects.all().create(creator=creator, content=content, card=card, is_comment=False)
    #     return

    # def delete(self, card_id):
    #     card = self.queryset.get(id='card_id')
    #     prev= card.prev
    #     next = self.queryset.get(prev=card)
    #     next.prev = prev
    #     next.save()
    #     card.delete()
    #     return
    #     # 연결해주는거 다시 체

class BasicCardSerializer(CardSerializer):
    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'members',
        )




