from rest_framework import serializers
from django.contrib.auth.models import User
from card.models import Card, UserCard
from list.models import List
from user.serializers import MiniUserSerializer
from activity.models import Activity
from activity.serializers import ActivitySerializer

class CardSerializer(serializers.ModelSerializer):
    queryset = Card.objects.all()
    activities = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    prev = serializers.SerializerMethodField()
    class Meta:
        model = Card
        fields = (
            'prev',
            'list',
            'name',
            'members',
            'description',
            'due_date',
            'activities',
            'created_at'
        )

    def get_prev(self, card):
        prev = None
        return prev

    def get_members(self, card):
        members = UserCard.objects.filter(card=card)
        return MiniUserSerializer(members, many=True, context=self.context).data

    def get_activities(self, card):
        activities = Activity.objects.filter(card_id=card.id)
        return ActivitySerializer(activities, many=True, context=self.context).data

    def create(self, card, data):
        self.change_head_card(self, card)
        card = super(CardSerializer, self).create(data)


        return card

    def change_head_card(self, card):
        head_card = Card.objects.get(is_head=True)
        head_card.is_head=False
        card.is_head=True
        head_card.save()

    def change_list_of_card(self, card, data):
        ##########################################################
        # 참고
        # List1 :  A <- B <- C
        # List2 :  E <- F <- G
        # 일 때, B를 F 앞으로 갖다놓는 로직을 주석으로 설명
        # 현재 data에는 바꿀 리스트와 prev의 id가 들어온 상황.
        ###########################################################
        list = List.objects.get(id=data.get('list'))  # 옮길 리스트인 List# 2를 받아온다
        card.list = list  # 리스트를 변경해준다
        beforeListNextCard = Card.objects.get(prev=card)  # 다음 카드인 C 를 받아온다
        beforeListNextCard.prev = card.prev  # C의 화살표를 A로 향하게 한다.
        if card.is_head: # 현재 카드가 head였다면
            beforeListNextCard.is_head = True # 다음 카드를 head로 만든다.
        if (data.get('prev')==None) or (data.get('prev')==""): # 받아온 prev가 없으면
            card.is_head=True # card를 head에 두고
            afterListNextCard = Card.objects.get(list=list, is_head=True) # 원래 head에 있던 카드를 찾는다
            afterListNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
            card.prev = None # 마지막으로 B의 화살표를 E로 향하게 한다.
        else: # 받아온 prev가 있으면
            afterListPrevCard = Card.objects.get(id=data.get('prev'))  # E를 찾는다
            afterListNextCard = Card.objects.get(prev=afterListPrevCard)  # F를 찾는다.
            afterListNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
            card.prev = afterListPrevCard  # 마지막으로 B의 화살표를 E로 향하게 한다.
            afterListPrevCard.save()
        beforeListNextCard.save()
        afterListNextCard.save()

    def change_order_of_card(self, card, data):
        beforeNextCard = Card.objects.get(prev=card.id)  # 다음 카드인 C 를 받아온다
        beforeNextCard.prev = card.prev  # C의 화살표를 A로 향하게 한다.
        afterPrevCard = Card.objects.get(id=data.get('prev'))  # E를 찾는다
        afterNextCard = Card.objects.get(prev=afterPrevCard)  # F를 찾는다.
        afterNextCard.prev = card  # F의 화살표를 B 로 향하게 한다.
        card.prev = afterPrevCard  # 마지막으로 B의 화살표를 E로 향하게 한다.
        beforeNextCard.save()
        afterPrevCard.save()
        afterNextCard.save()

    def update(self, card_id, data):
        card = Card.objects.get(id=card_id)
        creator = card.creator
        #create activity.
        if data.get('name'): card.name = data.get('name')
        if data.get('description'): card.description = data.get('description')
        if data.get('due_date'): card.due_date = data.get('due_date')
        if data.get('list') and data.get('prev'):
            self.change_list_of_card(self, card, data)
        elif data.get('prev') and not(data.get('list')):
            self.change_order_of_card(self, card, data)

        card.save()

    def create_activity(self, card, data):
        creator = card.creator
        member = User.objects.get(id=data.get('member'))

        UserCard.objects.create(user=member, card=card)

        if card.creator==member:
            content = creator.username + "joined this card"
        else:
            content = creator + " added " + member.username + " to this card"

        Activity.objects.create(creator=creator, content=content, card=card, is_comment=False)


    def create_activity(self, card):
        creator = card.creator
        content = creator.username + " added this card to " + card.list.name
        Activity.objects.create(creator=creator, content=content, card=card, is_comment=False)

    def delete(self, card_id):
        card = Card.objects.get(id=card_id)
        card.delete()

class BasicCardSerializer(CardSerializer):
    class Meta:
        model = Card
        fields=(
                'prev',
                'list',
                'name',
                'members',
                'description',
                'due_date',
                'created_at'
            )



