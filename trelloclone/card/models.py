from django.db import models
from django.contrib.auth.models import User
from trelloclone.board.models import Board
from trelloclone.list.models import List


class Card:
    name = models.CharField(max_length=30, db_index=True)
    description = models.TextField(db_index=True)
    duedate = models.DateTimeField(auto_now=True, null=True)

    list = models.ForeignKey(List, related_name='card_list', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='card_board', on_delete=models.CASCADE)
    card = models.ForeignKey('self')
