from datetime import datetime


class Product:
    """Base Product Class"""

    products_scraped = set()
    products = set()

    to_row_cols = {
        "name": "Name",
        "price": "Price",
        "link": "Link",
        "is_sold": "Sold",
        "last_updated": "Last Update",
        "website": "Website",
    }

    @staticmethod
    def reset_scraped_products_history():
        """Resets the history of products scraped"""
        Product.products_scraped = set()

    def __init__(self, name, price, link, website) -> None:
        self.name = name
        self.price = price
        self.link = link

        # later scrape automatically
        self.description = ""
        self.is_sold = False
        self.last_updated = datetime.now()
        self.website = website

        self.products_scraped.add(link)

    def __str__(self) -> str:
        res = []

        res.append(f"LISTING NAME: {self.name}")

        data = [
            f"Price: {self.price}",
            f"Link: {self.link}",
            f"Description: {self.description}",
            f"Is Sold: {self.is_sold}",
        ]

        res.append("\t\n".join(data))

        return "\n".join(res)

    def to_row(self):
        """Turns product to row for display in tkinter"""
        return [getattr(self, key) for key in self.to_row_cols]
