import os
import django
from django.core.management import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from books.models import Book, Review, Author  # dodano Author
from accounts.models import CustomUser
import random
from datetime import date, timedelta


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()


        first_names = [
            "Anna", "Bartek", "Cezary", "Daria", "Ewelina",
            "Filip", "Grzegorz", "Halina", "Igor", "Julia"
        ]

        books_data = [
            ("Harry Potter i Kamień Filozoficzny", "J.K. Rowling", "fantasy"),
            ("Harry Potter i Komnata Tajemnic", "J.K. Rowling", "fantasy"),
            ("Harry Potter i Więzień Azkabanu", "J.K. Rowling", "fantasy"),
            ("Harry Potter i Czara Ognia", "J.K. Rowling", "fantasy"),
            ("Harry Potter i Zakon Feniksa", "J.K. Rowling", "fantasy"),
            ("1984", "George Orwell", "dystopia"),
            ("Zbrodnia i kara", "Fiodor Dostojewski", "dramat"),
            ("Duma i uprzedzenie", "Jane Austen", "romans"),
            ("Mistrz i Małgorzata", "Michaił Bułhakow", "fantasy"),
            ("Folwark zwierzęcy", "George Orwell", "dystopia"),
        ]

        # Tworzenie użytkowników
        for name in first_names:
            email = f"{name.lower()}@gmail.com"
            if not CustomUser.objects.filter(email=email).exists():
                CustomUser.objects.create_user(
                    username=name.lower(),
                    email=email,
                    password="test"
                )

        # Tworzenie książek i autorów
        for title, author_name, category in books_data:
            author, _ = Author.objects.get_or_create(name=author_name)

            if not Book.objects.filter(title=title).exists():
                Book.objects.create(
                    title=title,
                    author=author,
                    category=category,
                    description="Magiczna przygoda 3 rycerzy.",
                    published_date=date(2000, 1, 1) + timedelta(days=random.randint(0, 5000))
                )

        # Tworzenie recenzji
        users = list(CustomUser.objects.all())
        books = list(Book.objects.all())

        review_texts = [
            "Świetna książka! Lubię do niej wracać, wartka akcja i mądre przesłanie.",
            "Nie podobało mi się, książka jest tragicznie napisana, najgorsze co w życiu czytałem.",
            "Fascynująca historia, nie mogłem się oderwać. Ciekawi bohaterowie i wciągająca fabuła.",
            "Trochę nudna i przewidywalna, ale ma swoje momenty. Ogólnie okej, ale nic specjalnego",
            "Polecam każdemu fanowi gatunku, bardzo dobra robota autora!"
            "Średnia - nie zachwyca, ale też nie jest zła. Przeciętna książka.",
        ]


        for user in users:
            reviewed_books = random.sample(books, 5)
            for book in reviewed_books:
                content = random.choice(review_texts)
                if not Review.objects.filter(user=user, book=book).exists():
                    Review.objects.create(
                        user=user,
                        book=book,
                        content=content
                    )
