from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True) #pole na opis profilu
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    bio = models.TextField(blank=True, null=True)

    def __string__(self) -> str:
        return self.email
