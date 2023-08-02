"""Page to initiate listings searches"""

import PySimpleGUI as sg
from scrapers.subito_scraper import SubitoScraper


class ScrapeListingsPage:
    """Page to scrape new listings given query"""

    layout = [
        [sg.Text("Search for a product"), sg.In("query", key="-SEARCH-QUERY-")],
        [
            sg.Text("Select Website:"),
            sg.Combo(
                values=("Subito", "Leboncoin"),
                default_value="Subito",
                key="-SEARCH-WEBSITE-",
            ),
        ],
        [sg.Button("Run query", key="-SEARCH-SUBMIT-")],
    ]

    def __init__(self) -> None:
        pass

    def handle_submit(self, values: dict[str, str]):
        """Creates the scraper and scrapes the website"""
        query = values["-SEARCH-QUERY-"]
        website = values["-SEARCH-WEBSITE-"]

        if website == "Subito":
            scraper = SubitoScraper(query)

            scraper.get_listings()
        else:
            print("not implemented yet")
