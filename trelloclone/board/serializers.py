from rest_framework import serializers
from list.models import List
from card.models import Card
from board.models import Board
from list.serializers import ListSerializer
from card.serializers import BasicCardSerializer
from itertools import chain
class BoardSerializer(serializers.ModelSerializer):
    lists=serializers.SerializerMethodField()
    class Meta:
        model=Board
        fields=(
            'id',
            'name',
            'lists',
        )
    def get_lists(self,boardobj):
        listquery=List.objects.filter(board=boardobj).all()
        headlist=boardobj.head
        firstlist=headlist.prev
        def listlistrec(listobj):
            prevlist=listobj.prev
            returnquery=listquery.filter(id=listobj.id).all()
            if prevlist:
                returnquery=list(chain(listlistrec(prevlist),returnquery))
            return returnquery
        if firstlist:
            fullquery=listlistrec(firstlist)
            return ListSerializer(fullquery,many=True).data
        else:
            return []
    