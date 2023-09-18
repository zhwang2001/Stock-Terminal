import pandas as pd
from pandas import DataFrame
from yahooquery import Ticker
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from models.des_model import DesModel

class EqrvController:

    def __init__(self, hist_earnings, info_data, hist_range):
        self.hist_earnings = hist_earnings
        self.info_data = info_data
        self.hist_range = hist_range
        self.symbol = self.info_data.get('symbol')
        # use recommendations as equivalent peers
        self.ticker_list = []
        # the 5 stocks that are most similar to the selected tickers
        recommendations = Ticker(self.symbol).recommendations
        for recommendation in recommendations[self.symbol]['recommendedSymbols']:
            self.ticker_list.append(recommendation['symbol'])


    def handle_stock_info(self) -> dict[dict]:
        """
        event handler for recording info on the current stock
        Extracted from the yfinance api
        :return: dict
        """
        dc = DesModel(self.symbol)
        info = dc.get_info()
        trailing_eps = info.get('trailingEps')
        enterprise_to_revenue = info.get('enterpriseToRevenue')
        enterprise_to_ebitda = info.get('enterpriseToEbitda')
        quick_ratio = info.get('quickRatio')
        current_ratio = info.get('currentRatio')
        pegRatio = info.get('pegRatio')
        shortRatio = info.get('shortRatio')

        stock_summary_dict = {}
        stock_summary_dict[self.symbol] = {trailing_eps, enterprise_to_revenue,
                                           enterprise_to_ebitda, quick_ratio,
                                           current_ratio, pegRatio, shortRatio}
        return stock_summary_dict

    def handle_competitor_info(self, competitors: list[str] | None = None) -> DataFrame:
        """
        event handler for getting info on equivalent peers Aggregate information on the stock and competitors needed for equities comparison
        Extracted from the yahooquery api (faster for numerous tickers)
        :param competitors: custom list of competitors to compare and analyze, leave blank to find peers automatically
        :returns: {ticker: {'long_name': str, 'mkt_cap': int, 'current_pe_multiple': float, 'hist_pe_multiple': list[float]}}
        """
        # if no competitors are provided then utilize the recommended peer group from yahoo api
        if competitors is None:
            competitors = self.ticker_list
        # A dictionary filled with dictionaries containing the competitors long name, ticker, market cap, avg eps, pe multiple
        comp_info_dict = {}
        # join to form a string and pass as an argument to Ticker class
        all_symbols = " ".join(competitors)

        try:
            # query numerous ticker symbols quickly
            myInfo = Ticker(all_symbols)
            # earnings history data
            my_earnings_dict = myInfo.earning_history
            # earliest earnings date
            earliest_date_str = my_earnings_dict['quarter'].min()
            # go back a couple of days to avoid errors
            earlier_date = datetime.strptime(earliest_date_str, '%Y-%m-%d') - timedelta(days=5)

            # latest earnings date
            latest_date_str = my_earnings_dict['quarter'].max()
            # go forward a couple of days to avoid errors
            later_date = datetime.strptime(latest_date_str, '%Y-%m-%d') + timedelta(days=5)

            # stock summary data
            my_summary_dict = myInfo.price
            # historical price data
            my_historical_dict = myInfo.history(interval="1d", start=earlier_date, end=later_date)

            # Record this info for every stock in competitors
            for ticker in competitors:

                mkt_cap = my_summary_dict[ticker]['marketCap']
                long_name = my_summary_dict[ticker]['longName']
                current_price = my_summary_dict[ticker]['regularMarketPrice']

                dc = DesModel(ticker)
                info = dc.get_info()
                trailing_eps = info.get('trailingEps')
                enterprise_to_revenue = info.get('enterpriseToRevenue')
                enterprise_to_ebitda = info.get('enterpriseToEbitda')
                quick_ratio = info.get('quickRatio')
                current_ratio = info.get('currentRatio')
                pegRatio = info.get('pegRatio')
                shortRatio = info.get('shortRatio')

                # all earnings in an array
                all_eps = my_earnings_dict['epsActual'][ticker].values
                t12m_eps = sum(all_eps) / len(all_eps)
                # all earnings dates in an array
                all_eps_dates = my_earnings_dict['quarter'][ticker].values

                # index the 'close' column of the dataframe
                df = my_historical_dict.loc[ticker, 'close']
                date_objects = df.index.tolist()
                # convert datetime object to string
                date_strings = [date.strftime('%Y-%m-%d') for date in date_objects]


                # the end goal of this for loop is to divide the eps data by the stock price near the eps release date to obtain historical PE
                # 1. utilize yahoo query to obtain a range of historical stock prices
                # 2. store all the dates in an array
                # 3. index the stored dates using eps dates to obtain index
                # 4. index the historical stock prices using index to get prices on the eps release dates
                hist_comp_pe = []
                for index, eps_date in enumerate(all_eps_dates):
                    # some eps release dates are on the weekend while the historical prices are all business days
                    # if the eps_date can't be found in the historical stock prices then find the closest day
                    if eps_date not in date_strings:
                        stock = yf.Ticker(ticker)

                        start_date = datetime.strptime(eps_date, '%Y-%m-%d')
                        # go forward a couple of days to avoid errors
                        end_date = start_date + timedelta(days=5)

                        # use yfinance api to choose a close business day near eps release date
                        business_day = stock.history(start=start_date, end=end_date, interval="1d", rounding=True)
                        date_string = business_day.index[0].strftime('%Y-%m-%d')
                        alternative_price_index = date_strings.index(date_string)
                        comp_price = df[alternative_price_index]
                        eps = all_eps[index]
                        hist_pe_multiple = comp_price / float(eps)
                        hist_comp_pe.append(hist_pe_multiple)
                    else:
                        price_index = date_strings.index(eps_date)
                        comp_price = df[price_index]
                        eps = all_eps[index]
                        hist_pe_multiple = comp_price / float(eps)
                        hist_comp_pe.append(hist_pe_multiple)

                # calculate the most recent pe_multiple
                current_pe_multiple = current_price / float(trailing_eps)

                # Store info on each stock
                comp_info_dict[ticker] = {
                    "long_name": long_name,
                    "mkt_cap": mkt_cap,
                    "current_pe_multiple": current_pe_multiple,
                    "hist_pe_multiple": hist_comp_pe,
                    'enterprise/revenue': enterprise_to_revenue,
                    'enterprise/ebitda': enterprise_to_ebitda,
                    'currentRatio': current_ratio,
                    'quickRatio': quick_ratio,
                    'pegRatio': pegRatio,
                    'shortRatio': shortRatio,
                    't12m_eps': t12m_eps
                }
            return pd.DataFrame(data=comp_info_dict)
        except Exception as e:
            print("Failed to fetch data from api: ", str(e))



