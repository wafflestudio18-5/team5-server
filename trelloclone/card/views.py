from django.shortcuts import render

# Create your views here.

from rest_framework import status, viewsets
from django.contrib.auth.models import User
from card.models import UserCard, Card
from card.serializers import CardSerializer, BasicCardSerializer, SimpleCardSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from list.models import List

class CardViewSet(viewsets.GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = SimpleCardSerializer

    def create(self, request):
        user=request.user
        data = request.data
        name=request.data.get('name')
        list_id=request.data.get('list_id')
        if not name or not list_id:
            return Response({"error": "missing request data."},status=status.HTTP_400_BAD_REQUEST)
        listobj=List.objects.get(id=list_id)
        if not listobj:
            return Response({"error": "list not found"},status=status.HTTP_400_BAD_REQUEST)

        createdcard=Card.objects.create(name=name,list=listobj)
        return Response(self.get_serializer(createdcard).data, status=status.HTTP_201_CREATED)

    ##############################################################

    def update(self, request, pk=None):
        card = self.get_object()
        # Q. 만약 다른 보드의 유저가 교체를 희망하는 경우도 넣어야 하나? 그게 사이트 입장에서 가능한가?
        # creator = request.user
        # if card.creator!=creator:
        #    return Response({"error": ""})
        data = request.data
        serializer = self.get_serializer(card, data=data, partial=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self,request):
        card_id=request.data.get('id')
        if not card_id:
            return Response({"error": "missing request data."},status=status.HTTP_400_BAD_REQUEST)
        cardobj=Card.objects.get(id=card_id)
        if not cardobj:
            return Response({"error": "card not found"},status=status.HTTP_404_NOT_FOUND)
        return Response(CardSerializer(cardobj).data,status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.get('card_id')
        self.serializer_class.delete(self, id)
        return Response(status=status.HTTP_200_OK)
    





