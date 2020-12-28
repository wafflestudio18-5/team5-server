from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from board.models import Board, UserBoard
from list.models import List
from board.serializers import BoardSerializer
from rest_framework.decorators import action
# from django.contrib.auth.models import User
from user.serializers import UserSerializer
from django.contrib.auth.models import User

class BoardViewSet(viewsets.GenericViewSet):
    serializer_class=BoardSerializer
    def create(self, request):
        user=request.user
        if not user.is_authenticated:
            return Response({'error':'not logged in'},status=status.HTTP_403_FORBIDDEN)
        name=request.data.get('name')
        if not name:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        headlist = List.objects.create(is_head=True)
        newboard = Board.objects.create(name=name,head=headlist)
        UserBoard.objects.create(user=user,board=newboard)
        return Response(self.get_serializer(newboard).data,status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def boardlist(self,request):
        user = request.user
        boardlist = UserBoard.objects.filter(user=user).all()
        return Response(self.get_serializer(boardlist,many=True).data,status=status.HTTP_200_OK)

    def get(self,request):
        board_id = request.data.get('id')
        board_key = request.data.get('key')
        
        if board_id and board_key:
            Response({'error':'too many arguments'},status=status.HTTP_400_BAD_REQUEST)
        elif board_id:
            board = Board.objects.get(id=board_id)
        elif board_key:
            board = Board.objects.get(key=board_key)
        else:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        if not board:
            Response({'error':'Board does not exist'},status=status.HTTP_400_BAD_REQUEST)
            
        return Response(self.get_serializer(board).data,status=status.HTTP_200_OK)
    
    def delete(self,request):
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error':'Board does not exist'},status=status.HTTP_400_BAD_REQUEST)
        board.delete()
        return Response(status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['POST'])
    def invite(self,request):
        board_id = request.data.get('id')
        username = request.data.get('username')
        if not board_id or not username:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error':'Board does not exist'},status=status.HTTP_400_BAD_REQUEST)
        user=request.user
        userboard = UserBoard.objects.get(user=user,board=board)
        if not userboard:
            return Response({'error':'unathorized'},status=status.HTTP_403_FORBIDDEN)
        usertoinvite = User.objects.get(username=username)
        if not usertoinvite:
            Response({'error':'User does not exist'},status=status.HTTP_400_BAD_REQUEST)
        UserBoard.objects.create(user=usertoinvite,board=board)
        return Response(UserSerializer(usertoinvite).data,status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'])
    def userlist(self,request):
        user=request.user
        board_id = request.data.get('id')
        if not user.is_authenticated:
            return Response({'error':'not logged in'},status=status.HTTP_403_FORBIDDEN)
        if not board_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error':'Board does not exist'},status=status.HTTP_400_BAD_REQUEST)
        UBlist = UserBoard.objects.filter(board=board).all()
        userlist=User.objects.filter(user_board__in=UBlist).all()
        return Response(UserSerializer(userlist,many=True).data,status=status.HTTP_200_OK)
    
    def put(self,request):
        user=request.user
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            Response({'error':'Board does not exist'},status=status.HTTP_404_NOT_FOUND)
        
        try:
            ub=UserBoard.objects.get(board=board,user=user)
        except UserBoard.DoesNotExist:
            Response({'error':'You have no access to this board'},status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        if name:
            board.name=name
        star = request.data.get('star')
        if star:
            ub.star=star
            ub.save()
        board.save()
        return Response(BoardSerializer(board).data,status=status.HTTP_200_OK)
    
# Create your views here.
