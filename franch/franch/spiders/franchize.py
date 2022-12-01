import scrapy
from ..items import FranchItem
import csv

class FranchizeSpider(scrapy.Spider):
    name = "franchize"
    allowed_domains = ['www.franchisedirect.com']
    start_urls = ['https://www.franchisedirect.com/top100globalfranchises/']
    
    def parse(self, response):
        list = response.css('ul.reportsList')
        urls = list.css('a.btn.navy::attr(href)')
        year = 2022
        
        for url in urls:
            yield scrapy.Request(
                url=url.get(), 
                callback=self.parse_items,
            )
            with open(f"ranks{year}.csv", "w") as csv_file:
                writer = csv.writer(csv_file, delimiter="\n")
                writer.writerow(['Rank, Name, Country, Industry, URL'])
            year -= 1

    def parse_items(self, response):
        item = FranchItem()
        year = response.css('h1.pageTitle::text').get().replace('Top 100 Franchises ', '')
        ranks = response.xpath("//td[@data-title='Rank']")
        names = response.xpath("//td[@data-title='Name']")
        countries = response.xpath("//td[@data-title='Country']")
        industries = response.xpath("//td[@data-title='Industry']")
        urls = response.xpath("//td[@data-title='Name']/span/a/@href")
        
        
        for i, pos in enumerate(ranks):
            rank = pos.css('span::text').get()
            name = names[i].css('a').css('span::text').get()
            country = countries[i].css('span::text').get()
            industry = industries[i].css('a::text').get()
            urla = urls[i].get()
            with open(f"ranks{year}.csv", "a+") as csv_file:
                write = csv.writer(csv_file)
                write.writerow([rank, name, country, industry, urla])
            
            item['rank'] = rank
            item['name'] = name
            item['country'] = country
            item['industry'] = industry
            item['year'] = year
            item['url'] = urla

            yield item

        next_page = response.xpath("//div[@class='col span2point4']/a[@class='btn select blue ']/parent::div/following-sibling::div/a[@class='btn grey']/@href").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_items)