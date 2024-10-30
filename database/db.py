import sqlite3
from models.restaurant import Restaurant
from models.product import Product
from models.client import Client


class DB:

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.__setup_tables()



    def __setup_tables(self):
        """ Cria tabelas, caso não existam (self)"""
        cur = self.connection.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS restaurant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_restaurant TEXT NOT NULL,
                commission INT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                last_login TEXT DEFAULT 'Este é seu primeiro login!'
            )
            ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_product TEXT NOT NULL,
                price INT NOT NULL,
                fk_id_restaurant INT NOT NULL,
                FOREIGN KEY (fk_id_restaurant) REFERENCES restaurant(id) 
            )
            ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_client TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                last_login TEXT DEFAULT 'Este é seu primeiro login!'
            )
            ''')
        
        cur.execute('''
            CREATE TABLE IF NOT EXISTS client_order (
                order_id TEXT,
                fk_client INT,
                fk_product INT,
                quantity INT,
                date_order TEXT,

                FOREIGN KEY (fk_client) REFERENCES client(id),
                FOREIGN KEY (fk_product) REFERENCES product(id)
            )
            ''')

        self.connection.commit()  
        cur.close()



    def create_restaurant(self, restaurant: Restaurant):
        """ Cria restaurante de acordo com os inputs do app. (self, restaurant: Restaurant)"""
        cur = self.connection.cursor()

        cur.execute('''
        INSERT INTO restaurant (name_restaurant, commission, email, password) VALUES (?, ?, ?, ?)
        ''', (restaurant.name_restaurant, restaurant.commission, restaurant.email, restaurant.password)
                    )

        self.connection.commit()
        cur.close()
        
        
        
    def create_client(self, client: Client):
        """ Cria cliente de acordo com os inputs do app. (self, client: Client)"""
        cur = self.connection.cursor()

        cur.execute('''
        INSERT INTO client (name_client, email, password) VALUES (?, ?, ?)
        ''', (client.name_client, client.email, client.password)
                    )

        self.connection.commit()
        cur.close()



    def login_restaurant(self, email: str, password: str): #renomear
        """ Realiza login se caso a combinação exista no DB, e atribui o usuário de acordo com o restaurante acessado. Retorna instância de Restaurant. (self, email: str, password: str)"""
        cur = self.connection.cursor()

        cur.execute('''
                SELECT id, name_restaurant, commission, email, password, last_login
                FROM restaurant
                WHERE email = ? and password = ?
                ''', (email, password))
        record = cur.fetchone()
        cur.close()
        if record is None:
            return None
        restaurant = Restaurant(pk=record[0],
                           name_restaurant=record[1],
                           commission=record[2],
                           email=record[3],
                           password=record[4],
                           last_login=record[5])
        return restaurant
    
    
    
    def login_client(self, email: str, password: str): #renomear
        """ Realiza login se caso a combinação exista no DB, e atribui o usuário de acordo com o cliente acessado. Retorna instância de Client. (self, email: str, password: str)"""
        cur = self.connection.cursor()

        cur.execute('''
                SELECT id, name_client, email, password, last_login
                FROM client
                WHERE email = ? and password = ?
                ''', (email, password))
        record = cur.fetchone()
        cur.close()
        if record is None:
            return None
        client = Client(pk=record[0],
                           name_client=record[1],
                           email=record[2],
                           password=record[3],
                           last_login=record[4])
        return client
    
    
    
    def show_products(self, fk_id_restaurant: int):
        """ Consulta DB para retornar uma lista de produtos do respectivo restaurante. (self, fk_id_restaurant: int)"""
        cur = self.connection.cursor()

        cur.execute('''
                SELECT id, name_product, price
                FROM product
                WHERE fk_id_restaurant = ?
                ''', (fk_id_restaurant,))
        
        record = cur.fetchall()
        cur.close()
        product_list = []
        
        if not record:
            return None
        else:
            for product in record:
                product_inst = Product(pk=product[0], name_product=product[1], price=product[2], fk_id_restaurant=fk_id_restaurant)
                product_list.append(product_inst)
        return product_list
    
    def insert_product(self, product: Product):
        """ Insere produto no DB, de acordo com inputs do app. (self, product: Product)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                INSERT INTO product (name_product, price, fk_id_restaurant)
                VALUES (?, ?, ?)
                ''', (product.name_product, product.price, product.fk_id_restaurant))
        
        self.connection.commit()
        cur.close()
        
        
        
    def delete_product(self, pk_product: int, pk_restaurant: int):
        """ Deleta produto no DB, de acordo com inputs do app. (self, pk_product: int, pk_restaurant: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                DELETE FROM product
                WHERE id = ? and fk_id_restaurant = ?
                ''', (pk_product, pk_restaurant))
        
        self.connection.commit()
        cur.close()
        
        
        
    def alter_commission(self, pk: int, new_commission: int):
        """ Altera comissão do respectivo restaurante, de acordo com inputs do app. (self, pk: int, new_commission: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                UPDATE restaurant
                SET commission = ?
                WHERE id = ?
                ''', (new_commission, pk))
        
        self.connection.commit()
        cur.close()



    def show_highest_commission(self):
        """ Retorna variável com maior comissão existente entre todos restaurantes registrados. (self)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                SELECT commission
                FROM restaurant
                ORDER BY commission DESC
                LIMIT 1
                ''')
        
        highest_commission = cur.fetchone()
        
        if highest_commission:
            print(f"A maior comissão entre todos os restaurantes é de {highest_commission[0]}%!")
            return highest_commission
        else:
            cur.close()#alterado
            return None 

        
        
        
    def show_current_commission(self, pk: int):
        """ Consulta comissão atual de respectivo restaurante. (self, pk: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                SELECT commission
                FROM restaurant
                WHERE id = ?
                ''', (pk,))
        
        current_commission = cur.fetchone()
        
        if current_commission:
            return current_commission[0]
        
        cur.close()
        
        
        
    def push_current_login_restaurant(self, current_date_login: str, pk: int):
        """ Insere no DB data/hora em que foi acessado. (self, current_date_login: str, pk: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                UPDATE restaurant
                SET last_login = ?
                WHERE id = ?
                ''', (current_date_login, pk))
        
        self.connection.commit()
        cur.close()
        
        
        
    def push_current_login_client(self, current_date_login: str, pk: int):
        """ Insere no DB data/hora em que foi acessado. (self, current_date_login: str, pk: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                UPDATE client
                SET last_login = ?
                WHERE id = ?
                ''', (current_date_login, pk))
        
        self.connection.commit()
        cur.close()
        
        
        
    def pull_last_login_restaurant(self, pk: int):
        """ Consulta no DB, ÚLTIMA data/hora em que foi acessado. (self, pk: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                SELECT last_login
                FROM restaurant
                WHERE id = ?
                ''', (pk,))
        
        last_login = cur.fetchone()
        cur.close()
        return last_login
    
    
    
    def pull_last_login_client(self, pk: int):
        """ Consulta no DB, ÚLTIMA data/hora em que foi acessado. (self, pk: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                SELECT last_login
                FROM client
                WHERE id = ?
                ''', (pk,))
        
        last_login = cur.fetchone()
        cur.close()
        return last_login


    def verify_existing_email_restaurant(self, email: str):
        """ Consulta no DB se já existe o parâmetro (email) cadastrado. Retorna True, se não existe, False, se já existe. (self, email: str)"""
        cur = self.connection.cursor()
    
        cur.execute('''
                        SELECT email
                        FROM restaurant
                        WHERE email = ?
                        ''', (email,))
    
        record = cur.fetchone()
        cur.close()
        
        if record is None:
            return False
        return True
    
    
    
    def verify_existing_email_client(self, email: str):
        """ Consulta no DB se já existe o parâmetro (email) cadastrado. Retorna True, se não existe, False, se já existe. (self, email: str)"""
        cur = self.connection.cursor()
    
        cur.execute('''
                        SELECT email
                        FROM client
                        WHERE email = ?
                        ''', (email,))
    
        record = cur.fetchone()
        cur.close()
        
        if record is None:
            return False
        return True
    
    
    
    def verify_existing_product(self, pk_product: int, pk_restaurant: int):
        """ Consulta no DB se já existe o parâmetro (produto) cadastrado. Retorna True, se não existe, False, se já existe. (self, pk: str)"""
        cur = self.connection.cursor()
    
        cur.execute('''
                        SELECT id
                        FROM product
                        WHERE id = ? AND fk_id_restaurant = ?
                        ''', (pk_product, pk_restaurant))
    
        record = cur.fetchone()
        cur.close()
        
        if record is not None:
            return True
        return False
    
    def verify_existing_restaurant(self, chosen_restaurant: int):
        cur = self.connection.cursor()
    
        cur.execute('''
                        SELECT id
                        FROM restaurant
                        WHERE id = ?
                        ''', (chosen_restaurant,))
    
        record = cur.fetchone()
        cur.close()
        
        if record is None:
            return False
        return True
    
    def show_restaurants_catalog(self):
        
        cur = self.connection.cursor()
    
        cur.execute('''
                        SELECT id, name_restaurant, commission
                        FROM restaurant
                        ORDER BY commission DESC
                        ''')
    
        records = cur.fetchall()
        cur.close()
        
        if not records:
            return False 
        
        formatted_list = []
        for i in range(len(records)):
            record = records[i]
            if i == 0:
                formatted_list.append(f"{record[0]}. {record[1]} 🌟🌟🌟")  
            elif i == 1:
                formatted_list.append(f"{record[0]}. {record[1]} 🌟🌟")     
            elif i == 2:
                formatted_list.append(f"{record[0]}. {record[1]} 🌟")        
            else:
                formatted_list.append(f"{record[0]}. {record[1]}")          

        return formatted_list  



    def pull_chosen_restaurant(self, chosen_restaurant: int):
        cur = self.connection.cursor()

        cur.execute('''
                SELECT name_restaurant
                FROM restaurant
                WHERE id = ?
                ''',(chosen_restaurant,))
        record = cur.fetchone()
        cur.close()
        
        return record[0] if record else None
    
    def create_order(self, client_order):
        """ Cria pedido de acordo com os inputs do app. (self, client_order)"""
        cur = self.connection.cursor()

        cur.execute('''
        INSERT INTO client_order (order_id, fk_client, fk_product, quantity) VALUES (?, ?, ?, ?)
        ''', (client_order.order, client_order.fk_client, client_order.fk_product, client_order.quantity)
                    )

        self.connection.commit()
        cur.close()
        
    def get_products_from_order(self, order_number: str):
        cur = self.connection.cursor()

        cur.execute('''
            SELECT fk_product, name_product, price
            FROM client_order
            INNER JOIN product ON client_order.fk_product = product.id
            WHERE client_order.order_id = ?
        ''', (order_number,))
        
        records = cur.fetchall()
        cur.close()
        
        return records
    
    def get_product_quantity(self, fk_product: int, order_number: str):
        cur = self.connection.cursor()
    
        cur.execute('''
                        SELECT quantity
                        FROM client_order
                        WHERE fk_product = ? AND order_id = ?
                        ''', (fk_product, order_number))
    
        record = cur.fetchone()
        cur.close()
        
        if record is not None:
            return record[0]
        return None
    
    def push_current_date_order(self, date_order, fk_product, order_number):
        """ Insere no DB data/hora em que foi acessado. (self, current_date_login: str, pk: int)"""
        cur = self.connection.cursor()
        
        cur.execute('''
                UPDATE client_order
                SET date_order = ?
                WHERE fk_product = ? AND order_id = ?
                ''', (date_order, fk_product, order_number))
        
        self.connection.commit()
        cur.close()
        