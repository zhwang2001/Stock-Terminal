import scrapy
from bs4 import BeautifulSoup


class BS4():
    def __init__(self, html_text):
        self.html_text = html_text
    def remove_html_tags(self):
        soup = BeautifulSoup(self.html_text, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)
        return text_content

class StockNewsSpider(scrapy.Spider):
    name = "StockNews"

    def start_requests(self):
        # urls = ['https://www.cnbc.com/2024/01/11/5-things-to-know-before-the-stock-market-opens-thursday-january-11.html']
        urls = ['https://finance.yahoo.com/news/16-most-widely-held-stocks-203143195.html',
                'https://finance.yahoo.com/m/1b114d0a-7d30-3cf1-83f8-e108bf2cc035/dow-jones-futures%3A-nvidia%2C.html',
                'https://finance.yahoo.com/m/48f00b3b-0ab3-3137-8661-8b4f9499ab3f/2-stock-split-ai-stocks-to.html',
                'https://finance.yahoo.com/m/a721ff5e-42c5-3846-947b-afd6a67f91fa/better-tech-stock%3A-nvidia-vs..html',
                'https://finance.yahoo.com/m/96374b0d-4e16-36c6-b6d6-28aa1a5a329e/missed-the-boat-on-nvidia%3F.html',
                'https://finance.yahoo.com/m/41e527d9-0ba9-39de-943b-3b9a0b0bf4b7/2-stock-spilt-stocks-crushing.html',
                'https://finance.yahoo.com/m/568425ee-40bf-31f2-ab79-067ec3a3b11f/are-the-%22magnificent-seven%22.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        page = response.url.split("/")[-2]
        site_name = f"stock_news-{page}.html"
        #html_string = response.css("div.caas-body").get()
        html_string = {site_name: response.body}

        site_html_string = {site_name : html_string}
        print(site_html_string)

        # text_only = BS4(site_html_string).remove_html_tags()
        # print('\n\n\n\n\n', text_only, '\n\n\n\n\n')

        #dict = {site_name: response.text}
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")


