from tkinter import *
from tkinter import ttk
from scrapers.product import Product
from subito_scraper import SubitoScraper

products = []


def create_radio_box(frame: Frame):
    """Creates the radio box to select the website"""
    available_websites = ["Subito", "leboncoin"]

    selection = StringVar(value=available_websites[0])

    for website in available_websites:
        radio_button = Radiobutton(
            frame, text=website, variable=selection, value=website
        )
        radio_button.pack()

    return selection


def create_query_entry(frame: Frame):
    """Creates box to enter the query"""
    query_box = Entry(frame, width=30)
    query_box.insert(0, "query")

    query_box.pack()

    return query_box


def create_products_table(frame, products):
    """Creates the table to display the various products scraped"""
    columns = list(Product.to_row_cols.keys())

    table = ttk.Treeview(frame, columns=columns)
    table.column("#0", width=0, stretch=NO)
    for column in columns:
        table.heading(column, text=column, anchor=CENTER)

    for product in products:
        table.insert(parent="", index="end", text="", values=product)

    table.insert(
        parent="", index="end", iid=0, text="", values=("1", "Ninja", "101", "Oklahoma")
    )

    table.pack()


def handle_submit(website: str, query: str):
    """Handles submit"""

    if website.lower() == "subito":
        scraper = SubitoScraper(query)

        scraper.scrape_listings()

    products = [product.to_row() for product in scraper.products.values()]


root = Tk()
root.geometry = "400x400"
root.title = "TESTING THINGS OUT"

main_frame = Frame(root)
main_frame.pack()

scrape_frame = Frame(main_frame, width="50")
scrape_frame.pack(side=LEFT)
website_chosen = create_radio_box(scrape_frame)
query = create_query_entry(scrape_frame)

scrape_button = Button(
    scrape_frame,
    command=lambda: handle_submit(website_chosen.get(), query.get()),
    text="Scrape products",
)
scrape_button.pack(padx=2, pady=2)

table_frame = Frame(root, width="100")
table_frame.pack(side=RIGHT)
create_products_table(table_frame, products)


root.mainloop()


# every 5 min scrape all the websites
