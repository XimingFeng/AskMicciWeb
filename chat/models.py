from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

# Create your models here.


class Room(models.Model):
    session_str = models.UUIDField(default=uuid.uuid4().hex, editable=False, unique=True)
    create_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=False)

    def __str__(self):
        start = datetime.datetime.strftime(self.create_datetime, "%Y-%m-%d %I: %m %p")
        end = datetime.datetime.strftime(self.end_datetime, "%Y-%m-%d %I: %m %p")
        return_str = "Room session: {} \n Created date time: {} \n End date time: {}"\
            .format(self.session_str, start, end)
        return return_str


class ChatLine(models.Model):
    message_content = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    create_datetime = models.DateTimeField()

    def __str__(self):
        start = datetime.datetime.strftime(self.create_datetime, "%Y-%m-%d %I: %m %p")
        return_str = "Message content: {} \n Room session: {} \n Created user: {} \n Created date time: {} "\
            .format(self.message_content, self.room.session_string, self.user, start)
        return return_str
