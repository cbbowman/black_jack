from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=CASCADE)
	games_played=models.PositiveSmallIntegerField(default=0)
	money_spent=models.PositiveSmallIntegerField(default=0)
	winnings=models.SmallIntegerField(default=0)
