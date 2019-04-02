import re
from io import StringIO
from functools import partial
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item
from tutorial.items import TutorialItem
import csv

class AlbawabaSpider(CrawlSpider):

    name = "albawabacrawler"
    #allowed_domains =[url[0][8:] for url in csv.reader(open('/home/chrx/Desktop/Scrapy/HezbollahScraper/urls.csv','r'),delimiter =',')]
    allowed_domains = ["www.albawaba.com/en/"]

    #start_urls = [url[0] for url in csv.reader(open('/home/chrx/Desktop/Scrapy/HezbollahScraper/urls.csv','r'),delimiter =',')]
    start_urls = ["https://www.albawaba.com/en/""]

    rules = [Rule(LinkExtractor(unique = True), follow=True, callback="check_buzzwords")]

    terms = []
    locations = []
    organizations = []
    wordlist = []

    with open('/home/chrx/Desktop/Scrapy/HezbollahScraper/terms.csv','r') as csvfile:
        terms_reader = csv.reader(csvfile,delimiter = ',')
        for row in terms_reader:
            terms.append(row[0])
            organizations.append(row[1])
    for term in terms:
        for indx in range(0,5):
            wordlist.append(tuple((term,organizations[indx])))







    def check_buzzwords(self, response):
        url = response.url
        contenttype = response.headers.get("content-type", "").decode('utf-8').lower()
        items = []

        paragraph_text = response.css("p::text")
        p_texts = [p.get() for p in paragraph_text]

        for p_text in p_texts:
            p_text_lower = p_text.lower()
            for word_row in self.wordlist:
                if word_row[0].lower() in p_text_lower and word_row[1].lower() in p_text_lower:
                    item = TutorialItem()
                    item["word"] = word_row[0]
                    item["url"] = url
                    item["sentence"] = p_text
                    items.append(item)

        return(items)



    #gets the requests to follow recursively
    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) != None:
                return CrawlSpider._requests_to_follow(self, response)
        else:
                return []
