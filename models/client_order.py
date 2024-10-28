class Client_order:
    def __init__(self,
                 order: str, #order_number
                 fk_client: int,
                 fk_product: int
                 ):
        self.order = order
        self.fk_client = fk_client
        self.fk_product = fk_product