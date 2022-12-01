import scrapy


class DronesspiderSpider(scrapy.Spider):
    name = 'dronesspider'
    allowed_domains = ['jessops.com/drones']
    start_urls = ['http://jessops.com/drones']

    def parse(self, response):
        products = response.css('div.details-pricing')
        for product in products:
            item = {
                'name': product.css('a::text').get(),
                'price': product.css('p.price.larger::text').get().replace('£', ''),
                'description': product.css('ul.f-list.j-list').css('li::text').getall()
            }
            yield item
        pass
