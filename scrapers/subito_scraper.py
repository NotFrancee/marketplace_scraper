import requests
import pandas as pd
from bs4 import BeautifulSoup, Tag
from classes.product import Product

default_bs_settings = {"features": "lxml"}


class SubitoProduct(Product):
    """Methods to scrape products for subito.it"""

    def __init__(self, name, price, link) -> None:
        super().__init__(name, price, link, "Subito")

    def scrape_is_sold(self, content: BeautifulSoup):
        """Checks if the product is sold"""
        try:
            status_box = content.select("[class*=transaction-status-container]")[0]

            print("is_sold function", status_box.text)
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

        url = self.link

        res = requests.get(url, timeout=10)
        content = BeautifulSoup(res.content)

        description = self.scrape_description(content)
        is_sold = self.scrape_is_sold(content)

        self.description = description
        self.is_sold = is_sold

        return description, is_sold


class SubitoScraper:
    """Scraper for subito.it"""

    def __init__(self, query) -> None:
        self.query = query

        self.products = dict()

    def should_skip(self, product: SubitoProduct):
        """Checks if the product has already been scraped and skips it in that case"""

        is_already_scraped = product.link in SubitoProduct.products_scraped

        if is_already_scraped:
            last_update = product.last_updated

            days_since_last_update = pd.Timestamp.today() - last_update

            if days_since_last_update.days < 5:
                return True

        return False

    def scrape_listings(self):
        """Scrapes all listings from the last page of the query (TODO not just the last page)"""
        url_template = "https://www.subito.it/annunci-italia/vendita/fotografia/?q={}"
        url = url_template.format(self.query.replace(" ", "+"))

        res = requests.get(url, timeout=10)
        content = BeautifulSoup(res.content, **default_bs_settings)

        containers: list[Tag] = content.find_all(attrs={"class": "item-card"})

        for container in containers:
            name = container.find("h2").text
            price = container.find("p").text
            link = container.find("a").attrs["href"]

            product = SubitoProduct(name, price, link)

            if self.should_skip(product):
                print("product has already been scraped")
                print(product)
                continue

            product.scrape()

            self.products[link] = product
