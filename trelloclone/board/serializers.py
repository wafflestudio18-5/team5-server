from rest_framework import serializers
from trelloclone.list.models import List
from trelloclone.card.models import Card
from trelloclone.board.models import Board
from trelloclone.list.serializers import ListSerializer
from trelloclone.card.serializers import BasicCardSerializer

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
            returnquery=List.objects.all().filter(id=prevlist.id)
            if prevlist:
                returnquery|=listlistrec(prevlist)
            return returnquery
        if firstlist:
            fullquery=listlistrec(firstlist)
            return ListSerializer(fullquery,many=True)
        else:
            return []
    def create(self,data):
        Board = super(BoardSerializer, self).create(data)
        headlist = List.objects.create(is_head=True)
        Board.head = headlist
        Board.save()
        return Board