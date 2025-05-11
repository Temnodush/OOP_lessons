import pytest

from src.utils import Product, Category


@pytest.fixture
def product():
    return Product(name="Товар", description="Описание товара", price=100.50, quantity=10)

@pytest.fixture
def category():
    return Category(name="Категория", description="Описание категории", products=[])