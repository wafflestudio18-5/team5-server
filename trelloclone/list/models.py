from django.db import models
from trelloclone.board.models import Board
from trelloclone.card.models import Card


class List:
    name = models.CharField(max_length=30, db_index=True)
    board = models.ForeignKey(Board, related_name='list_board', on_delete=models.CASCADE)
    prev = models.ForeignKey('self',related_name='next')
    head = models.ForeignKey(Card, related_name='list_in')
    is_head = models.Boolean_field(default=False)
