import yfinance as yf

class DesController:

    def __init__(self, query):
        self.query = query

    def get_info(self):
        """
        Retrieves variety of info on the stock
        :return: info
        """
        ticker = yf.Ticker(self.query)
        info = ticker.get_info()
        print(info)
        return info

    def get_open_price(self):
        """
        Retrieves the last opening price of the stock
        :return: open price
        """
        return "open_price"


    def get_close_price(self):
        """
        Retrieves the last closing price of the stock
        :return: close price
        """
        return "close_price"


    def get_low_price(self):
        """
        Retrieves the last lowest transaction price of the stock
        :return: low price
        """
        return "low_price"


    def get_high_price(self):
        """
        Retrieves the last highest transaction price of the stock
        :return: high price
        """
        return "high_price"


    def get_description(self):
        """
        Retrieves the description of the security
        :return: description
        """
        return "description"


    def get_stock_name(self):
        """
        Retrieves the name of the security
        :return: name
        """
        return "name"
