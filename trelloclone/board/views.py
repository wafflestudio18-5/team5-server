from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from board.models import Board, UserBoard
from list.models import List
from board.serializers import BoardSerializer, UserBoardSerializer
from rest_framework.decorators import action
# from django.contrib.auth.models import User
from user.serializers import UserSerializer
from django.contrib.auth.models import User

class BoardViewSet(viewsets.GenericViewSet):
    
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def create(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        name = request.data.get('name')
        if not name:
            return Response({'error': 'missing request data'}, status=status.HTTP_400_BAD_REQUEST)
        headlist = List.objects.create(is_head=True)
        newboard = Board.objects.create(name=name, head=headlist)
        newboard.key = str(newboard.id).zfill(8)
        newboard.save()
        headlist.board=newboard
        headlist.save()
        UserBoard.objects.create(user=user, board=newboard, is_creator=True)
        return Response(self.get_serializer(newboard).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['GET'])
    def boardlist(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        boardlist = UserBoard.objects.filter(user=user).all()
        page = self.paginate_queryset(boardlist)
        serializer = UserBoardSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
        #return Response(UserBoardSerializer(boardlist, many=True).data, status=status.HTTP_200_OK)

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)

        board_key = request.GET.get('key')
        board_id = request.GET.get('id')

        if board_key:
            try:
                board = Board.objects.get(key=board_key)
            except Board.DoesNotExist:
                return Response({"error": "board not found"}, status=status.HTTP_400_BAD_REQUEST)

        elif board_id:
            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return Response({"error": "board not found"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'missing params data'}, status=status.HTTP_400_BAD_REQUEST)

        try :
            UserBoard.objects.get(user=user, board=board)
        except UserBoard.DoesNotExist:
            return Response({"error": "You are not permitted to access this board"}, status=status.HTTP_403_FORBIDDEN)

        return Response(self.get_serializer(board).data, status=status.HTTP_200_OK)


    def delete(self, request):
        user = request.user
        if not user.is_authenticated: # 1. check login
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        board_id = request.data.get('id')
        if not board_id: # 2. check data
            return Response({'error': 'missing request data'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist: # 3. check db
            return Response({'error': 'Board does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        try :
            ub = UserBoard.objects.get(user=user, board=board)
        except UserBoard.DoesNotExist: # 4. check user belongs to the board
            return Response({"error": "You are not permitted to access this board"}, status=status.HTTP_403_FORBIDDEN)
        if ub.is_creator == False: # 5. check user is creator.
            return Response({"error": "You are not permitted to delete this board"}, status=status.HTTP_403_FORBIDDEN)

        board.delete()
        return Response(status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'])
    def invite(self, request):
        board_id = request.data.get('id')
        username = request.data.get('username')
        if not board_id or not username:
            return Response({'error': 'missing request data'}, status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error': 'Board does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            userboard = UserBoard.objects.get(user=user, board=board)
        except UserBoard.DoesNotExist:
            return Response({"error": "You are not permitted to access this board"}, status=status.HTTP_403_FORBIDDEN)
        try:
            usertoinvite = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        dup_error = False
        try:
            duplicate_check = UserBoard.objects.get(user=usertoinvite, board=board)
            if duplicate_check: dup_error = True
        except:
            pass
        if dup_error:
            return Response({'error': 'That user is already in the board'}, status=status.HTTP_400_BAD_REQUEST)

        UserBoard.objects.create(user=usertoinvite, board=board)
        return Response(UserSerializer(usertoinvite).data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'])
    def userlist(self, request):
        board_id = request.GET.get('board_id')
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        if not board_id:
            return Response({'error': 'missing board_id (enter params)'}, status=status.HTTP_400_BAD_REQUEST)
        board = Board.objects.get(id=board_id)
        if not board:
            Response({'error': 'Board does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        UBlist = UserBoard.objects.filter(board=board).all()
        userlist = User.objects.filter(user_board__in=UBlist).all()

        page = self.paginate_queryset(userlist)
        serializer = UserSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
        #return Response(UserSerializer(userlist, many=True).data, status=status.HTTP_200_OK)


    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        board_id = request.data.get('id')
        if not board_id:
            return Response({'error': 'missing request data'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            board = Board.objects.get(id=board_id)
        except Board.DoesNotExist:
            Response({'error': 'Board does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ub = UserBoard.objects.get(board=board, user=user)
        except UserBoard.DoesNotExist:
            Response({'error': 'You have no access to this board'}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get('name')
        if name:
            board.name = name
        star = request.data.get('star')
        if star == "True" or star == "true":
            ub.star=True
            ub.save()
        elif star == "False" or star == "false":
            ub.star=False
            ub.save()
        board.save()
        return Response(self.get_serializer(board,context={'request': request}).data, status=status.HTTP_200_OK)

# Create your views here.
