from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    type = (
        ('OAUTH', 'PASSWORD'),
    )
    user = models.ForeignKey(User, related_name="user_profile", unique=True, on_delete=models.CASCADE)
    grantType = models.CharField(max_length=20, choices=type, db_index=True)