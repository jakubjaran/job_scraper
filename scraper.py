from requests_html import HTMLSession
import dateparser

session = HTMLSession()

class Offer:
	def __init__(self, title, link, date, place, source):
		self.title = title
		self.link = link
		self.date = date
		self.place = place
		self.source = source


def formatDate(date):
	return dateparser.parse(date, languages=['pl'], settings={'PREFER_DATES_FROM': 'past'})


def get_lm_offers(pages):
	lmOffers = []
	for i in range(pages):
		r = session.get(f'https://www.lm.pl/ogloszenia/lista/87/{i}/36290215')
		divs = r.html.find('div.ogloszenie_kontener')
		for div in divs:
			source = 'LM.pl'
			aTag = div.find('a', first=True)
			title = aTag.text
			link = f"https://www.lm.pl{aTag.attrs['href']}"
			strongs = div.find('strong')

			date = strongs[0].text
			date = formatDate(date)

			place = strongs[2].text

			offer = Offer(title, link, date, place, source)

			lmOffers.append(offer)

	return lmOffers


def get_olx_offers(pages):
	olxOffers = []
	for i in range(pages):
		r = session.get(f'https://www.olx.pl/praca/konin/?page={i}')
		divs = r.html.find('tr.wrap')
		for div in divs:
			source = 'OLX.pl'
			title = div.find('strong', first=True).text
			link = div.find('a', first=True).attrs['href']
			breadcrumbs = div.find('small.breadcrumb')

			date = breadcrumbs[1].find('span', first=True).text
			date = formatDate(date)

			place = breadcrumbs[0].find('span', first=True).text
			
			offer = Offer(title, link, date, place, source)

			olxOffers.append(offer)

	return olxOffers


def get_pracuj_offers(pages):
	pracujOffers = []
	for i in range(pages):
		r = session.get(f'https://www.pracuj.pl/praca/konin;wp?rd=5&pn={i}')
		r.html.render()
		divs = r.html.find('li.results__list-container-item')
		for div in divs:
			source = 'pracuj.pl'
			aTag = div.find('a.offer-details__title-link', first=True)

			try:
				title = aTag.text
				link = aTag.attrs['href']
			except:
				continue

			date = div.find('span.offer-actions__date', first=True).text.split(':')[1].strip()
			date = formatDate(date)

			place = div.find('li.offer-labels__item', first=True).text
			
			offer = Offer(title, link, date, place, source)

			pracujOffers.append(offer)

	return pracujOffers


def get_offers(pages):
	allOffers = []

	lmOffers = get_lm_offers(pages)
	olxOffers = get_olx_offers(pages)
	pracujOffers = get_pracuj_offers(pages)

	allOffers = lmOffers + olxOffers + pracujOffers

	for offer in allOffers:
		print(offer.title)
		print(" ")
		print(offer.date)
		print(" ")
		print(offer.place)
		print(" ")
		print(offer.link)
		print(" ")
		print(offer.source)
		print(" ")
		print(" ")
		print(" ")


get_offers(1)


#TODO
# sort offers by date
# keywords