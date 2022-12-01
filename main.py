import scrapy

class ItemSpider(scrapy.Spider):
    name = 'item'
    start_urls = ['https://lainelir2.pythonanywhere.com']

    def parse(self, response):
        for link in response.css('div.container-link a::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_page)

        next_page = response.xpath("//a[@class='link-page-view']/following-sibling::a[@class='link-page']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
                  
    def parse_page(self, response):
        title = response.css('div.title::text').get()
        text = response.css('div.text-view::text').getall()
        comments = response.css('a.text-reply::text').getall()
        list = []
        for i in text:
            if i.strip() != '':
                list.append(i.strip().replace('\r\n', ''))
        list1 = []
        for i in comments:
            if i.strip() != '':
                list1.append(i.strip())
        yield{
            'Title': title,
            'Text': list,
            'Comments': list1,
        }