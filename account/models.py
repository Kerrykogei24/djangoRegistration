from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)