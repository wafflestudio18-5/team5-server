from django.shortcuts import render

# Create your views here.
from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from card.models import UserCard, Card
from card.serializers import CardSerializer, BasicCardSerializer, SimpleCardSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CardViewSet(viewsets.GenericViewSet):
    queryset = Card.objects.all()
    serializer_class = SimpleCardSerializer

    def create(self, request):
        data = request.data
        if not request.data.get('name'):
            return Response({"error": "Enter the name."},status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    def retrieve(self, request, pk=None):
        id = request.get('card_id')
        card_obj = self.queryset.get(id=id)
        return Response(self.get_serializer(card_obj).data)

    def delete(self, request):
        id = request.get('card_id')
        self.serializer_class.delete(self, id)
        return Response(status=status.HTTP_200_OK)




