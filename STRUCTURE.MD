


# Struktura projektu:

finance_app/
│
├── config/
│   ├── __init__.py
│   └── config.py           # Konfiguracja aplikacji
│
├── app/
│   ├── __init__.py        # Inicjalizacja aplikacji
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py     # Model konta
│   │   └── transaction.py # Model transakcji
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── accounts.py    # Endpointy związane z kontami
│   │   ├── transactions.py# Endpointy związane z transakcjami
│   │   └── main.py        # Główne endpointy (np. strona główna)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── account_service.py    # Logika biznesowa dla kont
│   │   └── transaction_service.py # Logika biznesowa dla transakcji
│   │
│   └── utils/
│       ├── __init__.py
│       └── logger.py      # Konfiguracja loggera
│
├── templates/             # Bez zmian - szablony HTML
│   ├── base.html
│   ├── index.html
│   ├── transactions.html
│   ├── accounts.html
│   └── error.html
│
├── static/               # Bez zmian - pliki statyczne
│   ├── css/
│   ├── js/
│   └── img/
│
├── logs/                 # Katalog na logi
│   └── finance_app.log
│
├── instance/             # Katalog na bazę danych
│   └── finance.db
│
├── requirements.txt      # Zależności projektu
└── run.py               # Punkt wejścia aplikacji
