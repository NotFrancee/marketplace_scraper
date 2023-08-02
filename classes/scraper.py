import pandas as pd
import requests
from bs4 import BeautifulSoup
from classes.product import Product
import logging

DAYS_THRESHOLD = 5
DEFAULT_BS4_SETTINGS = {"features": "lxml"}


class Scraper:
    """Base Scraper class"""

    def __init__(self, url_template: str, query: str, product_class: Product) -> None:
        query_formatted = query.replace(" ", "+")
        self.url = url_template.format(query_formatted)

        self.product_class = product_class

        self.scraped_products = dict()

    def should_skip(self, product):
        """Checks if the product has already been scraped and skips it in that case"""

        is_already_scraped = product.link in self.scraped_products

        if is_already_scraped:
            days_since_last_update = pd.Timestamp.today() - product.last_updated

            if days_since_last_update.days < DAYS_THRESHOLD:
                return True

        return False

    def get_listings(self):
        """Scrapes all listings from the last page of the query (TODO not just the last page)"""

        logging.info("getting all the recent listings...")
        res = requests.get(self.url, timeout=10)
        content = BeautifulSoup(res.content, **DEFAULT_BS4_SETTINGS)

        products = self.process_listings_page(content)

        self.scraped_products = self.scraped_products | products

        logging.info("...done!")

        return self.scraped_products

    def process_listings_page(self, content: BeautifulSoup) -> dict[str, Product]:
        """PLACEHOLDER FUNCTION"""
        return {"content": content}
