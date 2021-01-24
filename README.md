# job_scraper

It's a scraper in Python to search for job offers in my town.

It's looking for offers on polish sites (OLX, pracuj.pl, lm).

It uses: 
- **requests_html** for scraping,
- **dateparse** for transforming diffrent date fromats to one,
- **jsons** to turn offer object into json, 
- ^ which is then pushed to free **mongoDB Atlas** with **pymongo**
  
To make it works you need to create **SECRET.py** file, where:

    url = 'your_mongo_db_url'
  
It's providing offers data for my **posredniak** app, check it out too.
