import scrapy
import json

class ListSpider(scrapy.Spider):
    name = 'list'
    allowed_domains = ['directory.ntschools.net']
    start_urls = ['https://directory.ntschools.net/#/schools']

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://directory.ntschools.net/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
        'X-Requested-With': 'Fetch',
    }

    def parse(self, response):
        url = 'https://directory.ntschools.net/api/System/GetAllSchools'
        request = scrapy.Request(url, callback=self.parse_api, headers=self.headers)
        yield request

    def parse_api(self, response):
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='
        raw_data = response.body
        data = json.loads(raw_data)
        for school in data:
            school_code = school['itSchoolCode']
            school_url = base_url + school_code
            yield scrapy.Request(school_url, callback=self.parse_school, headers=self.headers)

    def parse_school(self, response):
        raw_data = response.body
        data = json.loads(raw_data)
        yield {
            'Name': data['name'],
            'PhysicalAddress': data['physicalAddress']['displayAddress'],
            'PostalAddress': data['postalAddress']['displayAddress'],
            'Email': data['mail'],
            'Phone': data['telephoneNumber'],
            data['schoolManagement'][0]['position'] : data['schoolManagement'][0]['firstName'] + ' ' + data['schoolManagement'][0]['lastName'],
            data['schoolManagement'][1]['position'] : data['schoolManagement'][1]['firstName'] + ' ' + data['schoolManagement'][1]['lastName'],
            'Location': [f'{data["long"]}',f'{data["lat"]}'],
            'Directorate': data['directorate']
        }