from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from board.models import Board, UserBoard
from list.models import List
from list.serializers import ListSerializer
from django.core.paginator import Paginator
from rest_framework.decorators import action
from card.models import Card
class ListViewSet(viewsets.GenericViewSet):
    serializer_class=ListSerializer
    def create(self,request):
        user=request.user
        board_id=request.data.get('board_id')
        name=request.data.get('name')
        if not board_id or not name:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board=Board.objects.get(id=board_id)
        headlist=board.head
        userboard=UserBoard.objects.filter(user=user,board=board)
        if userboard:
            headcard = Card.objects.create(is_head=True)
            createdlist=List.objects.create(name=name,head=headcard)
            befprev=headlist.prev
            headlist.prev=createdlist
            createdlist.prev=befprev
            headlist.save()
            createdlist.save()
            return Response(self.get_serializer(createdlist).data,status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'unathorized'},status=status.HTTP_403_FORBIDDEN)

    def update(self,request):
        user=request.user  # board 에속한 user인지 어떻게 확인하지..?
        list_id=request.data.get('list_id')
        board_id=request.data.get('board_id')
        name=request.data.get('name')
        prev_id=request.data.get('prev_id')
        if not list_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)

        listtochange=List.objects.get(id=list_id)
        if prev_id:
            if not board_id:
                return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
            else:
                listprev=List.objects.get(id=prev_id)
                befnextlist=listtochange.next
                befnextlist.save()
                befnextlist.prev=listtochange.prev
                aftnextlist=listprev.prev
                listprev.prev=listtochange
                listtochange.prev=aftnextlist
                listprev.save()

        if name:
            listtochange.name=name
        listtochange.save()
        return Response(self.get_serializer(listtochange).data,status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        list_id = request.data.get('list_id')
        if not list_id:
             return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        todelete = List.objects.get(id=list_id)
        if not todelete:
            return Response({'error':'invalid request id'},status=status.HTTP_400_BAD_REQUEST)
        prevlist=todelete.prev
        nextlist=todelete.next
        nextlist.prev=prevlist
        nextlist.save()
        todelete.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self,request):
        list_id = request.data.get('id')
        if not list_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        listobj=List.objects.get(id=list_id)
        if not listobj:
            Response({'error':'List does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(listobj).data,status=status.HTTP_200_OK)


# Create your views here.
