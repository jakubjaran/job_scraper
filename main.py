from scraper import *
import json
import requests


def main():
    print("Scraping offers...")
    offers = get_offers(2)
    print("Scraping done!")
    print("Writing to JSON")
    with open("offers.json", "w") as outfile:
        json.dump(offers, outfile, indent=4)
    print("JSON writing done!")


main()
