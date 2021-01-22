from scraper import *
from mongo import *
import time


def main():
	print('Scraping offers...')
	offers = get_offers(3)
	print('Scraping done!')
	print('Updating MongoDB...')
	updateMongoDB(offers)
	print('Update done!')


while True:
	main()
	time.sleep(600)
