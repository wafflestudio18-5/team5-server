from rest_framework import serializers
from list.models import List
from card.models import Card
from card.serializers import BasicCardSerializer

class ListSerializer(serializers.ModelSerializer):
    cards=serializers.SerializerMethodField()
    card_count=serializers.SerializerMethodField()
    class Meta:
        model=List
        fields=(
            'id',
            'name',
            'card_count',
            'cards',
        )
    def get_card_count(self,listobj):
        cardlist=Card.objects.filter(list=listobj).all()
        cardnum=cardlist.count()
        return cardnum

    def get_cards(self,listobj):
        headcard=listobj.head
        firstcard=headcard.prev
        def cardlistrec(cardobj):
            prevcard=cardobj.prev
            returnquery=Card.objects.get(id=cardobj.id)
            if prevcard:
                returnquery|=cardlistrec(prevcard)
            return returnquery
        if firstcard:
            fullquery=cardlistrec(firstcard)
            return BasicCardSerializer(fullquery,many=True).data
        else:
            return []

    


