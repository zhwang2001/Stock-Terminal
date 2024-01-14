import feedparser
import ssl
from bs4 import BeautifulSoup
import requests


def get_news():
    """
   Send a message to a recipient.
   :return: dictionary whose keys are titles of news article and values are the content of the news article, 
   if error, error is the value of the title's value
   :rtype: dict
   """
    ret_value = {}
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    NewsFeed = feedparser.parse("https://finance.yahoo.com/news/rssindex")
    for entry in NewsFeed.entries:
        try:
            print(entry.title)
            print(entry.link)
            data = requests.get(entry.link)
            soup = BeautifulSoup(data.text, 'html.parser')
            content = soup.find("div", {"class": "caas-body"})
            print(content.text)
            ret_value[entry.title] = content.text
        except:
            print("error")
    return ret_value
