from django.db import models
from django.contrib.auth.models import User


class Card(models.Model):
    name = models.CharField(max_length=30, db_index=True, null=False)
    description = models.TextField(db_index=True, null=True)
    due_date = models.DateTimeField(auto_now=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_head = models.BooleanField(default=False)

    creator = models.ForeignKey(User, related_name='card_creator', on_delete=models.DO_NOTHING)
    list = models.ForeignKey('list.List', related_name='card_list', on_delete=models.CASCADE)
    board = models.ForeignKey('board.Board', related_name='card_board', on_delete=models.CASCADE)
    prev = models.ForeignKey('self', related_name='next', on_delete=models.DO_NOTHING)

class UserCard(models.Model):
    user = models.ForeignKey(User, related_name='user_card', on_delete=models.DO_NOTHING)
    card = models.ForeignKey(Card, related_name='user_card', on_delete=models.DO_NOTHING)



