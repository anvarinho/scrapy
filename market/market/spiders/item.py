import scrapy
import gspread
import time

class ItemSpider(scrapy.Spider):
    name = 'item'
    allowed_domains = ['mixergy.com']
    start_urls = ['https://mixergy.com/interviews/']
    page_num = 2
    count = 2
    
    gc = gspread.service_account()
    sh = gc.open("Mixergy")
    sh.sheet1.update('A1:D1', [['Date','Guest Name','Sponsor 1','Sponsor 2']])

    def parse(self, response):
        table = response.css('div.row')
        items = table.css('div.col-sm-4')
        for item in items:
            try:
                name = item.css('h3::text').get().strip()
            except:
                name = ''
            yield scrapy.Request(
                url=item.css('div.content').css('a::attr(href)').get(),
                callback=self.parse_item,
                cb_kwargs={
                    'name': name,
                    'date': item.css('div.date::text').get().strip(),
                }
            )
        next_page = f'https://mixergy.com/interviews/page/{str(ItemSpider.page_num)}/'
        if ItemSpider.page_num <= 147:
            ItemSpider.page_num += 1
            yield response.follow(next_page, callback=self.parse)
        # pass

    def parse_item(self, response, name, date):
        table = response.css('div.col-sm-12')
        par = table.css('p')
        if len(par) > 0:
            sponsor1 = par[0].css('a::text').get()
        else:
            sponsor1 = ''
        if len(par) > 1:
            if par[1].css('a::text').get() == 'HostGator' and len(par) > 2 and sponsor1 == 'HostGator':
                sponsor2 = par[2].css('a::text').get()
            else:
                if sponsor1 != 'HostGator':
                    sponsor2 = par[1].css('a::text').get()
                else:
                    sponsor2 = ''
        else:
            sponsor2 = ''
        yield{
            'date':date,
            'name':name,
            'sponsor1':sponsor1,
            'sponsor2':sponsor2,
        }
        ItemSpider.sh.sheet1.update(f'A{ItemSpider.count}:D{ItemSpider.count}', [[date, name, sponsor1, sponsor2]])
        ItemSpider.count += 1
        time.sleep(1)