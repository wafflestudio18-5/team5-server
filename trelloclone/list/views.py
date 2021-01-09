from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from board.models import Board, UserBoard
from list.models import List
from list.serializers import ListSerializer
from rest_framework.decorators import action
from card.models import Card
from itertools import chain

class ListViewSet(viewsets.GenericViewSet):
    queryset = List.objects.all()
    serializer_class=ListSerializer

    def create(self,request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        board_id=request.data.get('board_id')
        name=request.data.get('name')
        if not board_id or not name:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board=Board.objects.get(id=board_id)
        headlist=board.head

        auth = False
        try:
            userboard=UserBoard.objects.filter(user=user,board=board)
            if userboard : auth = True
        except :
            pass

        if auth==True:
            headcard = Card.objects.create(is_head=True,board=board)
            createdlist=List.objects.create(name=name,head=headcard,board=board)
            
            befprev=headlist.prev
            headlist.prev=createdlist
            createdlist.prev=befprev
            headlist.save()
            createdlist.save()
            headcard.list=createdlist
            headcard.save()
            return Response(self.get_serializer(createdlist).data,status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'You have no permission to that board.'},status=status.HTTP_403_FORBIDDEN)

    def put(self,request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        list_id=request.data.get('list_id')
        board_id=request.data.get('board_id')
        name=request.data.get('name')
        prev_id=request.data.get('prev_id')
        if not list_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            listtochange=List.objects.get(id=list_id)
        except List.DoesNotExist:
            return Response({'error':'list not found'},status=status.HTTP_400_BAD_REQUEST)
        if listtochange.is_head:
            return Response({'error':'cannot change head list'},status=status.HTTP_400_BAD_REQUEST)

        bdcheck = listtochange.board
        try:
            ub = UserBoard.objects.get(user=user, board=bdcheck)
        except UserBoard.DoesNotExist:
            return Response({'error': 'You have no permission to access that board'}, status=status.HTTP_403_FORBIDDEN)

        if board_id:
            if(listtochange.board.id != int(board_id)):
                return Response({'error':'list does not belong to that board'},status=status.HTTP_400_BAD_REQUEST)
            boardto=Board.objects.get(id=board_id)
            if not boardto:
                return Response({'error':'Board not found'},status=status.HTTP_400_BAD_REQUEST)
            if not prev_id:
                if (listtochange.prev is not None) or (listtochange.board is not boardto):
                    try:
                        endlist=List.objects.get(board=boardto,prev=None)
                    except List.DoesNotExist:
                        return Response({'error':'db data error: endlist not found'},status=status.HTTP_400_BAD_REQUEST)
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
                        return Response({'error':'prev list not found'},status=status.HTTP_400_BAD_REQUEST)
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
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        list_id = request.data.get('id')
        if not list_id:
             return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            todelete = List.objects.get(id=list_id)
        except List.DoesNotExist:
            return Response({'error':'list not found'},status=status.HTTP_400_BAD_REQUEST)
        if todelete.is_head:
            return Response({'error':'cannot delete head list'},status=status.HTTP_400_BAD_REQUEST)

        board = todelete.board
        try:
            ub = UserBoard.objects.get(user=user, board=board)
        except UserBoard.DoesNotExist:
            return Response({'error': 'You have no permission to access that board'}, status=status.HTTP_403_FORBIDDEN)

        prevlist=todelete.prev
        nextlist=todelete.next
        nextlist.prev=prevlist
        todelete.prev=None
        todelete.save()
        nextlist.save()
        todelete.delete()
        return Response(status=status.HTTP_200_OK)

    def get(self,request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        list_id = request.data.get('id')
        if not list_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            listobj=List.objects.get(id=list_id)
        except List.DoesNotExist:
            Response({'error':'List does not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response(self.get_serializer(listobj).data,status=status.HTTP_200_OK)
