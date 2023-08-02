"""Scraper for subito.it"""

import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup, Tag
from classes.product import Product
from classes.scraper import Scraper
from utils.default_settings import DEFAULT_BS4_SETTINGS


class SubitoProduct(Product):
    """Methods to scrape products for subito.it"""

    def __init__(self, name, price, link) -> None:
        super().__init__(name, price, link, "Subito")

    def scrape_is_sold(self, content: BeautifulSoup):
        """Checks if the product is sold"""
        try:
            status_box = content.select("[class*=transaction-status-container]")[0]

            if status_box.text:
                return True
        except IndexError:
            return False

    def scrape_description(self, content: BeautifulSoup):
        """Scrapes the description of the product"""
        description_box = content.select('[class*="grid_description"]')[0]

        description = description_box.find("p").text

        return description

    def scrape(self):
        """Scrapes all the data about the product"""

        if self.should_skip():
            logging.info("skipped")
            return

        url = self.link

        res = requests.get(url, timeout=10)
        content = BeautifulSoup(res.content, **DEFAULT_BS4_SETTINGS)

        description = self.scrape_description(content)
        is_sold = self.scrape_is_sold(content)

        self.description = description
        self.is_sold = is_sold

        self.last_updated = datetime.today()

        return description, is_sold


class SubitoScraper(Scraper):
    """Scraper for subito.it"""

    def __init__(self, query: str, load_saved_data: bool) -> None:
        url_template = "https://www.subito.it/annunci-italia/vendita/fotografia/?q={}"
        super().__init__(url_template, query, SubitoProduct, "subito", load_saved_data)

    def process_listings_page(self, content: BeautifulSoup):
        containers: list[Tag] = content.find_all(attrs={"class": "item-card"})
        products = dict()

        for container in containers:
            name = container.find("h2").text
            price = container.find("p").text
            link = container.find("a").attrs["href"]

            if link in self.scraped_products:
                product = self.scraped_products[link]
                logging.info("product already existed, so using the stored version")
            else:
                product = SubitoProduct(name, price, link)
                logging.info("created product. now proceding to scrape")

            product.scrape()
            logging.info("scraped")
            products[link] = product

        return products
