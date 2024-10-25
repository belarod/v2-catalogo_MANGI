import re

class Client:
    def __init__(self,
                 pk: int | None,
                 email: str,
                 password: str,
                 name_client: str,
                 last_login: str
                 ):
        self.pk = pk
        self.email = email
        self.password = password
        self.name_client = name_client
        self.last_login = last_login
        
    @staticmethod
    def verify_name_client(name_client):
        """ Verifica se nome do restaurante é maior ou igual a 10. """
        pattern = r'^[\wÀ-ÿ]+(?:\s+[\wÀ-ÿ]+)+$'
        
        if len(name_client) >= 10 and re.match(pattern, name_client):
            return True
        return False

    @staticmethod
    def verify_email(email):
        """ Verifica se está em formato EMAIL. """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if re.match(pattern, email):
            return True
        return False

    @staticmethod
    def verify_password(password):
        """ Verifica se há ao menos uma letra maiúscula, uma minúscula e um número. """
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$'
        if len(password) >= 5 and re.match(pattern, password):
            return True
        return False