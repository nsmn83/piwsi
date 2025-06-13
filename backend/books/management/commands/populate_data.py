import os
import django
from django.core.management import BaseCommand

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from books.models import Book, Review, Author
from accounts.models import CustomUser
import random
from datetime import date, timedelta


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()
        CustomUser.objects.all().delete()

        first_names = [
            "Anna", "Bartek", "Cezary", "Daria", "Ewelina",
            "Filip", "Grzegorz", "Halina", "Igor", "Julia"
        ]

        profile_pics = [
            "https://i.pinimg.com/736x/46/dc/70/46dc7029e43b2dab0a5c993cbecb7da3.jpg",
            "https://content.imageresizer.com/images/memes/Doge-meme-4t0m5.jpg",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoVZuNX074cQMRxtib8LfqQ_UAUkovJEfV1g&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSIEd2zxEc_4IQ1jHyniHLECu15zRjkHTBJzA&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQwVt7GXhBiT0pc3w7WGTadYixDB-V5dLHJqA&s",
            "https://www.shutterstock.com/image-photo/profile-portrait-bengal-tiger-panthera-600nw-1953713884.jpg",
            "https://static.vecteezy.com/system/resources/previews/022/216/912/non_2x/face-profile-images-illustration-in-flat-style-free-vector.jpg",
            "https://i.pinimg.com/564x/51/c7/25/51c725e0a01212ff8e502281dda2a6dd.jpg",
            "https://thumbs.dreamstime.com/b/portrait-faceless-wizard-isolated-vector-illustration-293078574.jpg",
            "https://wallpapers.com/images/hd/profile-picture-8nn5taqcz5o8f2bz.jpg",
        ]

        # Tworzenie użytkowników z przypisanymi zdjęciami
        for name, pic_url in zip(first_names, profile_pics):
            email = f"{name.lower()}@gmail.com"
            if not CustomUser.objects.filter(email=email).exists():
                CustomUser.objects.create_user(
                    username=name.lower(),
                    email=email,
                    password="test1234",
                    profile_image_url=pic_url
                )

        # Dane autorów
        authors_data = [
            {
                "name": "J.K. Rowling",
                "nationality": "British",
                "birth_date": date(1965, 7, 31),
                "description": "Autorka serii Harry Potter, jedna z najpopularniejszych pisarek wszech czasów."
            },
            {
                "name": "George Orwell",
                "nationality": "British",
                "birth_date": date(1903, 6, 25),
                "description": "Autor powieści dystopijnych, takich jak 1984 i Folwark zwierzęcy."
            },
            {
                "name": "Fiodor Dostojewski",
                "nationality": "Russian",
                "birth_date": date(1821, 11, 11),
                "description": "Rosyjski pisarz, autor powieści psychologicznych i filozoficznych."
            },
            {
                "name": "Ryszard Kapuściński",
                "nationality": "Polish",
                "birth_date": date(1932, 3, 4),
                "description": "Polski reporter, znany z książek podróżniczych i reportaży politycznych."
            },
            {
                "name": "Norman Davies",
                "nationality": "British",
                "birth_date": date(1939, 6, 8),
                "description": "Brytyjski historyk, specjalizujący się w historii Europy Środkowo-Wschodniej."
            },
            {
                "name": "Olga Tokarczuk",
                "nationality": "Polish",
                "birth_date": date(1962, 1, 29),
                "description": "Polska pisarka, laureatka Nagrody Nobla w dziedzinie literatury."
            },
            {
                "name": "Frank Herbert",
                "nationality": "American",
                "birth_date": date(1920, 10, 8),
                "description": "Autor kultowej serii science fiction - Diuna."
            },
            {
                "name": "Jane Austen",
                "nationality": "British",
                "birth_date": date(1775, 12, 16),
                "description": "Brytyjska pisarka, znana z powieści obyczajowych, takich jak Duma i uprzedzenie."
            }
        ]

        authors_map = {}
        for author_data in authors_data:
            author, _ = Author.objects.update_or_create(
                name=author_data["name"],
                defaults={
                    "nationality": author_data["nationality"],
                    "birth_date": author_data["birth_date"],
                    "description": author_data["description"]
                }
            )
            authors_map[author.name] = author

        # Zakładamy, że autorzy już zostali utworzeni
        jk_rowling = Author.objects.get(name="J.K. Rowling")
        orwell = Author.objects.get(name="George Orwell")
        kapuscinski, _ = Author.objects.get_or_create(name="Ryszard Kapuściński")
        dostojewski = Author.objects.get(name="Fiodor Dostojewski")
        davies, _ = Author.objects.get_or_create(name="Norman Davies")
        tokarczuk = Author.objects.get(name="Olga Tokarczuk")
        herbert = Author.objects.get(name="Frank Herbert")
        austen = Author.objects.get(name="Jane Austen")

        Book.objects.create(
            title="Harry Potter i Kamień Filozoficzny",
            author=jk_rowling,
            category="fantasy",
            description="Młody Harry Potter odkrywa, że jest czarodziejem i rozpoczyna naukę w szkole magii Hogwart. Wraz z przyjaciółmi, Ronem i Hermioną, próbuje rozwikłać tajemnicę Kamienia Filozoficznego. Ich przygody pełne są magii, niebezpieczeństw i odkryć.",
            published_date=date(2001, 7, 1),
            cover_url="https://ia800404.us.archive.org/view_archive.php?archive=/33/items/l_covers_0010/l_covers_0010_84.zip&file=0010846904-L.jpg"
        )

        Book.objects.create(
            title="Harry Potter i insygnia śmierci",
            author=jk_rowling,
            category="fantasy",
            description="Harry ugina się pod ciężarem strasznego zadania: powinien odszukać i zniszczyć pozostałe horkruksy Voldemorta. Nigdy jeszcze nie czuł się tak samotnie jak teraz, gdy musi znaleźć w sobie dość siły, aby opuścić swoją bezpieczną Norę i bez wahań wyruszyć w nieznane.",
            published_date=date(2002, 7, 1),
            cover_url="https://ia902309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_19.zip&file=0008194648-L.jpg"
        )

        Book.objects.create(
            title="Harry Potter i Więzień Azkabanu",
            author=jk_rowling,
            category="fantasy",
            description="Harry poznaje Syriusza Blacka, zbiegłego więźnia z Azkabanu, który okazuje się jego ojcem chrzestnym. Dementorzy zagrażają szkole, a sekrety z przeszłości rzucają nowe światło na losy Harry’ego. Przygoda prowadzi do zaskakujących odkryć.",
            published_date=date(2003, 7, 1),
            cover_url="https://ia804608.us.archive.org/view_archive.php?archive=/16/items/olcovers104/olcovers104-L.zip&file=1046494-L.jpg"
        )

        Book.objects.create(
            title="Harry Potter i Czara Ognia",
            author=jk_rowling,
            category="fantasy",
            description="Harry zostaje wybrany do udziału w Turnieju Trójmagicznym, pełnym niebezpiecznych prób. Tajemnicze siły manipulują wydarzeniami, a powrót Lorda Voldemorta staje się realnym zagrożeniem. Przyjaźń i odwaga Harry’ego są wystawione na próbę.",
            published_date=date(2004, 7, 1),
            cover_url="https://ia902309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_10.zip&file=0008108730-L.jpg"
        )

        Book.objects.create(
            title="Harry Potter i Zakon Feniksa",
            author=jk_rowling,
            category="fantasy",
            description="Harry i jego przyjaciele zakładają Armię Dumbledore’a, by przygotować się do walki z Voldemortem. Ministerstwo Magii zaprzecza powrotowi czarnego maga, co komplikuje sytuację. Powieść pełna jest buntu, lojalności i trudnych wyborów.",
            published_date=date(2005, 7, 1),
            cover_url="https://ia802309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_23.zip&file=0008232735-L.jpg"
        )

        Book.objects.create(
            title="Rok 1984",
            author=orwell,
            category="dystopia",
            description="Winston Smith żyje w totalitarnym państwie, gdzie Wielki Brat kontroluje każdy aspekt życia. Buntując się przeciw reżimowi, nawiązuje zakazany romans i szuka prawdy. Powieść ukazuje przerażającą wizję zniewolenia i manipulacji.",
            published_date=date(1949, 6, 8),
            cover_url="https://ia902309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_40.zip&file=0008401033-L.jpg"
        )

        Book.objects.create(
            title="Folwark zwierzęcy",
            author=orwell,
            category="dystopia",
            description="Zwierzęta na farmie buntują się przeciw ludzkim właścicielom, tworząc własne społeczeństwo. Rządy świń szybko przeradzają się w nową tyranię. Powieść jest satyrą na totalitaryzm i rewolucje.",
            published_date=date(1945, 8, 17),
            cover_url="https://ia601909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_96.zip&file=0013964644-L.jpg"
        )

        Book.objects.create(
            title="Zbrodnia i kara",
            author=dostojewski,
            category="dramat",
            description="Raskolnikow, ubogi student, popełnia morderstwo, wierząc, że jest ponad moralnością. Dręczony wyrzutami sumienia, zmaga się z własnym sumieniem i sprawiedliwością. Powieść zgłębia psychologiczne i filozoficzne dylematy.",
            published_date=date(1866, 1, 1),
            cover_url="https://ia902309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_25.zip&file=0008250500-L.jpg"
        )

        # Kapuściński - reportaże
        Book.objects.create(
            title="Heban",
            author=kapuscinski,
            category="reportaż",
            description="Ryszard Kapuściński opisuje swoje podróże po Afryce, ukazując jej różnorodność i wyzwania. Od konfliktów po codzienne życie, reportaże oddają piękno i dramat kontynentu. Książka łączy empatię z wBoyską obserwacją.",
            published_date=date(1998, 1, 1),
            cover_url="https://ia600100.us.archive.org/view_archive.php?archive=/5/items/l_covers_0012/l_covers_0012_72.zip&file=0012725514-L.jpg"
        )

        Book.objects.create(
            title="Cesarz",
            author=kapuscinski,
            category="reportaż",
            description="Reportaż o upadku cesarza Etiopii Hajle Sellasje ukazuje mechanizmy władzy absolutnej. Kapuściński rozmawia z ludźmi z otoczenia cesarza, odsłaniając korupcję i iluzje. Książka jest uniwersalną refleksją nad tyranią.",
            published_date=date(1978, 1, 1),
            cover_url="https://ia801909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_95.zip&file=0013956449-L.jpg"
        )

        Book.objects.create(
            title="Imperium",
            author=kapuscinski,
            category="reportaż",
            description="Kapuściński podróżuje po rozpadającym się ZSRR, dokumentując jego różnorodność kulturową. Od Syberii po Kaukaz, opisuje życie ludzi w cieniu imperium. Książka łączy reportaż z refleksją historyczną.",
            published_date=date(1993, 1, 1),
            cover_url="https://ia804605.us.archive.org/view_archive.php?archive=/14/items/l_covers_0011/l_covers_0011_55.zip&file=0011554577-L.jpg"
        )

        # Dostojewski - druga książka
        Book.objects.create(
            title="Bracia Karamazow",
            author=dostojewski,
            category="powieść",
            description="Trzej bracia Karamazow borykają się z konfliktami rodzinnymi, wiarą i moralnością. Morderstwo ich ojca odsłania głębokie napięcia i filozoficzne pytania. Powieść zgłębia naturę ludzkiej duszy i sprawiedliwości.",
            published_date=date(1880, 1, 1),
            cover_url="https://ia902309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_26.zip&file=0008265150-L.jpg"
        )

        # Norman Davies - historia
        Book.objects.create(
            title="Boże igrzysko",
            author=davies,
            category="historyczna",
            description="Norman Davies przedstawia pełną historię Polski od średniowiecza po współczesność. Książka łączy szczegółowe analizy z barwnymi opowieściami o ludziach i wydarzeniach. To kompleksowy obraz polskiej kultury i polityki.",
            published_date=date(1987, 1, 1),
            cover_url="https://ia902309.us.archive.org/view_archive.php?archive=/20/items/l_covers_0008/l_covers_0008_29.zip&file=0008290806-L.jpg"
        )

        # Książki Olgi Tokarczuk
        Book.objects.create(
            title="Prawiek i inne czasy",
            author=tokarczuk,
            category="powieść",
            description="Powieść opowiada o losach mieszkańców mitycznej wsi Prawiek na przestrzeni XX wieku. Historie ludzi przeplatają się z elementami magii i natury. To refleksja nad czasem i ludzkim życiem.",
            published_date=date(1996, 1, 1),
            cover_url="https://ia601909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_96.zip&file=0013965721-L.jpg"
        )

        Book.objects.create(
            title="Dom dzienny, dom nocny",
            author=tokarczuk,
            category="powieść",
            description="Mozaika opowieści o życiu na polsko-czeskim pograniczu, pełna magii i folkloru. Bohaterowie zmagają się z historią i codziennością regionu. Książka łączy realizm z metafizyczną refleksją.",
            published_date=date(1998, 1, 1),
            cover_url="https://ia601909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_94.zip&file=0013941466-L.jpg"
        )

        Book.objects.create(
            title="Bieguni",
            author=tokarczuk,
            category="powieść",
            description="Zbiór opowieści o podróżnikach i nomadach, eksplorujących świat i siebie. Tokarczuk zgłębia ludzką potrzebę ruchu i ucieczki od rutyny. Powieść łączy filozofię z literacką mozaiką.",
            published_date=date(2007, 1, 1),
            cover_url="https://ia601909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_95.zip&file=0013951758-L.jpg"
        )

        # Książki Franka Herberta (uniwersum Diuny)
        Book.objects.create(
            title="Diuna",
            author=herbert,
            category="science fiction",
            description="Paul Atryda przybywa na pustynną planetę Arrakis, źródło cennej przyprawy. Walczy o władzę w świecie pełnym intryg i konfliktów. Powieść łączy politykę, ekologię i mistycyzm.",
            published_date=date(1965, 8, 1),
            cover_url="https://ia600505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_56.zip&file=0014563320-L.jpg"
        )

        Book.objects.create(
            title="Mesjasz Diuny",
            author=herbert,
            category="science fiction",
            description="Paul Atryda, jako mesjasz Arrakis, zmaga się z ciężarem swojej władzy. Intrygi i rebelie zagrażają jego rządom. Książka bada konsekwencje charyzmatycznego przywództwa.",
            published_date=date(1969, 10, 1),
            cover_url="https://ia600505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_56.zip&file=0014563316-L.jpg"
        )

        Book.objects.create(
            title="Dzieci Diuny",
            author=herbert,
            category="science fiction",
            description="Dzieci Paula Atrydy, Leto i Ghanima, stają przed nowymi wyzwaniami. Ich losy decydują o przyszłości imperium i Arrakis. Powieść zgłębia temat dziedzictwa i władzy.",
            published_date=date(1976, 4, 1),
            cover_url="https://ia600505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_59.zip&file=0014596254-L.jpg"
        )

        Book.objects.create(
            title="Bóg Imperator Diuny",
            author=herbert,
            category="science fiction",
            description="Leto II, syn Paula, rządzi jako nieśmiertelny imperator, zmieniając losy wszechświata. Jego decyzje budzą kontrowersje i opór. Książka analizuje poświęcenie i długoterminowe plany.",
            published_date=date(1981, 5, 1),
            cover_url="https://ia800505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_61.zip&file=0014613132-L.jpg"
        )

        Book.objects.create(
            title="Heretycy Diuny",
            author=herbert,
            category="science fiction",
            description="Tysiące lat po rządach Leto II nowe siły zagrażają stabilności wszechświata. Bene Gesserit i inne frakcje walczą o wpływy. Powieść eksploruje ewolucję społeczeństw.",
            published_date=date(1984, 6, 1),
            cover_url="https://ia800505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_61.zip&file=0014613133-L.jpg"
        )

        Book.objects.create(
            title="Kapitularz Diuną",
            author=herbert,
            category="science fiction",
            description="Bene Gesserit walczą o przetrwanie w świecie zmienionym przez dawne imperium Atrydów. Nowe zagrożenia zmuszają je do trudnych wyborów. Książka zamyka sagę o Diunie.",
            published_date=date(1985, 7, 1),
            cover_url="https://ia800505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_61.zip&file=0014613134-L.jpg"
        )

        # Książki Jane Austen
        Book.objects.create(
            title="Duma i uprzedzenie",
            author=austen,
            category="powieść obyczajowa",
            description="Elżbieta Bennet poznaje pana Darcy’ego, bogatego, ale pozornie aroganckiego mężczyznę. Ich relacja rozwija się przez nieporozumienia i stopniowe poznawanie siebie. Powieść bada miłość, klasę społeczną i ludzkie wady.",
            published_date=date(1813, 1, 28),
            cover_url="https://ia801909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_44.zip&file=0013440843-L.jpg"
        )

        Book.objects.create(
            title="Rozważna i romantyczna",
            author=austen,
            category="powieść obyczajowa",
            description="Siostry Dashwood, Elinor i Marianne, szukają miłości w świecie pełnym konwenansów. Każda z nich reprezentuje inny sposób podejścia do uczuć. Powieść ukazuje kontrast między rozumem a emocjami.",
            published_date=date(1811, 10, 30),
            cover_url="https://ia801909.us.archive.org/view_archive.php?archive=/31/items/l_covers_0013/l_covers_0013_94.zip&file=0013945705-L.jpg"
        )

        Book.objects.create(
            title="Emma",
            author=austen,
            category="powieść obyczajowa",
            description="Emma Woodhouse, młoda i zamożna, bawi się w swatanie innych, ignorując własne serce. Jej działania prowadzą do nieoczekiwanych komplikacji. Powieść łączy humor z analizą społeczną.",
            published_date=date(1815, 12, 23),
            cover_url="https://ia800505.us.archive.org/view_archive.php?archive=/35/items/l_covers_0014/l_covers_0014_55.zip&file=0014552684-L.jpg"
        )

        # Tworzenie recenzji
        users = list(CustomUser.objects.all())
        books = list(Book.objects.all())

        # Szablony recenzji dla różnych kategorii z podziałem na ton (pozytywne, negatywne, neutralne)
        review_templates = {
            "fantasy": {
                "positive": [
                    ["Magia tej książki wciąga od pierwszej strony!", "Bohaterowie są świetnie wykreowani.", "Czekam na kolejne przygody!"],
                    ["Niesamowita historia pełna czarów i tajemnic.", "Świat jest tak barwny, że czujesz się jego częścią.", "Polecam fanom fantasy!", "Zakończenie mnie zachwyciło."],
                    ["Fantastyczna podróż w magiczny świat!", "Każda strona trzyma w napięciu.", "Nie mogę się doczekać ekranizacji."],
                    ["Ten świat, te postacie! Ta książka jest tak dobra, że chciałbym przeczytać ją ponownie po raz pierwszy."],
                    ["Inne ksiażki fantasy mogą brać z niej przykład. Wzorowa książka. Szkoda, że taka krótka, bo dawno nie czytałem czegoś tak dobrego."]
                ],
                "negative": [
                    ["Zbyt przewidywalna fabuła, straszna nuda, chciałem odłożyć po pierwszych stronach"],
                    ["Ależ to było złe i nudne.", "Akcja nie porywa. Takich książek nie powinni pisać!"],
                    ["Rozczarowująca lektura - nie czuć klimatu, a świat przedstawiony pozostawia wiele do życzenia"],
                    ["Nie polecam nikomu, ponieważ pomimo ciekawego świata przedstawionego brakuje w niej głębi, a historia jest nijaka."],
                ],
                "neutral": [
                    ["Książka jak książka - brakuje trochę rozwoju postaci."],
                    ["Książka jest po prostu średnia.", "Czytaj tylko jeśli się nudzisz."],
                ]
            },
            "dystopia": {
                "positive": [
                    ["Przerażająco aktualna i wciągająca!", "Świat przedstawiony jest mroczny, ale fascynujący.", "Zmusza do myślenia."],
                    ["Genialna analiza totalitaryzmu!", "Bohaterowie są bardzo ludzcy i poruszający.", "Polecam każdemu!"],
                    ["Mocna opowieść, która zostaje w głowie.", "Napięcie budowane jest mistrzowsko.", "Świetna dystopia!"],
                    ["Ma w sobie to co lubię w książkach najbardziej - mądry przekaz."],
                ],
                "negative": [
                    ["Zbyt przygnębiająca i monotonna.", "Bohaterowie działają mi na nerwy.", "Nie wciągnęła mnie."],
                    ["Fabuła jest chaotyczna i nudna.", "Świat wydaje się naciągany.", "Szkoda czasu na tę książkę."],
                    ["Ciężko przebrnąć przez tę historię.", "Zbyt wiele polityki, za mało akcji.", "Rozczarowująca."],
                ],
                "neutral": [
                    ["Ciekawa wizja przyszłości, ale nie dla wszystkich.", "Niektóre fragmenty są intrygujące, inne nużące.", "Warto spróbować, jeśli lubisz dystopie."],
                    ["Historia nie zawsze wciąga.", "Bohaterowie są średni, brak im głębi.", "Średnia lektura."],
                ]
            },
            "dramat": {
                "positive": [
                    ["Głęboko poruszająca historia!", "Psychologiczne niuanse są mistrzowsko opisane.", "Klasyka, którą trzeba znać."],
                    ["Bohaterowie są tak realni, że czujesz ich emocje.", "Fabuła wciąga i zmusza do refleksji.", "Polecam z całego serca!"],
                    ["Niesamowita analiza ludzkiej duszy.", "Każde zdanie jest głęboko przemyślane.", "Warta każdej minuty."],
                    ["To się nazywa prawdziwa sztuka! Mam nadzieję, że każdy podziela moje zdanie - jest to arcydzieło!"],
                    ["Wciągająca od pierwszych stron - nic dziwnego, że zdobyła takie uznanie na świecie. Każdy powienien ją przeczytać chociaż raz"],
                ],
                "negative": [
                    ["Zbyt ciężka i przytłaczająca.", "Bohaterowie są irytujący.", "Nie dałem rady jej dokończyć."],
                    ["Historia jest nudna i rozwlekła.", "Filozoficzne rozważania są męczące.", "Nie polecam."],
                    ["Nic specjalnego, za dużo dramatyzmu.", "Postacie są jednowymiarowe.", "Szkoda czasu."],
                    ["Nie chciałbym czytać tego drugi raz - tragedia, miałka fabuła, to nawet nie leżało obok porządnej książki."]
                ],
                "neutral": [
                    ["Ciekawa, ale wymaga skupienia.", "Niektóre fragmenty są świetne, inne zbyt gęste.", "Dla miłośników literatury psychologicznej.", "Mocno nijaka"],
                    ["Historia, choć ciekawa zdecydowanie nie dla mnie.", "Bohaterowie mają potencjał, ale fabuła nierówna.", "Może się spodobać.", "Lepsze to niż nic, ale raczej nie przeczytam drugi raz"],
                ]
            },
            "reportaż": {
                "positive": [
                    ["Fascynująca podróż przez nieznane kultury!", "Autor opisuje wszystko z niezwykłą empatią.", "Czułem się, jakbym tam był."],
                    ["Wspaniałe reportaże, które otwierają oczy.", "Styl pisania jest bardzo plastyczny.", "Polecam miłośnikom podróży!"],
                    ["Niesamowite historie, które zostają w pamięci.", "Autor ma dar obserwacji.", "Rewelacyjna książka!"],
                    ["Otwiera oczy i pozwala zdobywać nową wiedzę. Dawno nie czytałem czegoś tak przyjemnego i ciekawego"]
                ],
                "negative": [
                    ["Zbyt chaotyczne opowieści.", "Niektóre historie są nudne.", "Spodziewałem się więcej głębi."],
                    ["Reportaże są nierówne.", "Czasem za dużo szczegółów, za mało emocji.", "Nie wciągnęła mnie."],
                    ["Rozczarowujące, brak spójności.", "Autor za bardzo skupia się na szczegółach.", "Nie polecam."],
                    ["Mam wrażenie, że autor nie ma pojęcia o czym pisze - gdybym wiedział na co się piszę, to w życiu bym jej nie kupił."]
                ],
                "neutral": [
                    ["Średnia pozycja - chyba tylko tyle mogę powiedzieć."],
                    ["Reportaże są OK, ale to nic wybitnego"],
                    ["Ciężko mi ocenić tę książkę, ogólnie jest średnia. Ma swoje mocne i słabe strony"]
                ]
            },
            "historyczna": {
                "positive": [
                    ["Niesamowita podróż przez historię!", "Autor ożywia przeszłość w fascynujący sposób.", "Polecam każdemu miłośnikowi historii."],
                    ["Świetnie napisana, pełna szczegółów.", "Czyta się jak dobrą powieść.", "Dowiedziałem się mnóstwo nowego!"],
                    ["Kompleksowa i wciągająca!", "Każdy rozdział to nowa przygoda.", "Must-read dla fanów historii."],
                    ["Czułem się jakbym przeniósł się w czasie - autor wie co robi i ma talen przedstawiania faktów w ciekawy sposób."],
                ],
                "negative": [
                    ["Zbyt dużo dat i faktów, za mało narracji.", "Nudna i przytłaczająca.", "Nie dla mnie."],
                    ["Ciężko przebrnąć przez tę książkę.", "Zbyt sucha i akademicka.", "Szkoda czasu."],
                    ["Rozczarowująca, brak emocji.", "Historia jest ciekawa, ale podana nudno.", "Nie polecam."],
                ],
                "neutral": [
                    ["Ciekawa, ale wymaga cierpliwości.", "Niektóre fragmenty są świetne, inne zbyt szczegółowe.", "Dla fanów historii OK."],
                    ["Całkiem niezła, ale brakuje ubarwnienia nudnych opisów. Mogłaby być troche przystępniejsza"],
                    ["Dla mnie takie 6/10. Jest przeciętna."],
                ]
            },
            "powieść": {
                "positive": [
                    ["Piękna historia, która chwyta za serce!", "Bohaterowie są bardzo autentyczni.", "Nie mogłem się oderwać!"],
                    ["Wciągająca opowieść pełna emocji.", "Styl pisania jest przepiękny.", "Polecam każdemu!"],
                    ["Niesamowita książka, pełna magii.", "Zakończenie mnie wzruszyło.", "Chcę więcej takich historii!"],
                ],
                "negative": [
                    ["Zbyt banalna fabuła.", "Bohaterowie są irytujący.", "Szkoda czasu na tę książkę."],
                    ["Historia jest nudna i przewidywalna.", "Nic nowego, same schematy.", "Nie polecam."],
                    ["Rozczarowująca lektura.", "Postacie są płaskie.", "Ciężko przebrnąć."],
                ],
                "neutral": [
                    ["Całkiem przyjemna, ale bez rewelacji.", "Bohaterowie są OK, ale fabuła nierówna.", "Może się spodobać."],
                    ["Historia ma potencjał, ale go nie wykorzystuje, drugi raz bym nie przeczytał, ale nie powiem, że jest jakaś tragiczna"],
                    ["Książka ma swoich fanów, nie jestem jednym z nich, ale potrafię zauważyć co podoba się w niej innym. Osobiście nie polecam, bo brakuje trochę rozwoju postaci"],
                ]
            },
            "powieść obyczajowa": {
                "positive": [
                    ["Cudowna historia o miłości i życiu!", "Bohaterowie są bardzo prawdziwi.", "Idealna na spokojny wieczór."],
                    ["Piękna i ciepła opowieść.", "Relacje między postaciami są świetnie opisane.", "Polecam z całego serca!"],
                    ["Urocza książka, która wzrusza.", "Autor świetnie oddaje emocje.", "Chcę więcej takich historii!"],
                ],
                "negative": [
                    ["Zbyt ckliwa i przewidywalna.", "Bohaterowie są nudni.", "Nie wciągnęła mnie."],
                    ["Fabuła jest banalna.", "Zbyt wiele schematów, za mało oryginalności.", "Szkoda czasu."],
                    ["Rozczarowująca, brak głębi.", "Postacie są płaskie.", "Nie polecam."],
                ],
                "neutral": [
                    ["Całkiem miła lektura, ale bez szału.", "Bohaterowie są w porządku, ale fabuła prosta.", "Dobra na relaks."],
                    ["Historia jest OK, ale nie zapada w pamięć.", "Styl pisania przyjemny, ale brak emocji.", "Średnia."],
                ]
            },
            "science fiction": {
                "positive": [
                    ["Niesamowity świat przyszłości!", "Intrygi i technologia wciągają od pierwszej strony.", "Polecam fanom sci-fi!"],
                    ["Epicka opowieść o kosmosie!", "Bohaterowie są charyzmatyczni.", "Czekam na kolejne części!"],
                    ["Fascynująca wizja przyszłości.", "Autor genialnie buduje napięcie.", "Must-read dla miłośników gatunku!"],
                    ["To się nazywa science-fiction. Mam nadzieję, że zachęcę innych do przeczytania. Wizja przyszłości jest intrygująca, postacie - nietuzinkowe."],
                ],
                "negative": [
                    ["Zbyt skomplikowana i chaotyczna.", "Bohaterowie są nieciekawi.", "Nie wciągnęła mnie."],
                    ["Fabuła jest naciągana.", "Zbyt wiele technicznych szczegółów.", "Szkoda czasu."],
                    ["Rozczarowująca, brak spójności.", "Świat jest ciekawy, ale historia nudna.", "Nie polecam."],
                ],
                "neutral": [
                    ["Ogólnie w porządku, wizja świata nie powala, mam mieszane odczucia"],
                    ["Średniawka :/"],
                ]
            }
        }

        # Tworzenie recenzji
        users = list(CustomUser.objects.all())
        books = list(Book.objects.all())

        # Słownik pomocniczy do kontrolowania użycia recenzji.
        used_reviews = {book.title: set() for book in books}

        for book in books:
            # Losowanie uzytkowników
            eligible_users = [user for user in users if not Review.objects.filter(user=user, book=book).exists()]
            if len(eligible_users) < 7:
                print(f"⚠️ Za mało użytkowników dla książki '{book.title}' — potrzebujesz co najmniej 7.")
                continue  # lub raise Exception()

            selected_users = random.sample(eligible_users, 7)
            for user in selected_users:
                tone = random.choice(["positive", "negative", "neutral"])
                available_reviews = review_templates[book.category][tone]
                # Pominięcie recenzji, które już się pojawiły przy danej książce
                available_reviews = [
                    r for r in available_reviews
                    if tuple(r) not in used_reviews[book.title]
                ]
                if not available_reviews:
                    available_reviews = review_templates[book.category][tone]

                review_sentences = random.choice(available_reviews)
                used_reviews[book.title].add(tuple(review_sentences))
                content = " ".join(review_sentences)

                Review.objects.create(
                    user=user,
                    book=book,
                    content=content
                )
