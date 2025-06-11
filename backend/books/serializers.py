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

class BookDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = Review.objects.filter(book=obj)
        return ReviewSerializer(reviews, many=True).data

class ReviewSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    user = CustomUSerSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'book']
