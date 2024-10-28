cur.execute('''
            CREATE TABLE IF NOT EXISTS client_order (
                order TEXT,
                fk_client INT,
                fk_product INT,

                FOREIGN KEY (fk_client) REFERENCES client(id),
                FOREIGN KEY (fk_product) REFERENCES product(id),
                PRIMARY KEY (id, fk_product)
            )
            ''')

        self.connection.commit()  
        cur.close()
        
        def create_order(self, client_order):
        """ Cria pedido de acordo com os inputs do app. (self, client_order)"""
        cur = self.connection.cursor()

        cur.execute('''
        INSERT INTO client_order (order, fk_client, fk_product) VALUES (?, ?, ?)
        ''', (client_order.order, client_order.fk_client, client_order.fk_product)
                    )

        self.connection.commit()
        cur.close()