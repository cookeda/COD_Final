import scrapy
import pandas as pd
import sqlite3
import re

class TeamsSpider(scrapy.Spider):
    name = "results"
    allowed_domains = ["cdl.game5.gg"]
    start_urls = ["https://cdl.game5.gg/major-3-qualifiers-2024/atlanta-faze-vs-carolina-royal-ravens/1605"]


    def parse(self, response):
        team_links = []
        for x in range (1, 13):
            team_links.append(response.css(f'li.product__item:nth-child({x}) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1)').attrib['href'])
        for link in team_links:
            full_url = response#.urljoin(link)
            print("Parse team:", full_url)
            yield scrapy.Request(full_url, callback=self.parse_team, meta={'full_url': full_url})

    def parse_match_result(self, response):
        print("MATCH RESULT PARSE")
        t1_name = response.css('div.live-match-team:nth-child(1) > h4:nth-child(2) > a:nth-child(1)::text').get()
        t2_name = response.css('div.live-match-team:nth-child(3) > h4:nth-child(2) > a:nth-child(1)::text').get()

        t1_score = response.css('.match_loss::text').get()
        t2_score = response.css('.match_won::text').get()

        team1_href = response.css('div.live-match-team:nth-child(1) > h4:nth-child(2) > a:nth-child(1)').attrib['href'] 
        team2_href = response.css('div.live-match-team:nth-child(3) > h4:nth-child(2) > a:nth-child(1)').attrib['href']
        print('Team hrefs:',  team1_href, team2_href)

        team1_id = team1_href.split('/')[-1]
        team2_id = team2_href.split('/')[-1]
        print(team1_id, team2_id)

        
        match_id = response.url.split('/')[-1]
        duration = response.css('.live-match-duration::text').get()
        date = response.css('.match-overview-subheader > p:nth-child(1)::text').get()
        major = response.css('.match-overview-time > h5:nth-child(1) > a:nth-child(1)::text').get()


#   # Match Report

        # Additional Statistics
        t1_total_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(1) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_m1_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(2) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_m2_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(3) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_m3_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(4) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_avg_hill = response.css('li.alc-event-result-box__stats-circular-item:nth-child(5) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_fb = response.css('li.alc-event-result-box__stats-circular-item:nth-child(6) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_fbed = response.css('li.alc-event-result-box__stats-circular-item:nth-child(7) > div:nth-child(1) > span:nth-child(1)::text').get()
        t1_caps = response.css('li.alc-event-result-box__stats-circular-item:nth-child(8) > div:nth-child(1) > span:nth-child(1)::text').get()

        t2_total_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(1) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_m1_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(2) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_m2_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(3) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_m3_kills = response.css('li.alc-event-result-box__stats-circular-item:nth-child(4) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_avg_hill = response.css('li.alc-event-result-box__stats-circular-item:nth-child(5) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_fb = response.css('li.alc-event-result-box__stats-circular-item:nth-child(6) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_fbed = response.css('li.alc-event-result-box__stats-circular-item:nth-child(7) > div:nth-child(1) > span:nth-child(2)::text').get()
        t2_caps = response.css('li.alc-event-result-box__stats-circular-item:nth-child(8) > div:nth-child(1) > span:nth-child(2)::text').get()

        # Team Overall KD and Mode KD
        t1_ovr_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1)::text').get()
        t1_m1_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1)::text').get()
        t1_m2_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1)::text').get()
        t1_m3_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1)::text').get()
        
        t2_ovr_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(5)::text').get()
        t2_m1_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(5)::text').get()
        t2_m2_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(5)::text').get()
        t2_m3_kd = response.css('.progress-table > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(5)::text').get()

        m1_element = response.css('li.alc-event-result-box__stats-circular-item:nth-child(2) > div:nth-child(2) > span:nth-child(1)::text').get()
        m2_element = response.css('li.alc-event-result-box__stats-circular-item:nth-child(3) > div:nth-child(2) > span:nth-child(1)::text').get()
        m3_element = response.css('li.alc-event-result-box__stats-circular-item:nth-child(4) > div:nth-child(2) > span:nth-child(1)::text').get()

        m1 = m1_element.split(' ')[0]
        m2 = m2_element.split(' ')[0]
        m3 = m3_element.split(' ')[0]

        yield {
            't1_total_kills'
        }

        winner_id = team2_id
        if t1_score > t2_score:
            winner_id = team1_id
        pass