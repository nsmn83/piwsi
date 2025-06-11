import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Book

# Mapowanie ocen tekstowych na liczby
RATING_MAP = {
    'positive': 1,
    'neutral': 0,
    'negative': -1,
}
def get_similar_users(user_id=None, min_similarity=0.2):
    from .models import Review

    #current_user=(CustomUser.objects.get(id=1))  #
    # 1. Pobierz wszystkie książki ocenione przez kogokolwiek
    reviews = Review.objects.all().values('user', 'book', 'sentiment')


    # Wyciągnij unikalne ID użytkowników i książek z recenzji
    user_ids = list(set(r['user'] for r in reviews))
    book_ids = list(set(r['book'] for r in reviews))

    user_id_to_idx = {uid: idx for idx, uid in enumerate(user_ids)}
    book_id_to_idx = {bid: idx for idx, bid in enumerate(book_ids)}

    # Utwórz macierz ocen użytkownik × książka (domyślnie 0 = neutralna)
    ratings_matrix = np.zeros((len(user_ids), len(book_ids)))

    # Wypełnij macierz ocenami
    for r in reviews:
        u_idx = user_id_to_idx[r['user']]
        b_idx = book_id_to_idx[r['book']]
        rating = RATING_MAP.get(r['sentiment'], 0)
        ratings_matrix[u_idx, b_idx] = rating

    # Oblicz podobieństwo kosinusowe
    similarities = cosine_similarity(ratings_matrix)

    # Znajdź indeks current_user w user_ids
    if user_id not in user_id_to_idx:
        # Użytkownik nie ma recenzji, brak podobnych
        return []
    current_idx = user_id_to_idx[user_id]

    sim_scores = similarities[current_idx]

    # Wybierz użytkowników o podobieństwie >= min_similarity, oprócz current_user
    similar_users = []
    for idx, score in enumerate(sim_scores):
        if idx != current_idx and score >= min_similarity:
            similar_users.append((user_ids[idx], score))

    # Posortuj malejąco po podobieństwie
    similar_users.sort(key=lambda x: x[1], reverse=True)

    # Zwróć listę użytkowników
    #from django.contrib.auth.models import User
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_pks = [uid for uid, _ in similar_users]

    users = User.objects.filter(id__in=user_pks)

    # Opcjonalnie: posortuj użytkowników według podobieństwa
    users_dict = {u.id: u for u in users}
    sorted_users = [users_dict[uid] for uid, _ in similar_users if uid in users_dict]

    return sorted_users

def recommend_books(user_id=None):

    similar_users = get_similar_users(user_id)

    # Pobierz książki ocenione pozytywnie przez podobnych użytkowników
    # ale nieocenione przez current_user

    recommended_books = Book.objects.filter(
        reviews__user__in=similar_users,
        reviews__sentiment='positive'
    ).exclude(
        reviews__user_id=user_id
    ).distinct()[:5]
    print(recommended_books)
    return recommended_books