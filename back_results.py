import scrapy
import sqlite3

class ResultsSpider(scrapy.Spider):
    name = "results1"
    allowed_domains = ["cdl.game5.gg"]
    start_urls = ["https://cdl.game5.gg/major-3-qualifiers-2024/la-thieves-vs-miami-heretics/1573"]

    def __init__(self):
        self.conn = sqlite3.connect('cod_data.db')
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create tables if they don't exist
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

        # Add additional CREATE TABLE statements for other tables

    def close_spider(self, spider):
        self.conn.close()

    def parse_results_page(self, response):
        # Match Overview
        t1_name = response.css('div.live-match-team:nth-child(1) > h4:nth-child(2) > a:nth-child(1)::text').get()
        t2_name = response.css('div.live-match-team:nth-child(3) > h4:nth-child(2) > a:nth-child(1)::text').get()

        t1_score = response.css('.match_loss::text').get()
        t2_score = response.css('.match_won::text').get()

        team1_href = response.css('div.live-match-team:nth-child(1) > h4:nth-child(2) > a:nth-child(1)').attrib['href'] 
        team2_href = response.css('div.live-match-team:nth-child(3) > h4:nth-child(2) > a:nth-child(1)').attrib['href']
        print('Team hrefs:',  team1_href, team2_href)

        # team1_href = '/team/boston-breach/186'
        # team2_href = '/team/atlanta-faze/2'

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
        ''', (match_id, date, major, duration, team1_id, team2_id, winner_id, t1_score, t2_score, t1_ovr_kd, t2_ovr_kd, t1_total_kills, t2_total_kills, t1_avg_hill, t2_avg_hill, t1_fb, t2_fb, t1_fbed, t2_fbed, t1_caps, t2_caps, m1, t1_m1_kills, t1_m1_kd, t2_m1_kills, t2_m1_kd, m2, t1_m2_kills, t2_m2_kills, t1_m2_kd, t2_m2_kd, m3, t1_m3_kills, t2_m3_kills, t1_m3_kd, t2_m3_kd))
        self.conn.commit()

        print("Success")

