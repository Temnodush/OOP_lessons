class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __add__(self, other):
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты Product")
        return self.__price * self.quantity + other.__price * other.quantity

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, data):
        return cls(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            quantity=data["quantity"],
        )


class Category:
    product_count: int = 0
    category_count: int = 0
    name: str
    description: str
    products: list

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []
        if products is not None:
            for product in products:
                self.add_product(product)
        Category.category_count += 1

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Ожидается объект класса Product")

    @property
    def products(self):
        product_strings = []
        for product in self.__products:
            product_info = (
                f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            )
            product_strings.append(product_info)
        return product_strings
