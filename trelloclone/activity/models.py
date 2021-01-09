from django.db import models
from card.models import Card
from django.contrib.auth.models import User
from django.utils import dateformat, timezone

class Activity(models.Model):
    creator = models.ForeignKey(User, related_name='activity_creator', on_delete=models.CASCADE)
    content = models.CharField(max_length=500, db_index=True, null=True)
    created_at = models.CharField(max_length=30, blank=True)
    card = models.ForeignKey('card.Card', related_name='activity_card', on_delete=models.CASCADE)
    is_comment = models.BooleanField(default=False)