from django.db import models
from django.contrib.auth.models import User
from list.models import List


class Board(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    key = models.CharField(max_length=10, null=True)
    head = models.ForeignKey(List, related_name='board_head', on_delete=models.CASCADE)
    star = models.BooleanField(default=False)

class UserBoard(models.Model):
    user = models.ForeignKey(User, related_name='user_board', on_delete=models.CASCADE)
    board = models.ForeignKey(Board, related_name='user_board', on_delete=models.CASCADE)
    star = models.BooleanField(default=False)

