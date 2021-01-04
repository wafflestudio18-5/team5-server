from django.db import models
#from card.models import Card


class List(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    board = models.ForeignKey('board.Board', related_name='list_board', on_delete=models.CASCADE, null=True)
    prev = models.OneToOneField('self',related_name='next', on_delete=models.SET(None),null=True)
    head = models.ForeignKey('card.Card', related_name='list_in', on_delete=models.CASCADE,null=True) # 어차피 head가 지워질일은 리스트 삭제할때밖에 없음.
    #head = models.ForeignKey(Card, related_name='list_in') # 순환참조때문에 고침.
    is_head = models.BooleanField(default=False)
