import pytest

from src.utils import Category, Product, Smartphone, LawnGrass, Mixin, BaseProduct


def test_product_initialization(product):
    assert product.name == "Товар"
    assert product.description == "Описание товара"
    assert product.price == 100.50
    assert product.quantity == 10


def test_category_initialization(category):
    assert category.name == "Категория"
    assert category.description == "Описание категории"
    assert isinstance(category.products, list)
    assert len(category.products) == 0


def test_category_counter(category):
    initial_count = Category.category_count
    Category(name="Новая категория", description="...", products=[])
    assert Category.category_count == initial_count + 1


def test_product_counter(product):
    initial_count = Category.product_count
    Category(name="Тест", description="...", products=[product])
    assert Category.product_count == initial_count + 1


def test_multiple_categories():
    Category.category_count = 0
    Category.product_count = 0

    p1 = Product("Товар 1", "...", 100, 1)
    p2 = Product("Товар 2", "...", 200, 2)
    Category("Категория 1", "...", [p1, p2])
    Category("Категория 2", "...", [p1])

    assert Category.category_count == 2
    assert Category.product_count == 3


def test_product_creation():
    p = Product("Телефон", "Смартфон", 20000, 5)
    assert p.name == "Телефон"
    assert p.price == 20000


def test_price_setter_valid():
    p = Product("Ноутбук", "Игровой", 50000, 3)
    p.price = 60000
    assert p.price == 60000


def test_price_setter_invalid(capsys):
    p = Product("Наушники", "Беспроводные", 5000, 10)
    p.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 5000


def test_category_add_product():
    p = Product("Клавиатура", "Механическая", 3000, 8)
    category = Category("Периферия", "Устройства ввода")
    category.add_product(p)
    assert len(category.products) == 1
    assert "Клавиатура, 3000 руб. Остаток: 8 шт." in category.products


def test_product_str_representation(product):
    expected_str = "Товар, 100.5 руб. Остаток: 10 шт."
    assert str(product) == expected_str


def test_category_str_representation():
    p1 = Product("Товар 1", "Описание", 100, 3)
    p2 = Product("Товар 2", "Описание", 200, 2)
    category = Category("Категория", "Описание", [p1, p2])

    assert str(category) == "Категория, количество продуктов: 5 шт."


def test_category_products_getter_optimization():
    p = Product("Тест", "Описание", 100, 5)
    category = Category("Категория", "Описание", [p])

    # Проверка, что используется __str__ продукта
    assert str(p) in category.products
    assert category.products == ["Тест, 100 руб. Остаток: 5 шт."]

def test_add_smartphones():
    """ Проверка сложения продукта Smartphone"""
    s1 = Smartphone(2.5, "X", 128, "black",
                    "Phone", "...", 50000, 1)
    s2 = Smartphone(3.0, "Y", 256, "white",
                    "Phone", "...", 60000, 2)
    assert s1 + s2 == 50000*1 + 60000*2

def test_add_grasses():
    """ Проверка сложения продукта LawnGrass"""
    lg1 = LawnGrass(7, "Russia", "green",
                    "Мятлик луговой", "Описание1", 120, 25)
    lg2 = LawnGrass(14, "Russia", "green",
                    "Полевица", "Описание2", 100, 15)
    assert lg1 + lg2 == 25*120 + 15*100


def test_add_different_classes_error():
    """ Проверка на сложение разных классов."""
    l = LawnGrass(14, "Russia", "green",
                  "Grass", "...", 1000, 5)
    s = Smartphone(2.5, "X", 128, "black",
                   "Phone", "...", 50000, 1)

    with pytest.raises(TypeError) as exc_info:
        l + s

    assert "Нельзя складывать продукты разных классов" in str(exc_info.value)


def test_add_subclass_products():
    category = Category("Тест", "...")
    s = Smartphone(2.5, "X", 128, "black",
                   "Phone", "...", 50000, 1)
    l = LawnGrass(14, "Russia", "green",
                  "Grass", "...", 1000, 5)

    category.add_product(s)
    category.add_product(l)

    assert len(category.products) == 2

def test_mixin_output_product(capsys):
    """Проверка вывода информации при создании Product"""
    p = Product("Телефон", "Смартфон", 20000, 5)
    captured = capsys.readouterr()
    assert "Product" in captured.out
    assert "('Телефон', 'Смартфон', 20000, 5)" in captured.out

def test_mixin_output_smartphone(capsys):
    """Проверка вывода информации при создании Smartphone"""
    s = Smartphone(2.5, "X", 128, "black",
                   "Phone", "...", 50000, 1)
    captured = capsys.readouterr()
    assert "Smartphone" in captured.out
    assert "('Phone', '...', 50000, 1)" in captured.out

def test_mixin_output_lawn_grass(capsys):
    """Проверка вывода информации при создании LawnGrass"""
    lg = LawnGrass(7, "Russia", "green",
                   "Трава", "Описание", 120, 25)
    captured = capsys.readouterr()
    assert "LawnGrass" in captured.out
    assert "('Трава', 'Описание', 120, 25)" in captured.out


def test_class_hierarchy():
    """Проверка корректности иерархии наследования"""
    assert issubclass(Product, Mixin)
    assert issubclass(Product, BaseProduct)
    assert issubclass(Smartphone, Product)
    assert issubclass(LawnGrass, Product)

    p = Product("Test", "Desc", 100, 5)
    assert isinstance(p, Mixin)
    assert isinstance(p, BaseProduct)


def test_abstract_method_implementation():
    p = Product("Test", "Desc", 100, 5)

    # Проверка __add__
    p2 = Product("Test2", "Desc2", 200, 3)
    assert p + p2 == 100 * 5 + 200 * 3

    # Проверка __str__
    assert str(p) == "Test, 100 руб. Остаток: 5 шт."

    # Проверка price property
    assert p.price == 100
    p.price = 150
    assert p.price == 150

def test_base_product_is_abstract():
    """Проверка, что BaseProduct нельзя инстанцировать"""
    with pytest.raises(TypeError):
        BaseProduct("Test", "Desc", 100, 5)