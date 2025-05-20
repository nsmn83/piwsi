from rest_framework import serializers
from accounts.serializers import UserSummarySerializer
from .models import Book, Review, Author

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'opinion', 'category', 'description', 'published_date']

class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  # Pełne dane książki
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['book', 'id', 'content', 'created_at', 'user']
        read_only_fields = ['user', 'book']  # Blokada zmian

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['name', 'description', 'nationality', 'birth_date']

    def __str__(self):
        return self.name
