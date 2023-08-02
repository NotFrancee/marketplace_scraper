"""Generic Product Class"""

import pandas as pd
from utils.default_settings import DAYS_THRESHOLD


class Product:
    """Generic Product Class"""

    to_row_cols = {
        "name": "Name",
        "price": "Price",
        "link": "Link",
        "is_sold": "Sold",
        "last_updated": "Last Update",
        "website": "Website",
    }

    def __init__(self, name, price, link, website) -> None:
        self.name = name
        self.price = price
        self.link = link

        # later scrape automatically
        self.description = ""
        self.is_sold = False
        self.last_updated = None
        self.website = website

    def should_skip(self):
        """Checks if the product has already been scraped and skips it in that case"""
        last_update = self.last_updated

        if last_update is not None:
            days_since_last_update = pd.Timestamp.today() - last_update

            if days_since_last_update.days < DAYS_THRESHOLD:
                return True

        return False

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

    def scrape(self):
        """PLACEHOLDER FUNCTION"""
