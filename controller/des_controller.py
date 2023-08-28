import yfinance as yf

class DesController:

    def __init__(self, query):
        self.query = query
        self.ticker = yf.Ticker(self.query)

    def get_info(self) -> list[dict]:
        """
        Retrieves variety of info on the stock such as price metrics, corporate information, and financial data
        :return: info array
        """
        info = self.ticker.get_info()
        return info

    def get_news(self) -> list[dict]:
        """
        Retrieves the latest news on the stock
        :return: news array
        """
        news = self.ticker.get_news()
        return news

    def get_history(self):
        """
        Retrieves the historical market data on the stock
        :return: history nested array
        """
        """
        history = yf.download(str(self.ticker), start="2023-01-01", end="2023-01-15")
        print(history['Close'].values)
        return history
        """
        return self.ticker.history(period='5d', interval="2m")

