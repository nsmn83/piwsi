from accounts.serializers import CustomUSerSerializer
from .models import Book, Review, Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class ReviewWithoutBookSerializer(serializers.ModelSerializer):
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        # wypisz tylko te pola, które chcesz zwrócić, bez 'book'
        fields = ['id', 'user', 'sentiment', 'content', 'created_at']
        read_only_fields = ['user']


class ReviewWithBookSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)  # Zawiera dane o książce
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'book']


class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()
    sentiment_summary = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = Review.objects.filter(book=obj)
        return ReviewSerializer(reviews, many=True).data

    def get_sentiment_summary(self, obj):
        reviews = Review.objects.filter(book=obj)
        sentiment_counts = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }

        for review in reviews:
            if review.sentiment in sentiment_counts:
                sentiment_counts[review.sentiment] += 1

        return sentiment_counts



class ReviewSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'book']
