from django.db import models
from common.models import CommonModel


# Create your models here.
class ChattingRoom(CommonModel):
    """ Direct Message Room Definition """

    users = models.ManyToManyField("users.User", related_name="chattin_grooms",)

    def __str__(self) -> str:
        return "ChattRoom.(인원들어갈거임)"

class Message(CommonModel):
    """ Message Model Definition """

    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="messages",)
    text = models.TextField()
    room = models.ForeignKey("direct_messages.ChattingRoom", on_delete=models.CASCADE, related_name="messages",)

    def __str__(self) -> str:
        return f"{self.user} says: {self.text}"
