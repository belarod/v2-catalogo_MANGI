import re

class Restaurant:
    def __init__(self,
                 pk: int | None,
                 email: str,
                 password: str,
                 name_restaurant: str,
                 commission: int,
                 last_login: str
                 ):
        self.pk = pk
        self.email = email
        self.password = password
        self.commission = commission
        self.name_restaurant = name_restaurant
        self.last_login = last_login

    @staticmethod
    def verify_name_restaurant(name_restaurant):
        """ Verifica se nome do restaurante é maior ou igual a 10. """
        if len(name_restaurant) >= 10:
            return True
        return False

    @staticmethod
    def verify_commission(commission):
        """ Verifica se comissão é maior ou igual a zero, e menor ou igual a 100. """
        if commission >= 0 and commission <= 100:
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