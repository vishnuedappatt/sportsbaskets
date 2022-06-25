
from django.db import models

from user.models import Account


# Create your models here.


class BlockedUser(models.Model):
    phone=models.CharField(max_length=15)


    def __str__(self):
        return self.phone