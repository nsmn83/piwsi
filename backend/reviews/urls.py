from django.urls import path

from reviews.views import BookReviewList, ReviewDetail, ReviewCreateView, ReviewUpdateView

urlpatterns = [
    path('book/<int:book_id>/', BookReviewList.as_view(), name='book-reviews'),
    path('<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('create/<int:book_id>/', ReviewCreateView.as_view(), name='create-review'),
    path('update/<int:pk>/', ReviewUpdateView.as_view(), name='update-review'),
]