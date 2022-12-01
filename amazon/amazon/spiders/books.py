import scrapy
from ..items import AmazonItem

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/gp/new-releases/books/5/ref=zg_bsnr_nav_books_1']

    def parse(self, response):
        item = AmazonItem()
        block = response.css('div#gridItemRoot')
        
        for i in block:
            names = i.css('.a-link-normal span div::text').get()
            author = i.css('.a-size-small ._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y::text').get()
            price = i.css('.p13n-sc-price , .a-color-price , ._cDEzb_p13n-sc-price_3mJ9Z').css('span::text').get()
            image = i.css('.p13n-product-image::attr(src)').get()

            item['name'] = names
            item['author'] = author
            item['price'] = price
            item['image'] = image
            yield item

        next_page = response.css('.a-last a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)