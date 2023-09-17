import yfinance as yf
import pandas as pd

class DesModel:
    """
    Utilizes Yfinance api endpoints
    """

    def __init__(self, query):
        self.ticker = yf.Ticker(query)

    def get_info(self) -> dict:
        """
        Retrieves variety of info on the stock such as price metrics, corporate information, and financial data
        :return: info array
        """
        try:
            info = self.ticker.get_info()
            return info
        except Exception as e:
            print("Could not fetch security info: ", str(e))
            return {}

    def get_news(self) -> list[dict]:
        """
        Retrieves the latest news on the stock
        :return: news array
        """
        try:
            news = self.ticker.get_news()
            return news
        except Exception as e:
            print('Could not fetch news data')
            return []

    def get_history(self) -> pd.DataFrame:
        """
        Retrieves the historical market data on the stock
        :return: pandas dataframe
        """
        try:
            historical_price_data = self.ticker.history(period="5d", interval="2m")
            if isinstance(historical_price_data, pd.DataFrame):
                return historical_price_data
            else:
                raise Exception("Data not returned as DataFrame")
        except Exception as e:
            print(f"Could not fetch historical market data: {str(e)}")
            return pd.DataFrame()
