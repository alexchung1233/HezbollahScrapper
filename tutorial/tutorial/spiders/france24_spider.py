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


class France24Spider(CrawlSpider):

    name = "france24crawler"
    #allowed_domains =[url[0][8:] for url in csv.reader(open('/home/chrx/Desktop/Scrapy/HezbollahScraper/urls.csv','r'),delimiter =',')]
    allowed_domains = ["www.france24.com"]
    custom_settings = {'FEED_FORMAT':"CSV",
    'FEED_URI':"/Users/Alex/Desktop/HezbollahScrapper/sample_output2.csv"}
    #start_urls = [url[0] for url in csv.reader(open('/home/chrx/Desktop/Scrapy/HezbollahScraper/urls.csv','r'),delimiter =',')]
    start_urls = ["https://www.france24.com/en/20181219-iran-israel-hezbollah-tunnels-missiles-lebanon-syria-nasrallah"]


 #possibly use process_links to to filter out links that dont mention hezbollah
    rules = [Rule(LinkExtractor(unique = True), follow=True, callback="check_buzzwords")]

    terms = []
    locations = []
    organizations = []
    wordlist = []

    with open('C:/Users/Alex/Desktop/HezbollahScrapper/terms_english.csv','r') as csvfile:
        terms_reader = csv.reader(csvfile,delimiter = ',')
        for row in terms_reader:
            terms.append(row[0])

    with open('C:/Users/Alex/Desktop/HezbollahScrapper/organizations_english.csv','r') as csvfile:
        terms_reader = csv.reader(csvfile,delimiter = ',')
        for row in terms_reader:
            organizations.append(row[0])
    for term in terms:
        for organization in organizations:
            wordlist.append(tuple((term,organization)))






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
