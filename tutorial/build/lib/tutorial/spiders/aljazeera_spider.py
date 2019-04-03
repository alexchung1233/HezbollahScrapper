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

class AljazeeraSpider(CrawlSpider):

    name = "aljazeeracrawler"
    #allowed_domains =[url[0][8:] for url in csv.reader(open('/home/chrx/Desktop/Scrapy/HezbollahScraper/urls.csv','r'),delimiter =',')]
    allowed_domains = ["www.aljazeera.com"]

    #start_urls = [url[0] for url in csv.reader(open('/home/chrx/Desktop/Scrapy/HezbollahScraper/urls.csv','r'),delimiter =',')]
    start_urls = ["https://www.aljazeera.com"]



    #start_urls = ["https://www.aljazeera.com/topics/organisations/hezbollah.html","https://www.nytimes.com/topic/organization/hezbollah"
    #            ,"https://www.theatlantic.com/international/archive/2018/05/lebanon-election-hezbollah-sunni-shia/559772/"
    #            ,"https://www.thenational.ae/world/mena/us-warns-of-growing-hezbollah-influence-as-lebanon-nears-agreement-on-new-government-1.804342",
    #            "https://www.washingtonpost.com/world/middle_east/hezbollah-on-the-rise-in-lebanon-fends-off-saudi-arabia/2017/11/23/d9d92b1c-c961-11e7-b506-8a10ed11ecf5_story.html?noredirect=on&utm_term=.f147561e9014",
    #            "https://www.counterextremism.com",
    #            "https://www.bbc.com/news/world-middle-east-10814698",
    #            "https://www.presstv.com/Detail/2018/12/19/583358/Lebanon-US-Israel-Hezbollah-influence-political-system-war"]
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
