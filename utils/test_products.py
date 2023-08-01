from classes.product import Product
import random

product_names = ["Nikon Z5", "Nikon Z7 w 24-70 f2", "Canon 6d Mk II"]


def init_products() -> list[Product]:
    """Initialize products for testing purposes"""
    products = []
    for name in product_names:
        price = random.randint(500, 1200)

        product = Product(name, price, "test_link", "Subito.it")
        product.description = "Test Description"

        products.append(product)

    return products
