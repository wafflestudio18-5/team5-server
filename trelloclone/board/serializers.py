from rest_framework import serializers
from list.models import List
from card.models import Card
from board.models import Board
from list.serializers import ListSerializer
from card.serializers import BasicCardSerializer

class BoardSerializer(serializers.ModelSerializer):
    lists=serializers.SerializerMethodField()
    class Meta:
        model=List
        fields=(
            'id',
            'name',
            'lists',
        )
    def get_lists(self,boardobj):
        headlist=boardobj.head
        firstlist=headlist.prev
        def listlistrec(listobj):
            prevlist=listobj.prev
            returnquery=List.objects.filter(id=listobj.id).all()
            if prevlist:
                returnquery|=listlistrec(prevlist)
            return returnquery
        if firstlist:
            fullquery=listlistrec(firstlist)
            return ListSerializer(fullquery,many=True).data
        else:
            return []