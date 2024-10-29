for product in products_from_order:
            product_id = product[0]
            product_name = product[1]
            product_price = product[2]
            total_price += product_price * quantity
            quantity = DB.get_product_quantity(app, product_id, order_number)
            
            print(f'Produto: {product_name}, Preço: R${product_price / 100:.2f}, Quantidade: {quantity}')
            
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