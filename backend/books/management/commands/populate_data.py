# populate_data.py
import os
import django
from django.core.management import BaseCommand

# Ustawienia projektu django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # Zamień 'backend' na nazwę swojego projektu
django.setup()

# Import modeli - środowisko zgłasza błąd ale skrypt działa bo django.setup() dynamicznie ustawia potrzebne scieżki
from books.models import Book, Review
from accounts.models import CustomUser
import random
from datetime import date, timedelta

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
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
                user = CustomUser.objects.create_user(
                    username=name.lower(),
                    email=email,
                    password="test"
                )

        # Tworzenie książek
        for title, author, category in books_data:
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

        for user in users:
            reviewed_books = random.sample(books, 5)
            for book in reviewed_books:
                if not Review.objects.filter(user=user, book=book).exists():
                    Review.objects.create(
                        user=user,
                        book=book,
                        content=
                        "Świetna książka! Lubię do niej wracać, wartka akcja i mądre przesłanie"
                        if random.randint(0, 1) else
                        "Nie podobało mi się, książka jest tragicznie napisana, najgorsze co w życiu czytałem",
                    )
