from scraper import *
from mongo import *

def main():
	print('Scraping offers...')
	offers = get_offers(1)
	print('Scraping done!')
	print('Updating MongoDB...')
	updateMongoDB(offers)
	print('Update done!')

main()