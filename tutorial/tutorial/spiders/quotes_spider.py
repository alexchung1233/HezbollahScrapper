import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
    'https://www.counterextremism.com/hezbollah-in-lebanon'
    ]

    def parse(self, response):
        for item in response.css('.field.field-type-text-with-summary div.hezbollah p'):
            yield {
                'text': item.css('::text').get().strip()
        }
        '''next_page = response.css('li.next a').attrib['href'].get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback = self.parse)'''
