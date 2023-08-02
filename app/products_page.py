"""Products Page"""

import PySimpleGUI as sg
from classes.product import Product


class ProductsPage:
    """Products page"""

    def __init__(self, products: list[Product], websites: list[str]) -> None:
        self.products = products

        self.filter_layout = [
            sg.Text("Filter by Website"),
            sg.Combo(values=websites, key="-FILTER-WEBSITE-", default_value="Subito"),
            sg.Button("Filter", key="-FILTER-BTN-"),
        ]

        self._initialize_layout(products)

    def _initialize_layout(self, products: list):
        """Initializes the layout of the page"""

        self.layout = [
            self.filter_layout,
            [
                sg.Table(
                    values=[product.to_row() for product in products],
                    headings=list(Product.to_row_cols.values()),
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification="right",
                    key="-LISTINGS-TABLE-",
                    row_height=25,
                )
            ],
        ]

    def udpate_listings_table(self, window: sg.Window, products: list[Product]):
        """Updates the listing table with the new elements"""

        products_rows = [product.to_row() for product in products]

        window.Element("-LISTINGS-TABLE-").update(values=products_rows)

    def filter_products(self, window: sg.Window, filter_value: str):
        """Filters the products"""

        filtered_products = [
            product
            for product in self.products
            if filter_value.lower() in product.website.lower()
        ]

        self.udpate_listings_table(window, filtered_products)
