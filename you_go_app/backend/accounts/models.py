from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_kyc_validated = models.BooleanField(default=False)
    # Add extra fields as needed (e.g., role)

    def __str__(self):
        return self.username
