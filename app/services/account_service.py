from app import db
from app.models.account import Account

class AccountService:
    @staticmethod
    def create_account(name, initial_balance=0.0):
        """
        Tworzy nowe konto z podaną nazwą i początkowym saldem.
        
        Args:
            name (str): Nazwa konta
            initial_balance (float): Początkowe saldo konta
            
        Returns:
            Account: Utworzone konto
            
        Raises:
            ValueError: Gdy nazwa jest pusta lub saldo jest nieprawidłowe
        """
        if not name:
            raise ValueError("Nazwa konta nie może być pusta")
        if not isinstance(initial_balance, (int, float)):
            raise ValueError("Saldo początkowe musi być liczbą")
            
        account = Account(name=name, balance=initial_balance)
        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def get_all_accounts():
        """
        Pobiera wszystkie konta.
        
        Returns:
            list[Account]: Lista wszystkich kont
        """
        return Account.query.all()

    @staticmethod
    def get_account(account_id):
        """
        Pobiera konto o podanym ID.
        
        Args:
            account_id (int): ID konta
            
        Returns:
            Account: Znalezione konto lub None
        """
        return Account.query.get(account_id)

    @staticmethod
    def update_account(account_id, name):
        """
        Aktualizuje nazwę konta.
        
        Args:
            account_id (int): ID konta
            name (str): Nowa nazwa konta
            
        Returns:
            Account: Zaktualizowane konto lub None
            
        Raises:
            ValueError: Gdy nazwa jest pusta
        """
        if not name:
            raise ValueError("Nazwa konta nie może być pusta")
            
        account = Account.query.get(account_id)
        if account:
            account.name = name
            db.session.commit()
        return account

    @staticmethod
    def update_account_with_balance(account_id, name, balance):
        """
        Aktualizuje nazwę i saldo konta.
        
        Args:
            account_id (int): ID konta
            name (str): Nowa nazwa konta
            balance (float): Nowe saldo konta
            
        Returns:
            Account: Zaktualizowane konto lub None
            
        Raises:
            ValueError: Gdy nazwa jest pusta lub saldo jest nieprawidłowe
        """
        if not name:
            raise ValueError("Nazwa konta nie może być pusta")
        if not isinstance(balance, (int, float)):
            raise ValueError("Saldo musi być liczbą")
            
        account = Account.query.get(account_id)
        if account:
            account.name = name
            account.balance = balance
            db.session.commit()
        return account

    @staticmethod
    def delete_account(account_id):
        """
        Usuwa konto o podanym ID.
        
        Args:
            account_id (int): ID konta
            
        Returns:
            bool: True jeśli konto zostało usunięte, False w przeciwnym razie
        """
        account = Account.query.get(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_balance(account_id, amount, is_inflow=True):
        """
        Aktualizuje saldo konta.
        
        Args:
            account_id (int): ID konta
            amount (float): Kwota do dodania/odjęcia
            is_inflow (bool): True jeśli to wpływ, False jeśli wydatek
            
        Returns:
            Account: Zaktualizowane konto lub None
            
        Raises:
            ValueError: Gdy kwota jest nieprawidłowa lub brak wystarczających środków
        """
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Kwota musi być dodatnią liczbą")
            
        account = Account.query.get(account_id)
        if account:
            if not is_inflow and account.balance < amount:
                raise ValueError("Niewystarczające środki na koncie")
                
            if is_inflow:
                account.balance += amount
            else:
                account.balance -= amount
            db.session.commit()
        return account

    @staticmethod
    def get_account_balance(account_id):
        """
        Pobiera aktualne saldo konta.
        
        Args:
            account_id (int): ID konta
            
        Returns:
            float: Saldo konta lub None jeśli konto nie istnieje
        """
        account = Account.query.get(account_id)
        return account.balance if account else None

    @staticmethod
    def get_total_balance():
        """
        Oblicza sumę sald wszystkich kont.
        
        Returns:
            float: Suma sald wszystkich kont
        """
        accounts = Account.query.all()
        return sum(account.balance for account in accounts)

    @staticmethod
    def check_account_exists(name):
        """
        Sprawdza czy konto o podanej nazwie już istnieje.
        
        Args:
            name (str): Nazwa konta do sprawdzenia
            
        Returns:
            bool: True jeśli konto istnieje, False w przeciwnym razie
        """
        return Account.query.filter_by(name=name).first() is not None