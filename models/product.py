import re

class Product:
    def __init__(self,
                 pk: int,
                 name_product: str,
                 price: int,
                 fk_id_restaurant: int):
        self.pk = pk
        self.name_product = name_product
        self.price = price
        self.fk_id_restaurant = fk_id_restaurant
        
    @staticmethod
    def verify_name_product(name_product):
        """ Verifica se nome do produto tem 5 ou mais letras. """
        if len(name_product) >= 5 and not any(char.isdigit() for char in name_product): 
            #checa se algum caractere na var name_product é um digito
            return True
        return False
    
    @staticmethod
    def verify_price(price):
        """ Verifica se o preço é maior que zero. """
        if price > 0:
            return True
        return False