from rest_framework import serializers
from list.models import List
from card.models import Card
from card.serializers import BasicCardSerializer

class ListSerializer(serializers.ModelSerializer):
    cards=serializers.SerializerMethodField()
    class Meta:
        model=List
        fields=(
            'id',
            'name',
            'cards',
        )

    def get_cards(self,listobj):
        headcard=listobj.head
        firstcard=headcard.prev
        def cardlistrec(card):
            prevcard=card.prev
            returnquery=Card.objects.get(id=prevcard.id)
            if prevcard:
                returnquery|=cardlistrec(prevcard)
            return returnquery
        if firstcard:
            fullquery=cardlistrec(firstcard)
            return BasicCardSerializer(fullquery,many=True)
        else:
            return []

    def create(self,data):
        List = super(ListSerializer, self).create(data)
        headcard = Card.objects.create(is_head=True)
        List.head = headcard
        List.save()
        return List


