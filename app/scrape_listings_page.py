"""Page to initiate listings searches"""

import PySimpleGUI as sg
from scrapers.subito_scraper import SubitoScraper
from classes.scraper import Scraper


class ScrapeListingsPage:
    """Page to scrape new listings given query"""

    def __init__(self) -> None:
        # pull saved searches
        saved_searches = Scraper.load_saved_searches()

        if len(saved_searches) > 0:
            default_val = saved_searches[0]
        else:
            default_val = None

        self.layout = [
            [
                sg.Radio(
                    "New Search", "search_type", key="-IS-NEW-SEARCH-", default=True
                ),
                sg.Radio(
                    "Saved Search",
                    "search_type",
                    key="-IS-SAVED-SEARCH-",
                    default=False,
                ),
            ],
            [sg.Text("Search for a product"), sg.In("query", key="-SEARCH-QUERY-")],
            [
                sg.Text("... or saved searches: "),
                sg.Combo(
                    values=saved_searches,
                    default_value=default_val,
                    key="-SAVED-SEARCH-",
                ),
            ],
            [
                sg.Text("Select Website:"),
                sg.Combo(
                    values=("Subito", "Leboncoin"),
                    default_value="Subito",
                    key="-SEARCH-WEBSITE-",
                ),
            ],
            [
                sg.Checkbox(
                    "Save Search and store results", default=False, key="-SAVE-SEARCH-"
                ),
            ],
            [sg.Button("Run query", key="-SEARCH-SUBMIT-")],
        ]

    def scrape_listings(self, values: dict[str, str]):
        """Creates the scraper and scrapes the website"""

        is_new_search = values["-IS-NEW-SEARCH-"]
        should_load_saved_data = values["-IS-SAVED-SEARCH-"]

        query = values["-SEARCH-QUERY-"] if is_new_search else values["-SAVED-SEARCH-"]
        website = values["-SEARCH-WEBSITE-"]

        if website == "Subito":
            scraper = SubitoScraper(query, should_load_saved_data)

            listings = scraper.get_listings()
            scraper.dump_listings_data()
            return listings

        else:
            print("not implemented yet")
