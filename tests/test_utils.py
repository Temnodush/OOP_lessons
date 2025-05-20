from src.utils import Category, Product


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
