import scrapy
from project.items import ProjectItem
from scrapy.loader import ItemLoader

class WhiskySpider(scrapy.Spider):
    name = 'item'
    start_urls = ['https://www.whiskyshop.com/scotch-whisky/all']

    def parse(self, response):
        for product in response.css('div.product-item-info'):
            yield response.follow(product.css('a.product-item-link::attr(href)').get(), callback=self.parse_page)
        #     l = ItemLoader(item=ProjectItem(), selector=product)
        #     l.add_css('name','a.product-item-link')
        #     l.add_css('price','span.price')
        #     l.add_css('link', 'a.product-item-link::attr(href)')

        #     yield l.load_item()

        # next_page = response.css('a.action.next').attrib['href']
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        name = response.css('h1.page-title::text').get().strip()
        price = response.css('span.price::text').get()
        brand = response.xpath("//dt[contains(text(), 'Distillery/Brand')]/following-sibling::dd[1]/text()").get()
        classification = response.xpath("//dt[contains(text(), 'Classification')]/following-sibling::dd[1]/a/text()").get()
        region = response.xpath("//dt[contains(text(), 'Region')]/following-sibling::dd[1]/text()").get()
        style = response.xpath("//dt[contains(text(), 'Style')]/following-sibling::dd[1]/a/text()").get()
        size = response.xpath("//dt[contains(text(), 'Size')]/following-sibling::dd[1]/text()").get()
        yield{
            'Name': name,
            'Price': price,
            'Brand': brand,
            'Classificaation': classification,
            'Region': region,
            'Style': style,
            'Size': size
        }
