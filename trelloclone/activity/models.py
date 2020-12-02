from django.db import models
from trelloclone.card.models import Card


class Activity:
    content = models.CharField(max_length=200, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    card = models.ForeignKey(Card, related_name='activity_card', on_delete=models.CASCADE)
