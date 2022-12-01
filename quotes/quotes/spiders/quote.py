import scrapy
from scrapy.http import FormRequest
# from scrapy.utils.response import open_in_browser
from ..items import QuotesItem


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']
    

    # Logging In ::::::
    def parse(self, response):
        token = response.xpath('//*[@name="csrf_token"]/@value').get()
        print(token)
        return FormRequest.from_response(response, formdata={
            'csrf_token': token,
            'username': 'averb@mail.ru',
            'password': 'sdsefdfsdf',
        }, callback=self.start_scraping)
        


    def start_scraping(self, response):
        # open_in_browser(response)
        item = QuotesItem()
        blocks = response.css('.quote')
        for i in blocks:
            title = i.css('.text::text').get()
            author = i.css('.author::text').get()
            tags = i.css('.tag::text').extract()

            item['title'] = title
            item['author'] = author
            item['tags'] = tags

            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.start_scraping)