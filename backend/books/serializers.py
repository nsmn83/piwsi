from accounts.serializers import CustomUSerSerializer
from .models import Book, Review, Author
from rest_framework import serializers

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    sentiment_summary = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'  # albo jawnie wypisz + sentiment_summary + average_rating

    def get_sentiment_summary(self, obj):
        reviews = obj.reviews.all()
        summary = {'positive': 0, 'neutral': 0, 'negative': 0}
        for review in reviews:
            if review.sentiment in summary:
                summary[review.sentiment] += 1
        return summary

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        total = 0
        for review in reviews:
            if review.sentiment == 'positive':
                total += 5
            elif review.sentiment == 'neutral':
                total += 2.5
            elif review.sentiment == 'negative':
                total += 0
        return round(total / len(reviews), 1)


class ReviewWithoutBookSerializer(serializers.ModelSerializer):
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'sentiment', 'content', 'created_at']
        read_only_fields = ['user']


class ReviewWithBookSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'content', 'sentiment','created_at', 'user', 'book']
        read_only_fields = ['user', 'book']

    def get_book(self, obj):
        book_serializer = BookDetailSerializer(obj.book, context=self.context)
        book_data = book_serializer.data
        book_data.pop('reviews', None)
        return book_data

class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()
    sentiment_summary = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'category', 'description', 'published_date',
            'sentiment_summary', 'average_rating', 'reviews'
        ]

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return ReviewWithoutBookSerializer(reviews, many=True).data

    def get_sentiment_summary(self, obj):
        reviews = obj.reviews.all()
        summary = {'positive': 0, 'neutral': 0, 'negative': 0}
        for review in reviews:
            if review.sentiment in summary:
                summary[review.sentiment] += 1
        return summary

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        total = 0
        for review in reviews:
            total += {
                'positive': 5,
                'neutral': 2.5,
                'negative': 0
            }.get(review.sentiment, 0)
        return round(total / len(reviews), 1)



class ReviewSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'book']
