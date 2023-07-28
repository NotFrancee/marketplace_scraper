from scrapers.subito_scraper import SubitoScraper


def script():
    query = "nikon z5"

    scraper = SubitoScraper(query)

    scraper.get_listings()
