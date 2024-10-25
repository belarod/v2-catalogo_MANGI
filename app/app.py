import time
from multiprocessing.resource_tracker import register
from database.db import DB

from models.product import Product
from models.restaurant import Restaurant
from models.client import Client
from models.client_order import Client_order
from utils.utils import Utils

#inicia app
class App:
    _instance = None
    _initialized = False

    def __new__(cls, db):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance
    
    
    
    def __init__(self, db):
        if not self._initialized:
            self.db = db
            self.current_restaurant = None
            self._initialized = True



    def start_app(self):
        """ Inicia o app. (self)"""
        self.show_area_menu()
        
    
    
    def show_area_menu(self):
        while True:
            print('-- Tela Inicial --')
            print('1. Área Restaurante')
            print('2. Área Cliente')

            res = input('Escolha uma opção: ')

            if res == '1':
                Utils.clear_screen()
                self.show_restaurant_menu()
                break
            elif res == '2':
                Utils.clear_screen()
                self.show_client_menu() #falta criar
                break
            else:
                Utils.clear_screen()
                print('Esta opção não é valida, digite um dos números acima.')



    def show_restaurant_menu(self):
        """ Mostra menu para restaurantes. (self)"""
        Utils.clear_screen()
        while True:
            print('-- Área Restaurante --')
            print('1. Cadastrar')
            print('2. Login')
            print('3. Voltar')

            res = input('Escolha uma opção: ')

            if res == '1':
                Utils.clear_screen()
                self.show_restaurant_register_menu()
                break
            elif res == '2':
                Utils.clear_screen()
                self.show_restaurant_login_menu()
                break
            elif res == '3':
                Utils.clear_screen()
                self.show_area_menu()
                break
            else:
                Utils.clear_screen()
                print('Esta opção não é valida, digite um dos números acima.')



    def show_restaurant_register_menu(self):
        """ Abre menu para registro do restaurante. (self)"""
        Utils.clear_screen()
        print('-- Registre seu restaurante --')

        name_restaurant = ''
        while not Restaurant.verify_name_restaurant(name_restaurant): #verificando nome do restaurante
            print('*Nome deve conter pelo menos 10 caracteres.')
            name_restaurant = input('Nome do restaurante: ')

        commission = 101
        while not Restaurant.verify_commission(commission):
            app = DB("example.db")
            DB.show_highest_commission(app)
            print('*Valor deve ser maior ou igual a zero.')
    
            try:
                commission = Utils.int_input('Comissão (em porcentagem): ')
            except ValueError:
                print('*Valor deve ser maior ou igual a zero.')

        email = ''
        while not Restaurant.verify_email(email):
            print('*Deve ser um email válido.')
            email = input('Email: ').lower()

        password = ''
        while not Restaurant.verify_password(password):
            print('*Deve conter ao menos uma letra maiúscila, uma minúscula e um número.')
            password = input('Senha: ')
            
        app = DB("example.db")    
        if not DB.verify_existing_email_restaurant(app, email) and not DB.verify_existing_email_client(app, email): #verificar se funciona
            register_restaurant = Restaurant(pk=None, name_restaurant=name_restaurant, commission=commission, email=email, password=password, last_login=None)
            
            app = DB("example.db")
            DB.create_restaurant(app, register_restaurant)
            Utils.clear_screen()
            print(f'O restaurante {name_restaurant} foi registrado!')
            Utils.sleep(5)
            self.show_restaurant_menu()
        else:
            Utils.clear_screen()
            print(f'Este email já está em uso.')
            Utils.sleep(5)
            self.show_restaurant_menu()



    def show_restaurant_login_menu(self):
        """ Abre menu para login (self)"""
        Utils.clear_screen()

        print('-- Login --')
        email = input('Email: ').lower()
        password = input('Senha: ')
        restaurant = self.db.login_restaurant(email=email, password=password)
        
        if restaurant is None: #se login estiver incorreto ou nao existir
            print('Credenciais inválidas. Não possui cadastro? Registre-se agora mesmo!')
            Utils.sleep(5)
            Utils.clear_screen()
            self.show_restaurant_menu()
        else:
            self.current_restaurant = restaurant
            
            app = DB("example.db")
            current_date_login = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            last_login = DB.pull_last_login_restaurant(app, restaurant.pk)
            
            Utils.clear_screen()
            print(f'Bem vindo, {restaurant.name_restaurant} seu ID é {restaurant.pk} e a comissão {restaurant.commission}%.')
            print(f'Último login: {last_login[0]}')
            Utils.sleep(10)
            
            DB.push_current_login_restaurant(app, current_date_login, restaurant.pk)
            
            self.show_restaurant_pannel(restaurant)

    def show_product_list(self, restaurant: Restaurant):
        """ Mostra lista de produtos, se existente, de um respectivo restaurante. (self, restaurant: Restaurant)"""
        self.current_restaurant = restaurant
        app = DB("example.db")
        product_list = DB.show_products(app, restaurant.pk)
        
        if product_list is None:
            return None
        else:
            return product_list



    def show_restaurant_pannel(self, restaurant: Restaurant):
        """ Mostra painel do restaurante. (self, restaurant: Restaurant)"""
        Utils.clear_screen()
        app = DB("example.db")
        current_commission = DB.show_current_commission(app, restaurant.pk)
        print(f'-- Produtos do {restaurant.name_restaurant} --')
        product_list = self.show_product_list(restaurant)
        
        if product_list is None:
            print('Este restaurante ainda não possui cardápio.')
            while True:
                print('1. Cadastrar produto')
                print(f'2. Alterar comissão (Atual: {current_commission})')
                print('3. Logout')

                res = input('Escolha uma opção: ')
                
                self.current_restaurant = restaurant
                
                if res == '1':
                    Utils.clear_screen()
                    self.show_insert_product(restaurant)
                    break
                elif res == '2':
                    Utils.clear_screen()
                    self.show_alter_commission(restaurant)
                    break
                elif res == '3':
                    Utils.clear_screen()
                    print(f'Até logo, {restaurant.name_restaurant}!')
                    Utils.sleep(5)
                    self.current_restaurant = None
                    self.show_area_menu()

                else:
                    Utils.clear_screen()
                    print('Esta opção não é valida, digite um dos números acima.')
        else:
            print(f'Existem {len(product_list)} produtos.')
            for product in product_list:
                print(f'-- {product.name_product:<20} -- ID: {product.pk:<5} -- Preço: {product.price/100:.2f}')
            while True:
                print('1. Cadastrar produto')
                print('2. Apagar produto')
                print(f'3. Alterar comissão -- atual: {current_commission}%')
                print('4. Logout')

                res = input('Escolha uma opção: ')
                
                self.current_restaurant = restaurant
                
                if res == '1':
                    Utils.clear_screen()
                    self.show_insert_product(restaurant)
                    break
                elif res == '2':
                    Utils.clear_screen()
                    self.show_delete_product(restaurant)
                    break
                elif res == '3':
                    Utils.clear_screen()
                    self.show_alter_commission(restaurant)
                    break
                elif res == '4':
                    Utils.clear_screen()
                    print(f'Até logo, {restaurant.name_restaurant}!')
                    Utils.sleep(5)
                    self.current_restaurant = None
                    self.show_restaurant_menu()

                else:
                    Utils.clear_screen()
                    print('Esta opção não é valida, digite um dos números acima.')
        
                
                           
    def show_insert_product(self, restaurant: Restaurant):
        """ Insere um produto. (self, restaurant: Restaurant)"""
        
        name_product = ''
        while not Product.verify_name_product(name_product):
            Utils.clear_screen()
            print('-- Cadastrar produto --')
            print('*Nome não pode conter número e deve ter no mínimo 5 caracteres.')
            name_product = Utils.str_no_digit_input('Produto: ')

        price = 0.0
        while not Product.verify_price(price):
            print('*Digite o valor.')
            try:
                price = float(input('Preço: '))
                
                formatted_price_for_db = int(price * 100)
                
                formatted_price = f"{formatted_price_for_db / 100:.2f}".replace('.', ',') #p/ exibir com vírgula
                
            except ValueError:
                Utils.clear_screen()
                print('-- Cadastrar produto --')
        
        self.current_restaurant = restaurant
        insert_product = Product(pk=None, name_product=name_product, price=formatted_price_for_db, fk_id_restaurant=restaurant.pk)
        app = DB("example.db")
        DB.insert_product(app, insert_product)
        Utils.clear_screen()
        print(f'O produto {name_product} foi registrado com valor de {formatted_price}!')
        Utils.sleep(5)
        self.show_restaurant_pannel(restaurant)
        
        
        
    def show_delete_product(self, restaurant: Restaurant):
        """ Deleta um produto. (self, restaurant: Restaurant) """
        valid_option = False
        while not valid_option:
            Utils.clear_screen()
            print('-- Deletar produto --')
            product_list = self.show_product_list(restaurant)
            for product in product_list:
                print(f'-- {product.name_product:<20} -- ID: {product.pk:<5} -- Preço: {product.price/100:.2f}')
        
            print('*Somente números.')
            pk_product = Utils.int_input('ID do produto: ')
            
            product_exists = any(product.pk == pk_product for product in product_list)
            if not product_exists:
                Utils.clear_screen()
                print(f'Um produto com ID {pk_product} não existe.')
                Utils.sleep(5)
                self.show_delete_product(restaurant)
                
            app = DB("example.db")
            DB.delete_product(app, pk_product, restaurant.pk)
            Utils.clear_screen()
            print(f'O produto de ID {pk_product} foi deletado.')
            Utils.sleep(5)
            self.show_restaurant_pannel(restaurant)
            valid_option = True
            
            
            
    def show_alter_commission(self, restaurant: Restaurant):
        """ Altera comissão. (self, restaurant: Restaurant)"""
        app = DB("example.db")
        DB.show_highest_commission(app) 
        
        new_commission = 0
        pk = restaurant.pk
        while not int(new_commission) and Restaurant.verify_commission(new_commission):
            print('Em porcentagem, de 0 a 100.')
            
            print(f'Atual: {restaurant.commission}%')
            new_commission = Utils.int_input('Comissão (em porcentagem): ')
            
        DB.alter_commission(app, pk, new_commission)
        Utils.clear_screen()
        print(f'A sua comissão foi alterada para {new_commission}%.')
        Utils.sleep(5)
        self.show_restaurant_pannel(restaurant)
        
        
        
#############################################################################



    def show_client_menu(self):
        Utils.clear_screen()
        while True:
            print('-- Área Cliente --')
            print('1. Cadastrar')
            print('2. Login')
            print('3. Voltar')

            res = input('Escolha uma opção: ')

            if res == '1':
                Utils.clear_screen()
                self.show_client_register_menu() #criar
                break
            elif res == '2':
                Utils.clear_screen()
                self.show_client_login_menu() #criar
                break
            elif res == '3':
                Utils.clear_screen()
                self.show_area_menu()
                break
            else:
                Utils.clear_screen()
                print('Esta opção não é valida, digite um dos números acima.')
                
                
                
    def show_client_register_menu(self):
        """ Abre menu para registro do cliente. (self)"""
        Utils.clear_screen()
        print('-- Registre-se --')

        name_client = ''
        while not Client.verify_name_client(name_client):
            print('*Nome deve conter pelo menos 10 caracteres e conter sobrenome.')
            name_client = Utils.str_no_digit_input('Seu nome: ')

        email = ''
        while not Client.verify_email(email):
            print('*Deve ser um email válido.')
            email = input('Email: ').lower()

        password = ''
        while not Client.verify_password(password):
            print('*Deve conter ao menos uma letra maiúscila, uma minúscula e um número.')
            password = input('Senha: ')
            
        app = DB("example.db")    
        if not DB.verify_existing_email_client(app, email) and not DB.verify_existing_email_restaurant(app, email): 
            register_client = Client(pk=None, name_client=name_client, email=email, password=password, last_login=None)
            
            DB.create_client(app, register_client) #criar no db.py funcao p criar cliente
            Utils.clear_screen()
            print(f'{name_client} foi registrado!')
            Utils.sleep(5)
            self.show_client_menu()
        else:
            Utils.clear_screen()
            print(f'Este email já está em uso.')
            Utils.sleep(5)
            self.show_client_menu()
    
    def show_client_login_menu(self):
        """ Abre menu para login do cliente.(self)"""
        Utils.clear_screen()

        print('-- Login --')
        email = input('Email: ').lower()
        password = input('Senha: ')
        client = self.db.login_client(email=email, password=password) #criar login_client
        
        if client is None: #se login estiver incorreto ou nao existir
            print('Credenciais inválidas. Não possui cadastro? Registre-se agora mesmo!')
            Utils.sleep(5)
            Utils.clear_screen()
            self.show_client_menu()
        else:
            self.current_client = client
            
            app = DB("example.db")
            current_date_login = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            last_login = DB.pull_last_login_client(app, client.pk) #mudar nome função e fazer nova p consulta do login do cliente
            
            Utils.clear_screen()
            print(f'Bem vindo, {client.name_client}!')
            print(f'Último login: {last_login[0]}')
            Utils.sleep(10)
            
            DB.push_current_login_client(app, current_date_login, client.pk) #renomear e criar p client
            
            self.show_client_pannel() 
            
    def show_client_pannel(self):
        Utils.clear_screen()
        app = DB("example.db")
        
        print(f'-- Restaurantes --')
        restaurants_catalog = DB.show_restaurants_catalog(app)
        
        if not restaurants_catalog:
            Utils.clear_screen()
            print(f'Ainda não possuimos restaurantes cadastrados no aplicativo. Volte em breve!')
            Utils.sleep(5)
            self.current_client = None
            self.show_area_menu()
            
        for restaurant in restaurants_catalog:
            print(restaurant)
        
        chosen_restaurant = Utils.int_input('Digite o número do restaurante escolhido: ')
        
        if DB.verify_existing_restaurant(app, chosen_restaurant):
            self.show_chosen_restaurant(chosen_restaurant)
        else:
            print('Este restaurante não existe, tente novamente.')
            Utils.sleep(5)
            Utils.clear_screen()
            self.show_client_pannel()
            
    def show_chosen_restaurant(self, chosen_restaurant: int):
        '''chosen_restaurant guarda o id p acessar o restaurante selecionado'''
        Utils.clear_screen()
        app = DB("example.db")
        restaurant = DB.pull_chosen_restaurant(app, chosen_restaurant)
        
        print(f'-- Produtos {restaurant} --')
        product_list = DB.show_products(app, chosen_restaurant)
        
        if product_list is None:
            print('Este restaurante ainda não possui cardápio.')
        else:
            for product in product_list:
                print(f'-- ID: {product.pk:<5} -- {product.name_product:<20} -- Preço: {product.price/100:.2f}')