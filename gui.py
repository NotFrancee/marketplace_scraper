"""Main GUI"""

import PySimpleGUI as sg
from utils.test_products import init_products
from utils.logger import initialize_logger
from app.scrape_listings_page import ScrapeListingsPage
from app.products_page import ProductsPage

products = init_products()
initialize_logger()

scrape_listings_page = ScrapeListingsPage()
products_page = ProductsPage(products, ("Subito", "Leboncoin"))

layout = [
    [sg.Text("Marketplace Scraper", font=("Helvetica", 16, "bold"))],
    [
        sg.TabGroup(
            [
                [
                    sg.Tab("Scrape", scrape_listings_page.layout),
                    sg.Tab("Listings", products_page.layout),
                ]
            ],
            key="-TAB-GROUP-",
            expand_x=True,
            expand_y=True,
        )
    ],
]


# Create the window
window = sg.Window("Marketplace Scraper", layout)


# Create an event loop
while True:
    event, values = window.read()

    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break

    if event == "-SEARCH-SUBMIT-":
        scrape_listings_page.handle_submit(values)

    if event == "-FILTER-BTN-":
        products_page.filter_products(window, values["-FILTER-WEBSITE-"])
window.close()
