import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="none")
    description = models.TextField(blank=True)
    published_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.author}"

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']  # Blokada wielu recenzji od jednego użytkownika

    def __str__(self):
        return f"Recenzja {self.user} dla {self.book}"