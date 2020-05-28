from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Room(models.Model):
    session_string = models.UUIDField(default=uuid.uuid4, editable=False)
    create_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    pass


class ChatLine(models.Model):
    message_content = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    create_datetime = models.DateTimeField()
