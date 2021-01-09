from django.db import models
from django.contrib.auth.models import User
from django.utils import dateformat, timezone

class Card(models.Model):
    name = models.CharField(max_length=30, db_index=True, null=False)
    description = models.TextField(db_index=True, null=True)
    due_date = models.DateTimeField(auto_now=False, blank=True,null=True)
    created_at = models.CharField(max_length=30, blank=True)
    is_head = models.BooleanField(default=False)
    key = models.CharField(max_length=10, null=True)
    creator = models.ForeignKey(User, related_name='card_creator', on_delete=models.DO_NOTHING,null=True)
    list = models.ForeignKey('list.List', related_name='card_list', on_delete=models.CASCADE,null=True)
    board = models.ForeignKey('board.Board', related_name='card_board', on_delete=models.CASCADE,null=True)
    prev = models.OneToOneField('self', related_name='next', on_delete=models.SET(None),null=True)

class UserCard(models.Model):
    user = models.ForeignKey(User, related_name='user_card', on_delete=models.DO_NOTHING)
    card = models.ForeignKey(Card, related_name='user_card', on_delete=models.DO_NOTHING)




