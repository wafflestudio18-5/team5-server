from django.shortcuts import render

# Create your views here.

from rest_framework import status, viewsets
from django.contrib.auth.models import User
from card.models import UserCard, Card
from card.serializers import CardSerializer, BasicCardSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from list.models import List
from board.models import Board,UserBoard
from activity.models import Activity
from django.utils import dateformat, timezone


class CardViewSet(viewsets.GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def create(self, request):
        user=request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        name=request.data.get('name')
        list_id=request.data.get('list_id')
        if not name or not list_id:
            return Response({"error": "missing request data."},status=status.HTTP_400_BAD_REQUEST)
        listobj=List.objects.get(id=list_id)
        if not listobj:
            return Response({"error": "list not found"},status=status.HTTP_400_BAD_REQUEST)
        boardobj=listobj.board
        ub=UserBoard.objects.get(user=user,board=boardobj)
        if not ub:
            return Response({"error": "Not authorized to create in this board"},status=status.HTTP_403_FORBIDDEN)
        card_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        createdcard=Card.objects.create(name=name,list=listobj,creator=user,board=listobj.board, created_at=card_date)
        createdcard.key=str(createdcard.id).zfill(8)
        headcard=listobj.head
        befprev=headcard.prev
        headcard.prev=createdcard
        createdcard.prev=befprev
        headcard.save()
        contentdt=" added this card to "+listobj.name

        activity_date = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
        cact=Activity.objects.create(creator=user,card=createdcard,content=contentdt, created_at =activity_date)
        createdcard.save()
        
        return Response(self.get_serializer(createdcard).data, status=status.HTTP_201_CREATED)

    ##############################################################

    def put(self, request):
        user=request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        card_id=request.data.get('id')
        member=request.data.get('member')
        name=request.data.get('name')
        description=request.data.get('description')
        due_date=request.data.get('due_date')
        prev_id=request.data.get('prev_id')
        list_id=request.data.get('list_id')

        if not card_id:
            return Response({"error": "missing request data."},status=status.HTTP_400_BAD_REQUEST)
        try:
            cardobj=Card.objects.get(id=card_id)
        except Card.DoesNotExist:
            return Response({"error": "card not found"},status=status.HTTP_400_BAD_REQUEST)
        
        if cardobj.is_head:
            return Response({'error':'cannot change head card'},status=status.HTTP_400_BAD_REQUEST)

        if member:
            try:
                toinvite=User.objects.get(username=member)
            except User.DoesNotExist:
                return Response({"error": "User not found"},status=status.HTTP_400_BAD_REQUEST)

            dup_error=False
            try:
                dup = UserCard.objects.get(card=cardobj, user=toinvite)
                if dup: dup_error=True
            except:
                pass
            if dup_error:
                return Response({"error": "That user is already the member of this card"}, status=status.HTTP_400_BAD_REQUEST)

            addcontent= " added "+toinvite.username+" to this card"
            if toinvite is user:
                addcontent= "joined this card"
            addact=Activity.objects.create(creator=user,card=cardobj,content=addcontent)
            uc=UserCard.objects.create(user=toinvite,card=cardobj)

        if due_date:
            cardobj.due_date=due_date
        if name:
            cardobj.name=name
        if description:
            cardobj.description=description
        beflist=cardobj.list
        if list_id:
            try:
                listobj=List.objects.get(id=list_id)
            except List.DoesNotExist:
                return Response({"error": "list not found"},status=status.HTTP_400_BAD_REQUEST)

            if not prev_id:
                if (cardobj.prev is not None) or (beflist is not list_id):
                    try:
                        endcard=Card.objects.get(list=listobj,prev=None)
                    except Card.DoesNotExist:
                        return Response({"error": "db error: first card not found"},status=status.HTTP_400_BAD_REQUEST) # 이론상 발생할 수 없음
                    fprev=cardobj.prev
                    fnext=cardobj.next
                    fnext.prev=fprev
                    cardobj.prev=None
                    cardobj.save()
                    fnext.save()
                    endcard.prev=cardobj
                    endcard.save()

            else:
                if cardobj.prev is None or prev_id is not cardobj.prev.id:
                    try:
                        tprev=Card.objects.get(id=prev_id,list=listobj)
                    except Card.DoesNotExist:
                        return Response({'error':'prev list not found'},status=status.HTTP_400_BAD_REQUEST)
                    fprev=cardobj.prev
                    fnext=cardobj.next
                    tprevnext=tprev.next
                    fnext.prev=fprev
                    cardobj.prev=None
                    cardobj.save()
                    fnext.save()
                    tprevnext.prev=cardobj
                    tprevnext.save()
                    cardobj.prev=tprev
                    cardobj.save()
                    
            if list_id is not beflist.id:
                cardobj.list = listobj
                ctt=" moved this card from "+beflist.name+" to "+listobj.name
                mact=Activity.objects.create(creator=user,card=cardobj,content=ctt)
        cardobj.save()
        return Response(CardSerializer(cardobj).data,status=status.HTTP_200_OK)


    def get(self,request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        card_id = request.GET.get('id')
        card_key = request.GET.get('key')
        if card_key:
            try:    
                cardobj=Card.objects.get(key=card_key)
            except Card.DoesNotExist:
                return Response({"error": "Card not found"},status=status.HTTP_400_BAD_REQUEST)
        elif card_id:
            try:
                cardobj=Card.objects.get(id=card_id)
            except Card.DoesNotExist:
                return Response({"error": "Card not found"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "missing request data."},status=status.HTTP_400_BAD_REQUEST)
        return Response(CardSerializer(cardobj).data,status=status.HTTP_200_OK)

    def delete(self, request):
        user=request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        card_id = request.data.get('id')
        if not card_id:
            return Response({"error": "missing request data."},status=status.HTTP_400_BAD_REQUEST)
        try:
            cardobj=Card.objects.get(id=card_id)
        except Card.DoesNotExist:
            return Response({"error": "card not found"},status=status.HTTP_400_BAD_REQUEST)
        if cardobj.is_head:
            return Response({"error": "cannot delete head card"},status=status.HTTP_403_FORBIDDEN)

        prevcard=cardobj.prev
        nextcard=cardobj.next
        nextcard.prev=prevcard
        cardobj.prev=None
        cardobj.save()
        nextcard.save()
        cardobj.delete()
        
        return Response(status=status.HTTP_200_OK)
    





