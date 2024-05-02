import scrapy
import pandas as pd

class TeamsSpider(scrapy.Spider):
    name = "teams"
    allowed_domains = ["cdl.game5.gg"]
    start_urls = ["https://cdl.game5.gg/teams"]

    def parse(self, response):
        # Extracting team page links
        team_links = response.css('li.product__item div:nth-child(2) div:nth-child(1) div:nth-child(1) h2:nth-child(1) a::attr(href)').getall()
        for link in team_links:
            full_url = response.urljoin(link)
            print("Queueing team page:", full_url)
            yield scrapy.Request(full_url, callback=self.parse_team, meta={'full_url': full_url})

    #TODO: Go to all results pages
    def parse_team(self, response):
        team_name = response.css('h1::text').get()
        results_url = response.meta['full_url'] + '/results'
        
        print("Constructed URL for results:", results_url)
        yield scrapy.Request(results_url, callback=self.parse_results, meta={'team_name': team_name})

    def parse_results(self, response):
        # Debug information
        print("Debug Response URL:", response.url)
        print("Debug Meta Team Name:", response.meta.get('team_name', 'No Team Name Found'))
        
        # Extracting match links
        match_links = response.css('.table-hover > tbody:nth-child(2) > tr:nth-child(10) > td:nth-child(7) > a:nth-child(1)::attr(href)').getall()  # Update selector as needed
        for link in match_links:
            match_url = response.urljoin(link)
            print("Queueing match page:", match_url)
            yield scrapy.Request(match_url, callback=self.parse_match, meta={'team_name': response.meta['team_name']})

    def parse_match(self, response):
        # Using CSS selector to extract table data
        rows = response.css('.match-report-section > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(2)')  # Replace with your actual CSS selector
        data = []
        for row in rows:
            cells = row.css('td::text').getall()  # Adjust as necessary for the structure
            data.append(cells)
        
        # Converting data to DataFrame and saving as CSV
        df = pd.DataFrame(data)
        filename = f"{response.meta['team_name']}_{response.url.split('/')[-1]}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved data to {filename}")

        yield {
            'team_name': response.meta['team_name'],
            'match_id': response.url.split('/')[-1],
            'filename': filename
        }