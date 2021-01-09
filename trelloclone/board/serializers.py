from rest_framework import serializers
from list.models import List
from card.models import Card
from board.models import Board,UserBoard
from list.serializers import ListSerializer
from card.serializers import BasicCardSerializer
from itertools import chain

class BoardSerializer(serializers.ModelSerializer):
    star=serializers.SerializerMethodField()
    lists=serializers.SerializerMethodField()
    class Meta:
        model=Board
        fields=(
            'id',
            'name',
            'star',
            'lists',
            'key',
        )
    def get_star(self,boardobj):
        user=self.context['request'].user
        try:
            ub=UserBoard.objects.get(board=boardobj,user=user)
        except:
            return None
        return ub.star
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
class UserBoardSerializer(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    name=serializers.SerializerMethodField()
    key=serializers.SerializerMethodField()
    class Meta:
        model=UserBoard
        fields=(
            'id',
            'name',
            'star',
            'key',
        )
    def get_id(self,UBobj):
        boardobj=UBobj.board
        return boardobj.id
    def get_name(self,UBobj):
        boardobj=UBobj.board
        return boardobj.name
    def get_key(self, UBobj):
        boardobj = UBobj.board
        return boardobj.key
