from scrapy.command import ScrapyCommand
import urllib
from urllib.parse import urlencode
import urllib.request
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import requests

class AllCrawlCommand(ScrapyCommand):
    requires_project = True
    default_settings = {'LOG_ENABLED': False}

    def short_desc(self):
        return "Schedule a run for all available spiders"

    def run(self, args, opts):
        setting = get_project_settings()
        process = CrawlerProcess(setting)

        url = 'http://localhost:6800/schedule.json'


            # adiciono cada site na lista
        settings = project.get_project_settings()
        spider_loader = spiderloader.SpiderLoader.from_settings(settings)
        spiders = spider_loader.list()
        for spider_name in spiders:
            print ("Running spider %s" % (spider_name))
            #process.crawl(spider_name,query="dvh") #query dvh is custom argument used in your scrapy
            values = {'project' : 'tutorial', 'spider' : spider_name}
            r = requests.post(url, data=values)
