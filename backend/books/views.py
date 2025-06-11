from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Review, Book, Author
from .recommendations import recommend_books
from .serializers import ReviewSerializer, BookListSerializer, BookDetailSerializer, AuthorSerializer

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookListSerializer

class BookReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Review.objects.filter(book__id=book_id)

    def perform_create(self, serializer):
        book = Book.objects.get(id=self.kwargs['book_id'])
        serializer.save(user=self.request.user, book=book)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.AllowAny]

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['book_id'])

        # Sprawdź, czy użytkownik już dodał recenzję dla tej książki
        if Review.objects.filter(user=request.user, book=book).exists():
            return Response(
                {"detail": "Możesz dodać tylko jedną recenzję do tej książki."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, book=book)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewUpdateView(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()

    def get_object(self):
        review = super().get_object()
        if review.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        return review

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)  # Zapobiegaj zmianie autora

class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def get_object(self):
        review = super().get_object()
        if review.user != self.request.user and not self.request.user.is_staff:
            self.permission_denied(self.request)
        return review

class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(user__id=user_id)

class BookRecommendationListView(generics.ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = [permissions.AllowAny]
    from books.recommendations import recommend_books

    def get_queryset(self):
        #current_user = self.request.user
        user_id = self.kwargs['user_id']
        books = recommend_books(user_id)
        return books
