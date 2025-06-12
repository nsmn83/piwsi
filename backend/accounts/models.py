from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# models.py
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    description = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # 🔽 NOWE POLE
    profile_image_url = models.URLField(
        default="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
