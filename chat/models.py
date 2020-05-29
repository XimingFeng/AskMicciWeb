from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Room(models.Model):
    session_string = models.UUIDField(default=uuid.uuid4, editable=False)
    create_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=False)

    def __str__(self):
        return_str = "Room session: {} \n Created date time: {} \n End date time: {}"\
            .format(self.session_string, self.create_datetime, self.end_datetime)
        return return_str

class ChatLine(models.Model):
    message_content = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    create_datetime = models.DateTimeField()

    def __str__(self):
        return_str = "Message content: {} \n Room session: {} \n Created user: {} \n Created date time: {} "\
            .format(self.message_content, self.room.session_string, self.user, self.create_datetime)
        return return_str