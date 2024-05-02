import scrapy


class TeamsSpider(scrapy.Spider):
    name = "teams"
    allowed_domains = ["cdl.game5.gg"]
    start_urls = ["https://cdl.game5.gg/teams"]

    def parse(self, response):
        pass
