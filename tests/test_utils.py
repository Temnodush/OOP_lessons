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
