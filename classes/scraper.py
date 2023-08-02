"""Generic Scraper Class"""

import logging
import pickle
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from classes.product import Product
from utils.default_settings import DEFAULT_BS4_SETTINGS, DAYS_THRESHOLD
from utils.path_formatter import create_path


class Scraper:
    """Generic Scraper class"""

    @staticmethod
    def load_saved_searches() -> list[str]:
        """Loads the name of saved searches by looking at the saved files"""
        websites = ["subito"]

        saved_searches = []

        for website in websites:
            path = create_path(f"./data/{website}")

            files = os.listdir(path)

            saved_searches += [file.split(".")[0].replace("_", " ") for file in files]

        return saved_searches

    def __init__(
        self,
        url_template: str,
        query: str,
        product_class: Product,
        website: str,
        load_saved_data: bool,
    ) -> None:
        query_formatted = query.replace(" ", "+")
        self.url = url_template.format(query_formatted)
        self.website = website
        self.query = query

        self.product_class = product_class

        self.scraped_products = dict()

        if load_saved_data:
            self.load_listing_data()

    def should_skip(self, product):
        """Checks if the product has already been scraped and skips it in that case"""

        is_already_scraped = product.link in self.scraped_products

        if is_already_scraped:
            days_since_last_update = pd.Timestamp.today() - product.last_updated

            if days_since_last_update.days < DAYS_THRESHOLD:
                return True

        return False

    def get_listings(self) -> list[Product]:
        """Scrapes all listings from the last page of the query (TODO not just the last page)"""

        logging.info("getting all the recent listings...")
        res = requests.get(self.url, timeout=10)
        content = BeautifulSoup(res.content, **DEFAULT_BS4_SETTINGS)

        products = self.process_listings_page(content)

        self.scraped_products = self.scraped_products | products

        logging.info("...done!")

        return list(self.scraped_products.values())

    def load_listing_data(self):
        """Loads the listings data from the pickle file"""

        path = create_path(f"./data/{self.website}/{self.query}.pkl")

        with open(path, "rb") as file:
            data = pickle.load(file)
            self.scraped_products = data

    def dump_listings_data(self):
        """Dumps the listings data in a pickle file"""

        path = create_path(f"./data/{self.website}/{self.query}.pkl")

        with open(path, "wb") as file:
            pickle.dump(self.scraped_products, file)

    def process_listings_page(self, content: BeautifulSoup) -> dict[str, Product]:
        """PLACEHOLDER FUNCTION"""
        return {"content": content}
