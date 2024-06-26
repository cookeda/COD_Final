import scrapy
import pandas as pd
import sqlite3
import re

class TeamsSpider(scrapy.Spider):
    name = "results"
    allowed_domains = ["cdl.game5.gg"]
    start_urls = ["https://cdl.game5.gg/teams"]


    def __init__(self):
        self.conn = sqlite3.connect('cod_results.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''DROP TABLE IF EXISTS Matches;''')
        
        self.cur.execute('''CREATE TABLE IF NOT EXISTS Matches (
            Match_ID TEXT PRIMARY KEY,
            Date TEXT,
            Event TEXT,
            Duration TEXT,
            Tm_1_ID INTEGER,
            Tm_2_ID INTEGER,
            Winner_ID INTEGER,
            Tm_1_Score INTEGER,
            Tm_2_Score INTEGER,
            Tm_1_Ovr_KD REAL,
            Tm_2_Ovr_KD REAL,
            Tm_1_Tot_Kills INTEGER,
            Tm_2_Tot_Kills INTEGER,
            Tm_1_Hill BLOB,
            Tm_2_Hill BLOB,
            Tm_1_FB INTEGER,
            Tm_2_FB INTEGER,
            Tm_1_FBed INTEGER,
            Tm_2_FBed INTEGER,
            Tm_1_Caps INTEGER,
            Tm_2_Caps INTEGER,
            M1 TEXT,
            Tm_1_M1_Kills INTEGER,
            Tm_2_M1_Kills INTEGER,
            Tm_1_M1_KD REAL,
            Tm_2_M1_KD REAL,
            M2 TEXT,
            Tm_1_M2_Kills INTEGER,
            Tm_2_M2_Kills INTEGER,
            Tm_1_M2_KD REAL,
            Tm_2_M2_KD REAL,
            M3 TEXT,
            Tm_1_M3_Kills INTEGER,
            Tm_2_M3_Kills INTEGER,
            Tm_1_M3_KD REAL,
            Tm_2_M3_KD REAL
        )''')

        # self.cur.execute('''CREATE TABLE IF NOT EXISTS Player_Match_Stats (
        #     Report_ID TEXT PRIMARY KEY,
        #     Match_ID TEXT FOREIGN KEY,
        #     Player_ID TEXT FOREIGN KEY,
        #     Team_ID TEXT FOREIGN KEY,
        #     Kills INTEGER,
        #     Deaths INTEGER,
        #     K/D REAL,
        #     +/- REAL,
        #     DMG INTEGER,
        #     Fantasy REAL,
                          
        # )''')

        # self.cur.execute('''CREATE TABLE IF NOT EXISTS Player_Match_Stats (
        #     Stat_ID TEXT PRIMARY KEY,
        #     Match_ID TEXT FOREIGN KEY,
        #     Total_Kills TEXT FOREIGN KEY,
        #     M1 Kills TEXT FOREIGN KEY,
        #     M2 Kills INTEGER,
        #     M3 Kills INTEGER,
        #     K/D REAL,
        #     +/- REAL,
        #     DMG INTEGER,
        #     Fantasy REAL, 
        # )''')

    def close_spider(self, spider):
        self.conn.close()


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

        winner_id = team2_id
        if t1_score > t2_score:
            winner_id = team1_id
        
        print(winner_id)

        self.cur.execute('''
            INSERT INTO Matches (Match_ID, Date, Event, Duration, Tm_1_ID, Tm_2_ID, Winner_ID, Tm_1_Score, Tm_2_Score, Tm_1_Ovr_KD, Tm_2_Ovr_KD, Tm_1_Tot_Kills, Tm_2_Tot_Kills, Tm_1_Hill, Tm_2_Hill, Tm_1_FB, Tm_2_FB, Tm_1_FBed, Tm_2_FBed, Tm_1_Caps, Tm_2_Caps, M1, Tm_1_M1_Kills, Tm_2_M1_Kills, Tm_1_M1_KD, Tm_2_M1_KD, M2, Tm_1_M2_Kills, Tm_2_M2_Kills, Tm_1_M2_KD, Tm_2_M2_KD, M3, Tm_1_M3_Kills, Tm_2_M3_Kills, Tm_1_M3_KD, Tm_2_M3_KD)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (match_id, date, major, duration, team1_id, team2_id, winner_id, t1_score, t2_score, t1_ovr_kd, t2_ovr_kd, t1_total_kills, t2_total_kills, t1_avg_hill, t2_avg_hill, t1_fb, t2_fb, t1_fbed, t2_fbed, t1_caps, t2_caps, m1, t1_m1_kills, t2_m1_kills, t1_m1_kd, t2_m1_kd, m2, t1_m2_kills, t2_m2_kills, t1_m2_kd, t2_m2_kd, m3, t1_m3_kills, t2_m3_kills, t1_m3_kd, t2_m3_kd))
        self.conn.commit()

        print("Success")
        pass