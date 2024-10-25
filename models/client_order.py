class Client_order:
    def __init__(self,
                 pk: int | None,
                 fk_product: int,
                 fk_client: int
                 ):
        self.pk = pk
        self.fk_product = fk_product
        self.fk_client = fk_client