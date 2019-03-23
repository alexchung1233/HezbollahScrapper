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


def find_all_substrings(string, sub):
    #list comprehension using regex doing what??
    #re.escape matches patterns that may have regular expression metacharacters
    #pattern = r'((\b{domain}\b)(?!.*\2).*\bHezbollah\b)|((\bhezbollah\b)(?!.*\4).*\b{domain}\b)'.format(domain = sub)
    #change it so it only goes from beginning of text to keyword#
    pattern = r'(\b{domain}\b.*\bHezbollah\b)|(\bHezbollah\b.*\b{domain}\b)'.format(domain = sub)
    return re.search(pattern,string)

class GenericSpider(CrawlSpider):

    name = "webcrawler"
    #allowed_domains =[url[0][8:] for url in csv.reader(open('C:/Users/Alex/Desktop/HezbollahScrapper-master/urls.csv','r'),delimiter =',')]
    allowed_domains = ["www.dailystar.com.lb","www.counterextremism.com","www.bbc.com"]
    #,"www.aljazeera.com","www.nytimes.com","www.theatlantic.com","www.thenational.ae/world","www.washingtonpost.com/world","www.bbc.com/news","www.presstv.com"]
    #start_urls = ["https://www.aljazeera.com/topics/organisations/hezbollah.html","https://www.nytimes.com/topic/organization/hezbollah"
    #            ,"https://www.theatlantic.com/international/archive/2018/05/lebanon-election-hezbollah-sunni-shia/559772/"
    #            ,"https://www.thenational.ae/world/mena/us-warns-of-growing-hezbollah-influence-as-lebanon-nears-agreement-on-new-government-1.804342",
    #            "https://www.washingtonpost.com/world/middle_east/hezbollah-on-the-rise-in-lebanon-fends-off-saudi-arabia/2017/11/23/d9d92b1c-c961-11e7-b506-8a10ed11ecf5_story.html?noredirect=on&utm_term=.f147561e9014",
    #            "https://www.counterextremism.com",
    #            "https://www.bbc.com/news/world-middle-east-10814698",
    #            "https://www.presstv.com/Detail/2018/12/19/583358/Lebanon-US-Israel-Hezbollah-influence-political-system-war"]
    #start_urls = [url[0] for url in csv.reader(open('C:/Users/Alex/Desktop/HezbollahScrapper-master/urls.csv','r'),delimiter =',')]
    start_urls = ["http://www.dailystar.com.lb","http://www.counterextremism.com","https://www.aljazeera.com"]

    #possibly use process_links to to filter out links that dont mention hezbollah
    rules = [Rule(LinkExtractor(unique = True), follow=True, callback="check_buzzwords")]

    terms = []
    locations = []
    organizations = []
    wordlist = []
    with open('C:/Users/Alex/Desktop/HezbollahScrapper-master/terms.csv','r') as csvfile:
        terms_reader = csv.reader(csvfile,delimiter = ',')
        for row in terms_reader:
            terms.append(row[0])
            organizations.append(row[1])
    for term in terms:
        for indx in range(0,5):
            wordlist.append(tuple((term,organizations[indx])))


    def __init__(self, category=None, *args, **kwargs):
        self.rules = [Rule(LinkExtractor(unique = True), follow=True, callback="check_words")]
        super(GenericSpider, self).__init__(*args, **kwargs)






    def check_words(self, response):
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
                #found = find_all_substrings(p_text, word)
                    #if(found != None):
                    #    item["sentence"] = found.group(0)

        return(items)
    def parse_item(self, response):
        print('!!!!!!!!!!!!! Parsing: %s !!!!!!!!!!!!!' % response.url)

        # Check the Content-Type.
        if is_content_type_ok(response.headers.getlist('Content-Type')):
            # Yield data here
            yield {}


    #gets the requests to follow recursively
    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) != None:
                return CrawlSpider._requests_to_follow(self, response)
        else:
                return []
