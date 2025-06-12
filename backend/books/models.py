from django.db import models
from django.conf import settings
from .sentiment import analyze_sentiment


class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default="none")
    description = models.TextField(blank=True)
    published_date = models.DateField()
    cover_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.author}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=20, default='neutral')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']  # Blokada wielu recenzji od jednego użytkownika

    def __str__(self):
        return f"Recenzja {self.user} dla {self.book}"

    def save(self, *args, **kwargs):
        if self.content:
            self.sentiment = analyze_sentiment(self.content)
        super().save(*args, **kwargs)
