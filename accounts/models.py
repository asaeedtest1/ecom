from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Profile of {self.user.username}"
