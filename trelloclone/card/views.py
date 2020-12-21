from django.shortcuts import render

# Create your views here.
from django.db import transaction
from django.utils import timezone
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from card.models import UserCard, Card
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class CardViewSet(viewsets.GenericViewSet):

    def update(self, request, pk=None):
        user = request.user
        card = self.get_object()
        data = request.data
        serializer = self.get_serializer(card, data=data, partial=True)

        if data.get('member'):
            id=data.get('member')
            user = User.objects.get(id=id)
            UserCard.object.create(user=user, card=card)
