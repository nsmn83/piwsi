# PIWSI
## Projektowanie i wdrażanie systemów informatycznych - projekt zaliczeniowy 📚
Repozytorium zawiera projekt (w trakcie realizacji), którego celem utworzenie jest aplikacji internetowej "Rejestr książek".
Aplikacja będzie forum to wyrażania swoich opinii na temat książek.

Użytkownik będzie mógł:<br>
🔵 utworzyć konto<br>
🔵 zalogować się<br>
🔵 wylogować się<br>
🔵 przeglądać książki i ich recenzje<br>
🔵 dodawać i edytować recenzje<br>
🔵 sprawdzać profile użytkowników<br>
🔵 sprawdzać informacje zarówno o książkach, jak i o autorze<br>
🔵 dostawać rekomendacje na podstawie wystawionych recenzji<br>

Moderator będzie mógł:<br>
🔵 Dodawać, usuwać i edytować książki w systemie<br>
🔵 Usuwać nieodpowiednie recenzje<br>

Uruchomienie projektu lokalnie (backendu) - opis dla brancha simple-data

1. W folderze /backend stwórz lub uruchom wirtualne środowisko<br>
2. Wpisz komendę pip install -r requirements.txt<br>
3. Wpisz komendę python manage.py makemigrations  (może być wymagane usunięcie starej bazy del db.sqlite3)<br>
4. Wpisz komendę python manage.py migrate
5. Stwórz superusera: python manage.py createsuperuser, najlepiej coś prostego typu username='admin', password='test'<br>
6. Uruchom skrpyt, który wrzuci dane do bazy (na razie zostawilem sqlite3, żeby nie odpalać postgresa lokalnie): python manage.py populate_data<br>
7. Po wejściu na admina powinno wszystko działać jak należy.
