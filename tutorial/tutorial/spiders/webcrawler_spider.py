import re
from io import StringIO
from functools import partial
from scrapy.http import Request
from scrapy.spiders import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.item import Item
from tutorial.items import TutorialItem


def find_all_substrings(string, sub):
    #list comprehension using regex doing what??
    #re.escape matches patterns that may have regular expression metacharacters
    #pattern = r'((\b{domain}\b)(?!.*\2).*\bHezbollah\b)|((\bhezbollah\b)(?!.*\4).*\b{domain}\b)'.format(domain = sub)
    #change it so it only goes from beginning of text to keyword#
    pattern = r'(\b{domain}\b.*\bHezbollah\b)|(\bHezbollah\b.*\b{domain}\b)'.format(domain = sub)
    return re.search(pattern,string)

class GenericSpider(CrawlSpider):

    name = "webcrawler"
    allowed_domains = ["www.aljazeera.com","www.counterextremism.com","www.nytimes.com","www.theatlantic.com/international"]
    start_urls = ["https://www.aljazeera.com/topics/organisations/hezbollah.html","https://www.counterextremism.com","https://www.nytimes.com/topic/organization/hezbollah","https://www.theatlantic.com/international/archive/2018/05/lebanon-election-hezbollah-sunni-shia/559772/"]

    #possibly use process_links to to filter out links that dont mention hezbollah
    rules = [Rule(LinkExtractor(unique = True), follow=True, callback="check_buzzwords")]

    #handles each individual request given to the parsing function



    def check_buzzwords(self, response):

        wordlist = ["hospital","mosque","clinic","charitable","Jihad al-Binaa","charitable","school","medical centers","al-Waad al-Sadiq"]
        url = response.url
        contenttype = response.headers.get("content-type", "").decode('utf-8').lower()
        items = []

        paragraph_text = response.css("p::text")
        p_texts = [p.get() for p in paragraph_text]

        for p_text in p_texts:
            for word in wordlist:
                if word in p_text and "Hezbollah" in p_text:
                    item = TutorialItem()
                    item["word"] = word
                    item["url"] = url
                    item["sentence"] = p_text
                    items.append(item)
                #found = find_all_substrings(p_text, word)
                    #if(found != None):
                    #    item["sentence"] = found.group(0)

        return(items)

    #gets the requests to follow recursively
    def _requests_to_follow(self, response):
        if getattr(response, "encoding", None) != None:
                return CrawlSpider._requests_to_follow(self, response)
        else:
                return []
