from django.db import models
from trelloclone.board.models import Board


class List:
    name = models.CharField(max_length=30, db_index=True)
    board = models.ForeignKey(Board, related_name='list_board', on_delete=models.CASCADE)
    next = models.ForeignKey('self')
