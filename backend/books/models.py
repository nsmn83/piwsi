from django.db import models
from django.conf import settings


class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, default="none")
    description = models.TextField(blank=True)
    opinion = models.TextField(default='Pozytywny')  # opinia liczona na podstawie sentymentu z recenzji
    published_date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.author}"


class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']  # Blokada wielu recenzji od jednego użytkownika

    def __str__(self):
        return f"Recenzja {self.user} dla {self.book}"
