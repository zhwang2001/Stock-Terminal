import tkinter as tk
from tkinter import ttk

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from utilities.utils import date_conversion
from datetime import datetime
from controllers.des_controller import handle_on_enter, handle_on_leave, handle_open_link

class Des:
    """
    Broad overview of the stocks, encompassing, financial and news data
    """
    def __init__(self, active_frame, info_data, history_data, news_data, win_width, win_height):
        """
        Initialization of variables
        :param active_frame: Master widget containing all the currently active slave widgets
        :param info_data: A large quantity of data on the stock
        :param history_data: Historical price data on the stock
        :param news_data: The most recent 8 news articles
        :param win_width: The window's width
        :param win_height: The window's height
        """
        self.active_frame = active_frame
        self.info_data = info_data
        self.news_data = news_data
        self.history_data = history_data
        self.win_width = win_width - 20
        self.win_height = win_height

        # Master widget for all widgets in the des function
        self.des_master = tk.Frame(self.active_frame, bg="black", width=self.win_width)
        self.des_master.grid(sticky="nsew", row=0, column=0, columnspan=3)
        self.des_master.rowconfigure(0, weight=1)
        self.des_master.columnconfigure(0, weight=1)


    def main(self):
        self.security()
        self.description()
        self.hist_price_plot()
        self.news()
        self.price_metrics()
        self.earnings_dividends()
        self.corporate_info()

    def security(self):
        """Key details about the security such as the price per share and the volume traded"""
        security_frame = tk.LabelFrame(self.des_master, bg="black", fg="white", text="Security")
        security_frame.grid(columnspan=5, sticky="nsew", row=0, column=0)

        stock_name = tk.Label(security_frame, bg="black", fg="deep sky blue",
                              font="Helvetica 12 bold", text=self.info_data.get('longName'))
        stock_name.grid(row=1, column=0, sticky="nw")

        ticker_volume_frame = tk.Frame(security_frame, bg="black")
        ticker_volume_frame.grid(row=2, column=0, stick="nw")
        ticker = tk.Label(ticker_volume_frame, bg="black", fg="orange", font="Helvetica 10",
                          text=f"{self.info_data.get('symbol')}")
        ticker.grid(row=0, column=0, sticky="w")

        volume = tk.Label(ticker_volume_frame, bg="black", fg="white", font="Helvetica 10",
                          text=f"VOL {self.info_data.get('volume')}")
        volume.grid(row=0, column=3, sticky="e")

        # Closing price of the day
        close_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                               fg="light green", text=f"C: ${round(self.info_data.get('currentPrice'), 2)}")
        close_price.grid(row=1, column=1)

        # Opening price of the day
        open_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                              fg="light green", text=f"O: ${round(self.info_data.get('open'), 2)}")
        open_price.grid(row=2, column=1)

        # Highest share price during the day
        high_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                              fg="light green", text=f"H: ${round(self.info_data.get('dayHigh'), 2)}")
        high_price.grid(row=1, column=2)

        # Lowest share price sold during the day
        low_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                             fg="light green", text=f"L: ${round(self.info_data.get('dayLow'), 2)}")
        low_price.grid(row=2, column=2)

        # Sector information
        sector = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                          bg="black", fg="orange", text=f"{'Sector'}")
        sector.grid(sticky="w", row=1, column=3)
        sector_value = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                                bg="black", fg="white", text=self.info_data.get('sector'))
        sector_value.grid(sticky="w", row=1, column=4)

        # Industry information
        classification = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                                  bg="black", fg="orange", text=f"{'Classification'}")
        classification.grid(sticky="w", row=2, column=3)
        industry = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                            bg="black", fg="white", text=f"{self.info_data.get('industry')}")
        industry.grid(sticky="w", row=2, column=4)

        # Type of asset
        quote_type = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                              bg="black", fg="orange", text="Quote Type")
        quote_type.grid(sticky="w", row=1, column=5)
        quote_type_value = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                                    bg="black", fg="white", text=self.info_data.get('quoteType'))
        quote_type_value.grid(sticky="w", row=1, column=6)

        # Exchange where the security is being traded
        exchg = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                         bg="black", fg="orange", text="Exchange")
        exchg.grid(sticky="w", row=2, column=5)
        exchg_value = tk.Label(security_frame, anchor="w", font="Helvetica 10", padx='2',
                               bg="black", fg="white", text=self.info_data.get('exchange'))
        exchg_value.grid(sticky="w", row=2, column=6)

    def description(self):
        """The description of the stock"""
        desc_frame = tk.LabelFrame(self.des_master, bg="black", fg="white", text="Description")
        desc_frame.grid(sticky="nsew", row=1, column=0, columnspan=3)
        desc_frame.rowconfigure(0, weight=1)
        desc_frame.rowconfigure(0, weight=1)

        desc = tk.Message(
            desc_frame,
            width=self.win_width,
            bg="black",
            fg="orange",
            text=self.info_data.get("longBusinessSummary"),
        )
        desc.grid(row=3, column=0)

    def hist_price_plot(self):
        """A graph showing price changes of the stock over time"""
        # Initializing figure that will contain plot, color outside the axes
        fig = Figure(facecolor="black", figsize=(6, 2.5), dpi=75, tight_layout=True)
        # historical market data
        history_data = self.history_data
        # Initializing subplot (area within axes)
        price_graph = fig.add_subplot(111)
        # color within the axes
        price_graph.set_facecolor('black')
        # color of the numbers
        price_graph.tick_params(colors="white")
        # color of the spines
        price_graph.spines['left'].set_color('none')
        price_graph.spines['right'].set_color('none')
        price_graph.spines['top'].set_color('none')
        price_graph.spines['bottom'].set_color('none')

        # Extracting date and converting to formatted string
        str_dates = history_data.index.strftime('%Y/%m/%d')
        # All closing prices
        close_prices = history_data['Close'].values
        # Create a linear sequence of x values based on the number of data points
        # only 5 x values are displayed, they are evenly spaced apart on the x-axis
        x_values = np.linspace(0, len(str_dates) - 1, 5, dtype=int)

        # Set the x-axis tick labels to be the original dates
        price_graph.plot(close_prices, color="teal")

        # display a small fraction
        price_graph.set_xticks(x_values, str_dates[x_values], rotation=0)

        # Initializing the tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=self.des_master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky="nw")

    def news(self):
        """The most recent news on the stock"""
        news_frame = tk.LabelFrame(self.des_master, bg="black", fg="white", text="News")
        news_frame.grid(sticky="nsew", row=2, column=2)
        news_frame.rowconfigure(0, weight=1)
        news_frame.columnconfigure(0, weight=1)

        # limit to 9 news articles if news_data has more than 9 articles else use all news_data articles
        self.stop = 8 if len(self.news_data) >= 8 else len(self.news_data)
        for news_index in range(1, self.stop):
            title = self.news_data[news_index].get('title')
            # if the title has 47 characters or more, then limit it to the first 46 and add a text elipsis
            recent_news_title = f"{title[:47]}..." if len(title) >= 47 else title
            news_link = self.news_data[news_index].get('link')
            news_widget = tk.Label(news_frame, bg='black', fg="white", anchor="w",
                                   text=recent_news_title, cursor="hand2")
            news_widget.grid(sticky='nsew', row=news_index, column=0)

            # Lambda functions to pass news_link as an argument, so that the correct link widget is used with the
            # current iteration of the for loop
            open_link = lambda event, news_link=news_link, news_widget=news_widget: \
                handle_open_link(event, news_link, news_widget)
            on_enter = lambda event, news_link=news_link, news_widget=news_widget: \
                handle_on_enter(event, news_link, news_widget)
            on_leave = lambda event, news_link=news_link, news_widget=news_widget: \
                handle_on_leave(event, news_link, news_widget)

            news_widget.bind('<Button-1>', open_link)
            news_widget.bind('<Enter>', on_enter)
            news_widget.bind('<Leave>', on_leave)

            # date of publication
            publication_date = self.news_data[news_index].get('providerPublishTime')
            formatted_date = date_conversion(publication_date, 'date')
            # if the date of publication is on the same day show the time
            if str(datetime.now().date()) == str(formatted_date):
                formatted_date = date_conversion(publication_date, 'time')
                date = tk.Label(news_frame, bg="black", fg="orange", anchor="e", text=formatted_date)
                date.grid(sticky='ne', row=news_index, column=1)
            # if the date of publication is on a different day show the date
            else:
                formatted_date = date_conversion(publication_date, 'date')
                date = tk.Label(news_frame, bg="black", fg="orange", anchor="e", text=formatted_date)
                date.grid(sticky='ne', row=news_index, column=1)

    def price_metrics(self):
        """A measure on how price relates to other metrics like time or earnings"""
        price_frame = tk.LabelFrame(self.des_master, bg="black", fg="white", text="Price Metrics")
        price_frame.grid(sticky="nsew", row=3, column=0)
        price_frame.rowconfigure(0, weight=1)
        price_frame.columnconfigure(0, weight=1)

        # Previous close - close
        px_chg = tk.Label(price_frame, anchor="w", bg="black", fg="orange",
                          text=f"Px/Chg {'1D'} ({self.info_data.get('currency')})")
        px_chg.grid(sticky="w", row=0, column=0)
        # Calculations
        new_price = self.info_data.get('currentPrice')
        old_price = self.info_data.get('previousClose')
        price_change = round(new_price - old_price, 2)
        percent_chg = round((new_price - old_price) / old_price * 100, 2)
        # if positive change
        if price_change > 0 or percent_chg > 0:
            px_chg_value = tk.Label(price_frame, anchor="e", bg="black", fg="green",
                                    text=f"+{price_change} | +{percent_chg}%")
            px_chg_value.grid(sticky="e", row=0, column=1)
        # else if negative change
        elif price_change < 0 or percent_chg < 0:
            px_chg_value = tk.Label(price_frame, anchor="e", bg="black", fg="red",
                                    text=f"{price_change} | {percent_chg}%")
            px_chg_value.grid(sticky="e", row=0, column=1)
        # unchanged price
        else:
            px_chg_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                    text=f"{price_change} | {percent_chg}%")
            px_chg_value.grid(sticky="e", row=0, column=1)

        # 52-week high date
        year_high = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"52 Wk H")
        year_high.grid(sticky="w", row=1, column=0)
        year_high_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                   text=self.info_data.get('fiftyTwoWeekHigh'))
        year_high_value.grid(sticky="e", row=1, column=1)

        # 52-week low date
        year_low = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"52 Wk L")
        year_low.grid(sticky="w", row=2, column=0)
        year_low_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                  text=self.info_data.get('fiftyTwoWeekLow'))
        year_low_value.grid(sticky="e", row=2, column=1)

        # 52 Week change % change
        year_px_chg = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"52 Wk Chg/%")
        year_px_chg.grid(sticky="w", row=3, column=0)
        year_px_chg_percent = round(self.info_data.get('52WeekChange') * 100, 2)
        # Price Change = New price - Old price
        year_px_chg_value = round(new_price - (new_price / (1 + year_px_chg_percent / 100)), 1)
        # if 52 week stock price change is positive
        if year_px_chg_percent > 0 or year_px_chg_value > 0:
            year_px_chg = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                   text=f"+{year_px_chg_value} | +{year_px_chg_percent}%")
            year_px_chg.grid(sticky="e", row=3, column=1)
        # if 52 week stock price change is 0 or negative
        else:
            year_px_chg = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                   text=f"{year_px_chg_value} | {year_px_chg_percent}%")
            year_px_chg.grid(sticky="e", row=3, column=1)

        separator = ttk.Separator(price_frame, orient="horizontal")
        separator.grid(sticky="ew", row=4, column=0, padx="2", pady="5", columnspan=2)

        # Market cap
        mkt_cap = tk.Label(price_frame, anchor="w", bg="black", fg="orange",
                           text=f"Mkt Cap ({self.info_data.get('currency')})")
        mkt_cap.grid(sticky="w", row=5, column=0)
        mkt_cap_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                 text=f"{round(self.info_data.get('marketCap')/1000000, 0)} M")
        mkt_cap_value.grid(sticky="e", row=5, column=1)

        # Shares outstanding and float shares
        shrs_out_float = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Shrs Out/Float")
        shrs_out_float.grid(sticky="w", row=6, column=0)
        shrs_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                              text=f"{round(self.info_data.get('sharesOutstanding')/1000000, 0)} | {round(self.info_data.get('floatShares')/1000000, 0)} M")
        shrs_value.grid(sticky="e", row=6, column=1)

        # total cash
        cash = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Total Cash")
        cash.grid(sticky="w", row=7, column=0)
        cash_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                              text=f"{round(self.info_data.get('totalCash')/1000000, 0)} M")
        cash_value.grid(sticky="e", row=7, column=1)

        # total debt
        debt = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Total Debt")
        debt.grid(sticky="w", row=8, column=0)
        debt_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                              text=f"{round(self.info_data.get('totalDebt')/1000000, 0)} M")
        debt_value.grid(sticky="e", row=8, column=1)

    def earnings_dividends(self):
        """The companies earnings compared to other metrics as well as dividends"""
        earnings_frame = tk.LabelFrame(self.des_master, bg="black", fg="white", text="Earnings & Dividends")
        earnings_frame.grid(sticky="nsew", row=3, column=1)
        earnings_frame.rowconfigure(0, weight=1)
        earnings_frame.columnconfigure(0, weight=1)

        # Trailing 12 month eps
        t12_eps = tk.Label(earnings_frame, bg="black", fg="orange", text=f"T12M EPS ({self.info_data.get('currency')})")
        t12_eps.grid(sticky="w", row=0, column=0)
        t12_eps_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info_data.get('trailingEps'))
        t12_eps_value.grid(sticky="e", row=0, column=1)

        # Estimated future eps
        projected_eps = tk.Label(earnings_frame, bg="black", fg="orange", text=f"Est Projected EPS")
        projected_eps.grid(sticky="w", row=1, column=0)
        projected_eps_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info_data.get('forwardEps'))
        projected_eps_value.grid(sticky="e", row=1, column=1)

        # earnings before interest tax depreciation amortization
        ebitda = tk.Label(earnings_frame, bg="black", fg="orange", text='EBITDA')
        ebitda.grid(sticky="w", row=2, column=0)
        ebitda_value = tk.Label(earnings_frame, bg="black", fg="white",
                                text=f"{round(self.info_data.get('ebitda')/1000000, 0)} M")
        ebitda_value.grid(sticky="e", row=2, column=1)

        # Trailing 12 month p/e ratio
        t12_pe = tk.Label(earnings_frame, bg="black", fg="orange", text="T12M P/E")
        t12_pe.grid(sticky="w", row=3, column=0)
        t12_pe_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info_data.get('trailingPE'))
        t12_pe_value.grid(sticky="e", row=3, column=1)

        # Estimated future p/e ratio
        forecasted_eps = tk.Label(earnings_frame, bg="black", fg="orange", text="Forward P/E")
        forecasted_eps.grid(sticky="w", row=4, column=0)
        forecasted_eps_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info_data.get('forwardPE'))
        forecasted_eps_value.grid(sticky="e", row=4, column=1)

        separator = ttk.Separator(earnings_frame, orient="horizontal")
        separator.grid(row=5, column=0, sticky="we", columnspan=2, padx=2, pady=5)

        # Dividend Rate = dividend dollar amount per share
        dividend_rate = tk.Label(earnings_frame, bg="black", fg="orange", text=f"Dividend Rate")
        dividend_rate.grid(sticky="w", row=6, column=0)
        dividend_rate_value = self.info_data.get('dividendRate')
        if not dividend_rate_value:
            dividend_rate_value = tk.Label(earnings_frame, bg="black", fg="white", text="N/A")
            dividend_rate_value.grid(sticky="e", row=6, column=1)
        else:
            dividend_rate_value = tk.Label(earnings_frame, bg="black", fg="white", text=dividend_rate_value)
            dividend_rate_value.grid(sticky="e", row=6, column=1)

        # Dividend Yield = Annual dividends per share / price per share
        dividend_yield = tk.Label(earnings_frame, bg="black", fg="orange", text="Dividend Yield% (A)")
        dividend_yield.grid(sticky="w", row=7, column=0)
        dividend_yield_value = self.info_data.get('dividendYield')
        if dividend_yield_value:
            dividend_yield_value = tk.Label(earnings_frame, bg="black", fg="white",
                                            text=f"{round(dividend_yield_value*100, 3)}%")
            dividend_yield_value.grid(sticky="e", row=7, column=1)
        else:
            dividend_yield_value = tk.Label(earnings_frame, bg="black", fg="white",
                                            text="N/A")
            dividend_yield_value.grid(sticky="e", row=7, column=1)

        # ex Dividend Date = date that dividends are paid out to shareholders
        ex_dividend_date = tk.Label(earnings_frame, bg="black", fg="orange", text="ex Dividend Date")
        ex_dividend_date.grid(sticky="w", row=8, column=0)
        ex_dividend_date_value = self.info_data.get('exDividendDate')
        if not ex_dividend_date_value:
            ex_dividend_date_value = tk.Label(earnings_frame, bg="black", fg="white", text="N/A")
            ex_dividend_date_value.grid(sticky="e", row=8, column=1)
        else:
            # conversion from unix time to formatted date
            formatted_date = date_conversion(ex_dividend_date_value, 'date')
            ex_dividend_date_value = tk.Label(earnings_frame, bg="black", fg="white", text=formatted_date)
            ex_dividend_date_value.grid(sticky="e", row=8, column=1)

    def corporate_info(self):
        """Information on the corporation and management"""
        corporate_frame = tk.LabelFrame(self.des_master, bg="black", fg="white", text="Corporate Info")
        corporate_frame.grid(sticky="nsew", row=3, column=2)
        corporate_frame.rowconfigure(0, weight=1)
        corporate_frame.columnconfigure(0, weight=1)

        # Corporate Website
        website = tk.Label(corporate_frame, bg="black", fg="orange", text="Website")
        website.grid(sticky="w", row=0, column=0)
        website_value = tk.Label(corporate_frame, anchor="e", bg="black", fg="white", text=self.info_data.get('website'))
        website_value.grid(sticky="e", row=0, column=1)

        # Location of the Headquarters
        website = tk.Label(corporate_frame, bg="black", fg="orange", text="Location")
        website.grid(sticky="w", row=1, column=0)
        website_value = tk.Label(corporate_frame, bg="black", fg="white",
                                 text=f"{self.info_data.get('city')}, "
                                      f"{self.info_data.get('state')}, "
                                      f"{self.info_data.get('country')}")
        website_value.grid(sticky="e", row=1, column=1)

        # Number of employees
        empls = tk.Label(corporate_frame, bg="black", fg="orange", text=f"Employees")
        empls.grid(sticky="w", row=2, column=0)
        empls_value = tk.Label(corporate_frame, bg="black", fg="white",
                               text=self.info_data.get('fullTimeEmployees'))
        empls_value.grid(sticky="e", row=2, column=1)

        # Chief Executive Officer
        ceo = tk.Label(corporate_frame, bg="black", fg="orange",
                       text=self.info_data.get('companyOfficers')[0]['title'])
        ceo.grid(sticky="w", row=3, column=0)
        ceo_value = tk.Label(corporate_frame, bg="black", fg="white",
                             text=self.info_data.get('companyOfficers')[0]['name'])
        ceo_value.grid(sticky="e", row=3, column=1)

        # Key executive 2
        exec_2 = tk.Label(corporate_frame, bg="black", fg="orange",
                          text=self.info_data.get('companyOfficers')[1]['title'])
        exec_2.grid(sticky="w", row=4, column=0)
        exec_2 = tk.Label(corporate_frame, bg="black", fg="white",
                          text=self.info_data.get('companyOfficers')[1]['name'])
        exec_2.grid(sticky="e", row=4, column=1)

        # Key executive 3
        exec_3 = tk.Label(corporate_frame, bg="black", fg="orange",
                          text=self.info_data.get('companyOfficers')[2]['title'])
        exec_3.grid(sticky="w", row=5, column=0)
        exec_3 = tk.Label(corporate_frame, bg="black", fg="white",
                          text=self.info_data.get('companyOfficers')[2]['name'])
        exec_3.grid(sticky="e", row=5, column=1)

        separator = ttk.Separator(corporate_frame, orient="horizontal")
        separator.grid(row=6, column=0, sticky="we", columnspan=2, padx=2, pady=5)

        # Estimated p/e to growth ratio
        peg = tk.Label(corporate_frame, bg="black", fg="orange", text='Est PEG Ratio')
        peg.grid(sticky="w", row=7, column=0)
        peg_value = tk.Label(corporate_frame, bg="black", fg="white",
                             text=self.info_data.get('pegRatio'))
        peg_value.grid(sticky="e", row=7, column=1)

        # Measure of stock volatility
        beta_ukx = tk.Label(corporate_frame, bg="black", fg="orange", text=f"Beta")
        beta_ukx.grid(sticky="w", row=8, column=0)
        beta_ukx_value = tk.Label(corporate_frame, bg="black", fg="white",
                                  text=self.info_data.get('beta'))
        beta_ukx_value.grid(sticky="e", row=8, column=1)
