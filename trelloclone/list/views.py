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
            createdlist=List.objects.create(name=name,head=headcard,board=board)
            befprev=headlist.prev
            headlist.prev=createdlist
            createdlist.prev=befprev
            headlist.save()
            createdlist.save()
            return Response(self.get_serializer(createdlist).data,status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'unathorized'},status=status.HTTP_403_FORBIDDEN)

    def put(self,request):
        user=request.user  # board 에속한 user인지 어떻게 확인하지..?
        list_id=request.data.get('list_id')
        board_id=request.data.get('board_id')
        name=request.data.get('name')
        prev_id=request.data.get('prev_id')
        if not list_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            listtochange=List.objects.get(id=list_id)
        except List.DoesNotExist:
            return Response({'error':'list not found'},status=status.HTTP_404_NOT_FOUND)
        if listtochange.is_head:
            return Response({'error':'cannot change head list'},status=status.HTTP_400_BAD_REQUEST)
            
        if board_id:
            if(listtochange.board.id != int(board_id)):
                return Response({'error':'list does not belong to that board'},status=status.HTTP_400_BAD_REQUEST)
            boardto=Board.objects.get(id=board_id)
            if not boardto:
                return Response({'error':'Board not found'},status=status.HTTP_404_NOT_FOUND)
            if not prev_id:
                if listtochange.prev is not None:
                    try:
                        endlist=List.objects.get(board=boardto,prev=None)
                    except List.DoesNotExist:
                        return Response({'error':'db data error: endlist not found'},status=status.HTTP_404_NOT_FOUND)
                    fprev=listtochange.prev
                    fnext=listtochange.next
                    fnext.prev=fprev
                    listtochange.prev=None
                    listtochange.save()
                    fnext.save()

                    endlist.prev=listtochange
                    endlist.save()
            else:
                if listtochange.prev is None or prev_id is not listtochange.prev.id:
                    try:
                        tprev=List.objects.get(id=prev_id,board=boardto)
                    except List.DoesNotExist:
                        return Response({'error':'prev list not found'},status=status.HTTP_404_NOT_FOUND)
                    fprev=listtochange.prev
                    fnext=listtochange.next
                    tprevnext=tprev.next
                    fnext.prev=fprev
                    listtochange.prev=None
                    listtochange.save()
                    fnext.save()
                    tprevnext.prev=listtochange
                    tprevnext.save()
                    listtochange.prev=tprev
                    listtochange.save()

        if name:
            listtochange.name=name
            listtochange.save()
        
        return Response(self.get_serializer(listtochange).data,status=status.HTTP_200_OK)
    
    def delete(self, request):
        user = request.user
        list_id = request.data.get('id')
        if not list_id:
             return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            todelete = List.objects.get(id=list_id)
        except List.DoesNotExist:
            return Response({'error':'list not found'},status=status.HTTP_404_NOT_FOUND)
        if todelete.is_head:
            return Response({'error':'cannot delete head list'},status=status.HTTP_403_FORBIDDEN)
        prevlist=todelete.prev
        nextlist=todelete.next
        nextlist.prev=prevlist
        todelete.delete()
        nextlist.save()
        
        return Response(status=status.HTTP_200_OK)

    def get(self,request):
        list_id = request.data.get('id')
        if not list_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            listobj=List.objects.get(id=list_id)
        except List.DoesNotExist:
            Response({'error':'List does not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response(self.get_serializer(listobj).data,status=status.HTTP_200_OK)


# Create your views here.
