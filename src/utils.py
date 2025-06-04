from abc import ABC, abstractmethod

class BaseProduct(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, new_price):
        pass

class Mixin:
    name: str
    description: str
    price: float
    quantity: int
    def __init__(self,  *args, **kwargs):
        print(f"{self.__class__.__name__}: {args}, {kwargs}")
        super().__init__(*args, **kwargs)



    def __repr__(self):
        return f"{self.__class__.__name__}, {self.name}, {self.description}', {self.price}, {self.quantity}"


class Product(Mixin, BaseProduct):
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity


    def __add__(self, other):
        if type(other) != type(self):
            raise TypeError("Нельзя складывать продукты разных классов")
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

class Smartphone(Product):
    def __init__(self, efficiency, model, memory, color, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

class LawnGrass(Product):
    def __init__(self, germination_period, country, color, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        self.germination_period = germination_period
        self.country = country
        self.color = color

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

    def average_price(self):
        try:
            total_price = 0
            count_products = len(self.__products)
            for product in self.__products:
                total_price += product.price
            return total_price / count_products
        except ZeroDivisionError:
            return 0


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