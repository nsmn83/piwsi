from rest_framework import serializers

from .models import Book, Review

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category', 'description', 'published_date']

class ReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  # Pełne dane książki

    class Meta:
        model = Review
        fields = ['id', 'content', 'created_at']
        read_only_fields = ['user', 'book']  # Blokada zmian