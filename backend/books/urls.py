from django.urls import path

from .views import BookReviewList, ReviewDetail, ReviewCreateView, ReviewUpdateView, BookListView, ReviewDeleteView, BookDetailView, AuthorDetailView
from .views import UserReviewListView
urlpatterns = [

    #Recenzje dla książki
    path('book/<int:book_id>/review/', BookReviewList.as_view(), name='book-reviews'),

    #Szczegóły recenzji
    path('book/<int:book_id>/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),

    #Dodanie recenzji do danej ksiazki
    path('create/<int:book_id>/', ReviewCreateView.as_view(), name='create-review'),

    #Aktualizacja recenzji
    path('update/<int:pk>/', ReviewUpdateView.as_view(), name='update-review'),

    #Usunięcie recenzji
    path('delete/<int:pk>/', ReviewDeleteView.as_view(), name='delete-review'),

    #Lista książek
    path('books/', BookListView.as_view(), name='book-list'),

    #Szczegóły książki
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

    #Szczegóły autora
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),

    #Lista recenzji użytkownika o podanym id
    path('user/<int:user_id>/reviews/', UserReviewListView.as_view(), name='user-reviews'),

    #Rzeczy dotyczące edycji i wyswietlania profilu sa w acounts/urls.py
]