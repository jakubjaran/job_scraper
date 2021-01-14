from requests_html import HTMLSession

session = HTMLSession()

# https://www.lm.pl/ogloszenia/lista/87/2/36290215
# https://www.olx.pl/praca/konin/?page=2

class Offer:
	def __init__(self, title, link, date, place):
		self.title = title
		self.link = link
		self.date = date
		self.place = place

allOffers = []

def get_lm_offers():
	lmOffers = []
	for i in range(1):
		r = session.get(f'https://www.lm.pl/ogloszenia/lista/87/{i}/36290215')
		divs = r.html.find('div.ogloszenie_kontener')
		for div in divs:
			aTag = div.find('a', first=True)
			title = aTag.text
			link = f"https://www.lm.pl{aTag.attrs['href']}"
			strongs = div.find('strong')
			date = strongs[0].text
			place = strongs[2].text

			offer = Offer(title, link, date, place)

			lmOffers.append(offer)

	return lmOffers

def get_olx_offers():
	olxOffers = []
	for i in range(1):
		r = session.get(f'https://www.olx.pl/praca/konin/?page={i}')
		divs = r.html.find('tr.wrap')
		for div in divs:
			title = div.find('strong', first=True).text
			link = div.find('a', first=True).attrs['href']
			breadcrumbs = div.find('small.breadcrumb')
			date = breadcrumbs[1].find('span', first=True).text
			place = breadcrumbs[0].find('span', first=True).text
			
			offer = Offer(title, link, date, place)

			olxOffers.append(offer)

	return olxOffers

allOffers += get_lm_offers()
allOffers += get_olx_offers()

for offer in allOffers:
	print(offer.title)
	print(offer.date)
	print(offer.place)
	print(offer.link)
	print(" ")
	print(" ")
	print(" ")


