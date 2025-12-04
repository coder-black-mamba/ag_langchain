# models.py
from django.db import models
from django.contrib.auth.models import User
import uuid

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default="New Session")
    created_at = models.DateTimeField(auto_now_add=True)

    def thread_id(self):
        return f"user-{self.user.id}-session-{self.session_id}"
