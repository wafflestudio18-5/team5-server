from django.db import models
from card.models import Card
from django.contrib.auth.models import User

class Activity:
    creator = models.ForeignKey(User, related_name='activity_creator', on_delete=models.CASCADE)
    content = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    card = models.ForeignKey(Card, related_name='activity_card', on_delete=models.CASCADE)
