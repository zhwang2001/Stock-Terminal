import requests
import pandas as pd
from typing import Literal

class EqrvModel:
    """
    Utilizes Alpha Vantage end points
    """
    def __init__(self, query):
        self.query = query
        self.api_key = 'JTD3X0ZN3D0B72D4'


    def get_intraday_data(self) -> pd.DataFrame:
        """
        Retrieves the intraday trading data
        :description:
            function = Time series intraday (intraday trading data)
            symbol = ticker symbol
            adjusted = Adjusted price incorporating stock splits
            interval = "1min", "5min", "15min", "30min", "60min"
        :return: pandas dataframe
        """
        interval = '60min'
        api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.query}&interval={interval}&adjusted=false&outputsize=full&apikey={self.api_key}"
        try:
            r = requests.get(api_url)
            data = r.json()
            return data[f"Time Series ({interval})"]
        except Exception as e:
            print(f"Could not fetch intraday trading data: {str(e)}")
            return pd.DataFrame()

    def get_earnings(self) -> dict[list]:
        """
        Retrieves a list of quarterly and annual dividends
        :return: dictionaries filled with date and earnings data (reported and estimated_eps)
        """
        api_url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={self.query}&apikey={self.api_key}'
        try:
            data = requests.get(api_url).json()
            quarterly_earnings = data['quarterlyEarnings']
            date_eps_dict = {}
            for date_eps in quarterly_earnings:
                reported_date = date_eps['reportedDate']
                reported_eps = date_eps['reportedEPS']
                estimated_eps = date_eps['estimatedEPS']
                date_eps_dict[reported_date] = [reported_eps, estimated_eps]
            return date_eps_dict

        except Exception as e:
            print(f"Could not fetch earnings data: {str(e)}")
            return {}



