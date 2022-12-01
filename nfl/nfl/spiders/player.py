import scrapy


class PlayerSpider(scrapy.Spider):
    name = 'player'
    allowed_domains = ['nfl.com']
    start_urls = ['https://www.nfl.com/players/active/a']
    def parse(self, response):
        pages = response.css('li.d3-o-tabs__list-item')
        for page in pages:
            url = page.css('a::attr(href)').get()
            yield response.follow(url, callback=self.parse_page)

    def parse_page(self, response):
        blocks = response.css('div.d3-o-media-object')
        for block in blocks:
            url = block.css('a::attr(href)').get()
            if url is not None:
                yield response.follow(url, callback=self.parse_info)

        next_page = response.css("a.nfl-o-table-pagination__next::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_page)


    def parse_info(self, response):

        name = response.css('h1.nfl-c-player-header__title::text').get()
        position = response.css('span.nfl-c-player-header__position::text').get().strip()
        team = response.css('a.nfl-o-cta--link::text').get()
        height = response.xpath("//div[contains(text(), 'Height')]/following-sibling::div/text()").get() # 
        weight = response.xpath("//div[contains(text(), 'Weight')]/following-sibling::div/text()").get()
        arms = response.xpath("//div[contains(text(), 'Arms')]/following-sibling::div/text()").get()
        hands = response.xpath("//div[contains(text(), 'Hands')]/following-sibling::div/text()").get()
        experience = response.xpath("//div[contains(text(), 'Experience')]/following-sibling::div/text()").get()
        age = response.xpath("//div[contains(text(), 'Age')]/following-sibling::div/text()").get()
        college = response.xpath("//div[contains(text(), 'College')]/following-sibling::div/text()").get()
        home = response.xpath("//div[contains(text(), 'Home')]/following-sibling::div/text()").get()
        yield{
            'Name': name,
            'Position': position,
            'Team': team,
            'Height': height,
            'Weight': weight,
            'Arms': arms,
            'Hands': hands,
            'Experience': experience,
            'Age': age,
            'College': college,
            'Home': home
        }
    