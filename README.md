
lsof -i :5000

Aplikacja Finansowa
Aplikacja webowa do zarządzania osobistymi finansami napisana w Pythonie z wykorzystaniem Flask.
Funkcjonalności

Zarządzanie kontami bankowymi
Śledzenie transakcji (wpływy i wydatki)
Kategoryzacja transakcji
Kalendarz finansowy
Przegląd wydatków

Wymagania systemowe

Python 3.8+
Flask
SQLAlchemy
Bootstrap 5

Instalacja

Sklonuj repozytorium:

bashCopygit clone [URL_REPOZYTORIUM]
cd [NAZWA_KATALOGU]

Utwórz wirtualne środowisko:

bashCopypython -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Zainstaluj zależności:

bashCopypip install -r requirements.txt

Uruchom aplikację:

bashCopypython run.py
Aplikacja będzie dostępna pod adresem: http://127.0.0.1:5000
Struktura projektu
Copyfinance_app/
├── config/
├── app/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── templates/
└── static/
Licencja
Ten projekt jest udostępniany na licencji MIT.