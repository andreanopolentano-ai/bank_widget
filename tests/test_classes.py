import pytest

from src.classes import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Сбрасывает счетчики категорий и товаров перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product() -> Product:
    """Возвращает тестовый товар."""
    return Product(
        name="Samsung Galaxy S23 Ultra",
        description="256GB, Серый цвет, 200MP камера",
        price=180000.0,
        quantity=5,
    )


@pytest.fixture
def second_product() -> Product:
    """Возвращает второй тестовый товар."""
    return Product(
        name="Iphone 15",
        description="512GB, Gray space",
        price=210000.0,
        quantity=8,
    )


def test_product_initialization(product: Product) -> None:
    """Тестирует корректную инициализацию товара."""
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization(
    product: Product,
    second_product: Product,
) -> None:
    """Тестирует корректную инициализацию категории."""
    category = Category(
        name="Смартфоны",
        description="Смартфоны, как средство не только коммуникации",
        products=[product, second_product],
    )

    assert category.name == "Смартфоны"
    assert category.description == (
        "Смартфоны, как средство не только коммуникации"
    )
    assert category.products == [product, second_product]


def test_category_count(
    product: Product,
    second_product: Product,
) -> None:
    """Тестирует подсчет количества категорий."""
    Category(
        name="Смартфоны",
        description="Смартфоны, как средство коммуникации",
        products=[product],
    )
    Category(
        name="Телевизоры",
        description="Современные телевизоры",
        products=[second_product],
    )

    assert Category.category_count == 2


def test_product_count(
    product: Product,
    second_product: Product,
) -> None:
    """Тестирует подсчет количества товаров в категориях."""
    Category(
        name="Смартфоны",
        description="Смартфоны, как средство коммуникации",
        products=[product, second_product],
    )
    Category(
        name="Аксессуары",
        description="Аксессуары для смартфонов",
        products=[],
    )

    assert Category.product_count == 2


def test_empty_category_products() -> None:
    """Тестирует категорию без товаров."""
    category = Category(
        name="Аксессуары",
        description="Аксессуары для смартфонов",
        products=[],
    )

    assert category.products == []
    assert Category.category_count == 1
    assert Category.product_count == 0
