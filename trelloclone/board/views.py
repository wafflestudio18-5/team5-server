from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from board.models import Board, UserBoard
from list.models import List
from board.serializers import BoardSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from user.serializers import UserSerializer

class BoardViewSet(viewsets.GenericViewSet):
    serializer_class=BoardSerializer
    def create(self, request):
        user=request.user
        name=request.data.get('name')
        if not name:
            Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        newboard = Board.objects.create(name=name)
        UserBoard.objects.create(user=user,board=newboard)
        return Response(self.get_serializer(newboard).data,status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def boardlist(self,request):
        user = request.user
        boardlist = UserBoard.objects.filter(user=user).all()
        return Response(self.get_serializer(boardlist,many=True).data,status=status.HTTP_200_OK)

    def get(self,request):
        board_id = request.data.get("id")
        board_key = request.data.get("key")
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
    
    def userlist(self,request):
        user=request.user
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error':'Board does not exist'},status=status.HTTP_400_BAD_REQUEST)
        UBlist = UserBoard.objects.filter(user=user).all()
        userlist=User.objects.filter(User_board__in=UBlist).all()
        return Response(UserSerializer(userlist,many=True).data,status=status.HTTP_200_OK)
    
    def update(self,request):
        user=request.user
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error':'missing request data'},status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error':'Board does not exist'},status=status.HTTP_400_BAD_REQUEST)
        
        name = request.data.get('name')
        if name:
            board.name=name
        star = request.data.get('star')
        if star:
            board.star=star
        board.save()
        return Response(BoardSerializer(board).data,status=status.HTTP_200_OK)
    
# Create your views here.
