from rest_framework import serializers
from accounts.serializers import UserSummarySerializer
from .models import Book, Review, Author

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'category']


class BookDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_name', 'reviews', 'category', 'description', 'published_date']

    def get_reviews(self, obj):
        reviews = Review.objects.filter(book=obj)
        sentiment_counts = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }

        for review in reviews:
            sentiment_counts[review.sentiment] += 1

        return sentiment_counts

class ReviewSerializer(serializers.ModelSerializer):

    # Dane książki (potrzebne jeśli np. chcemy wyswietlic review uzytkownika
    # w jego profilu wraz z tytulem książki)
    book = BookListSerializer(read_only=True)

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
