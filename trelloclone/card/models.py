from django.db import models
from django.contrib.auth.models import User
from board.models import Board
from list.models import List


class Card:
    name = models.CharField(max_length=30, db_index=True)
    description = models.TextField(db_index=True)
    due_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    creator = models.ForeignKey(User, related_name='card_creator', on_delete=models.DO_NOTHING)
    list = models.ForeignKey(List, related_name='card_list', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='card_board', on_delete=models.CASCADE)
    prev = models.ForeignKey('self')
