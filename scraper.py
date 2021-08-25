from requests_html import HTMLSession
import dateparser
import jsons

session = HTMLSession()


class Offer:
    def __init__(self, title, link, date, place, source):
        self.title = title
        self.link = link
        self.date = date
        self.place = place
        self.source = source


def formatDate(date):
    return dateparser.parse(
        date, languages=["pl"], settings={"PREFER_DATES_FROM": "past"}
    )


def get_lm_offers(pages, url):
    lmOffers = []
    for i in range(pages):
        r = session.get(f"https://www.lm.pl/ogloszenia/lista/87/{i}/{url}")
        divs = r.html.find("div.ogloszenie_kontener")
        for div in divs:
            source = "LM.pl"
            aTag = div.find("a", first=True)
            title = aTag.text
            link = f"https://www.lm.pl{aTag.attrs['href']}"
            strongs = div.find("strong")

            date = strongs[0].text
            date = formatDate(date)

            place = strongs[2].text

            offer = Offer(title, link, date, place, source)

            for lmOffer in lmOffers:
                if lmOffer.link == offer.link:
                    print("Offer duplication")
                    break
            else:
                lmOffers.append(offer)

    return lmOffers


def get_olx_offers(pages, url):
    olxOffers = []
    for i in range(pages):
        r = session.get(url + f"{i}")
        divs = r.html.find("tr.wrap")
        for div in divs:
            source = "OLX.pl"
            title = div.find("strong", first=True).text
            link = div.find("a", first=True).attrs["href"].split("#")[0]
            breadcrumbs = div.find("small.breadcrumb")

            date = breadcrumbs[1].find("span", first=True).text
            date = formatDate(date)

            place = breadcrumbs[0].find("span", first=True).text

            offer = Offer(title, link, date, place, source)

            for olxOffer in olxOffers:
                if olxOffer.link == offer.link:
                    print("Offer duplication")
                    break
            else:
                olxOffers.append(offer)

    return olxOffers


def get_pracuj_offers(pages, url):
    pracujOffers = []
    for i in range(pages):
        r = session.get(url + f"{i}")
        r.html.render()
        divs = r.html.find("li.results__list-container-item")
        for div in divs:
            source = "pracuj.pl"
            aTag = div.find("a.offer-details__title-link", first=True)

            try:
                title = aTag.text
                link = aTag.attrs["href"]
            except:
                continue

            date = (
                div.find("span.offer-actions__date", first=True)
                .text.split(":")[1]
                .strip()
            )
            date = formatDate(date)

            place = div.find("li.offer-labels__item", first=True).text

            offer = Offer(title, link, date, place, source)

            for pracujOffer in pracujOffers:
                if pracujOffer.link == offer.link:
                    print("Offer duplication")
                    break
            else:
                pracujOffers.append(offer)

    return pracujOffers


def get_offers(pages):
    offers = []
    lmOffers = get_lm_offers(pages, "36290215")
    lmOffers += get_lm_offers(pages, "37762253")
    olxOffers = get_olx_offers(
        pages, "https://www.olx.pl/praca/konin/?search%5Bdist%5D=15&page="
    )
    olxOffers += get_olx_offers(pages, "https://www.olx.pl/praca/kolo/?page=")
    pracujOffers = get_pracuj_offers(
        pages, "https://www.pracuj.pl/praca/konin;wp?rd=20&pn="
    )
    pracujOffers += get_pracuj_offers(
        pages, "https://www.pracuj.pl/praca/kolo;wp?rd=20&pn="
    )

    offers = lmOffers + olxOffers + pracujOffers

    sortedOffers = sorted(offers, key=lambda offer: offer.date, reverse=True)

    jsonOffers = []

    for offer in sortedOffers:
        jsonOffers.append(jsons.dump(offer))

    return jsonOffers
