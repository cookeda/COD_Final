import scrapy
from sklearn.preprocessing  import OneHotEncoder
from datetime import datetime
import pandas as pd

import re

class MatchResultsSpider(scrapy.Spider):
    name = "Match_Results"
    allowed_domains = ["cdl.game5.gg"]
    start_urls = ["http://cdl.game5.gg/team"]

    # def parse(self, response):
    #     # Starting the crawl from the homepage to a specific match page
    #     # match_url = "https://cdl.game5.gg/major-3-qualifiers-2024/atlanta-faze-vs-carolina-royal-ravens/1605"
    #     yield scrapy.Request('https://cdl.game5.gg/major-2-qualifiers-2024/atlanta-faze-vs-los-angeles-guerrillas/1455', callback=self.parse_match_result)
    #     yield scrapy.Request('https://cdl.game5.gg/major-3-qualifiers-2024/atlanta-faze-vs-carolina-royal-ravens/1605', callback=self.parse_match_result)
    #     # yield scrapy.Request('https://cdl.game5.gg/team/atlanta-faze/2/results/p1', callback=self.parse_result_page)

    def parse(self, response):
        team_links = []
        for x in range (1, 13):
            team_links.append(response.css(f'li.product__item:nth-child({x}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').attrib['href'])
        for link in team_links:
            full_url = response.urljoin(link)
            print("Parse team:", full_url)
            yield scrapy.Request(full_url, callback=self.parse_team, meta={'full_url': full_url})


    def parse_team(self, response):
        team_name = response.css('h1::text').get()
        #full_url = response.urljoin('/result')

        print("Team: ", team_name)
        result_list_href = response.css('div.card--has-table > div:nth-child(1) > a:nth-child(2)').attrib['href']
        print("Parse result list:", result_list_href)
        full_url = response.urljoin(result_list_href)
        yield scrapy.Request(full_url, callback=self.parse_result_list, meta={'full_url': response.meta['full_url']})
    
    def parse_result_list(self, response):
        print("TESTING")
        results_pages = response.css('.pagination > li:nth-child(5) > a:nth-child(1)').extract_first()
        total_pages = int(re.search(r'(?<=/p)\d+', results_pages).group())
        print('Number of pages: ', total_pages)
        
        for page_num in range(1, total_pages + 1):
            page_url = f"{response.url}/p{page_num}"
            print("Processing page:", page_url)
            yield scrapy.Request(page_url, callback=self.parse_result_page, meta={'full_url': response.meta['full_url']})

    def parse_result_page(self, response):
        match_result_buttons = response.css('.table-hover > tbody > tr > td:nth-child(7) > a')
        
        for button in match_result_buttons:
            match_result_url = button.attrib['href']
            full_match_result_url = response.urljoin(match_result_url)
            print("Match url:", full_match_result_url)
            yield scrapy.Request(full_match_result_url, callback=self.parse_match_result, meta={'full_url': response.meta['full_url']})


    def parse_match_result(self, response):
        match_result_buttons = response.css('.table-hover > tbody > tr > td:nth-child(7) > a')
        
        for button in match_result_buttons:
            match_result_url = button.attrib['href']
            full_match_result_url = response.urljoin(match_result_url)
            print("Match url:", full_match_result_url)
            yield scrapy.Request(full_match_result_url, callback=self.parse_match_result, meta={'full_url': response.meta['full_url']})


    def parse_match_result(self, response):
        # Extracting scores using the correct method
        winner_score = response.css('.match_won::text').get()
        loser_score = response.css('.match_loss::text').get()

        tm1_score = response.xpath('/html/body/div/div[4]/div/div/div/div/div[1]/div/div[1]/div[4]/div[2]/div/h2/span[1]/text()').get()
        tm2_score = response.xpath('/html/body/div/div[4]/div/div/div/div/div[1]/div/div[1]/div[4]/div[2]/div/h2/span[2]/text()').get()

        tm1_name = response.css('div.live-match-team:nth-child(1) > h4:nth-child(2) > a:nth-child(1)::text').get()
        tm2_name = response.css('div.live-match-team:nth-child(3) > h4:nth-child(2) > a:nth-child(1)::text').get()

        tm1_win = (tm1_score == winner_score)

        date_text = response.css('.match-overview-subheader > p:nth-child(1)::text').get()
        date_text = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_text)
        date = pd.to_datetime(date_text, format="%A %d %B, %Y")


        yield {
            'date': date,
            't1': tm1_name.split(' ')[-1].upper(),
            't2': tm2_name.split(' ')[-1].upper(),
            'tm_1_score': tm1_score,
            'tm_2_score': tm2_score,
            'tm_1_win': tm1_win
        }

