import tkinter as tk
from tkinter import ttk
from datetime import datetime


class Des:
    def __init__(self, active_frame, info, win_width, win_height):
        """
        :param active_frame: Master widget containing all the currently active slave widgets
        :param win_width: The window's width
        :param win_height: The window's height
        """
        self.page_frame = active_frame
        self.info = info
        self.win_width = win_width
        self.win_height = win_height
        # Master widget for all widgets in the third row
        self.third_row_master = tk.Frame(self.page_frame, bg="black", width=self.win_width)
        self.third_row_master.grid(sticky="nw", row=3, column=0, columnspan=3)

    def main(self):
        self.security()
        self.description()
        self.price_metrics()
        self.earnings_dividends()
        self.corporate_info()

    def security(self):
        """Key details about the security such as the price per share and the volume traded"""
        security_frame = tk.LabelFrame(self.page_frame, width=self.win_width,
                                       bg="black", fg="white", text="Security")
        security_frame.grid(columnspan=5, sticky="w", row=1, column=0)

        stock_name = tk.Label(security_frame, bg="black", fg="deep sky blue",
                              font="Helvetica 12 bold", text=self.info.get('longName'))
        stock_name.grid(row=1, column=0, sticky="w")

        ticker_volume_frame = tk.Frame(security_frame, bg="black")
        ticker_volume_frame.grid(row=2, column=0, stick="nw")
        ticker = tk.Label(ticker_volume_frame, bg="black", fg="orange", text=f"{self.info.get('symbol')}")
        ticker.grid(row=0, column=0, sticky="w")

        volume = tk.Label(ticker_volume_frame, bg="black", fg="white", text=f"VOL {self.info.get('volume')}")
        volume.grid(row=0, column=3, sticky="e")

        # Closing price of the day
        close_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                               fg="light green", text=f"C: ${self.info.get('currentPrice')}")
        close_price.grid(row=1, column=1)

        # Opening price of the day
        open_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                              fg="light green", text=f"O: ${self.info.get('open')}")
        open_price.grid(row=2, column=1)

        # Highest share price during the day
        high_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                              fg="light green", text=f"H: ${self.info.get('dayHigh')}")
        high_price.grid(row=1, column=2)

        # Lowest share price sold during the day
        low_price = tk.Label(security_frame, font="Helvetica 10", padx='10', bg="black",
                             fg="light green", text=f"L: ${self.info.get('dayLow')}")
        low_price.grid(row=2, column=2)

        # Sector information
        sector = tk.Label(security_frame, anchor="w", font="Helvetica 11", padx='2',
                         bg="black", fg="orange", text=f"{'Sector'}")
        sector.grid(sticky="w", row=1, column=3)
        sector_value = tk.Label(security_frame, anchor="w", font="Helvetica 11", padx='2',
                               bg="black", fg="white", text=self.info.get('sector'))
        sector_value.grid(sticky="w", row=1, column=4)

        # Industry information
        classification = tk.Label(security_frame, anchor="e", font="Helvetica 11", padx='2',
                                  bg="black", fg="orange", text=f"{'Classification'}")
        classification.grid(sticky="e", row=2, column=3)
        industry = tk.Label(security_frame, anchor="e", font="Helvetica 11", padx='2',
                            bg="black", fg="white", text=f"{self.info.get('industry')}")
        industry.grid(sticky="e", row=2, column=4)

        # Type of asset
        quote_type = tk.Label(security_frame, anchor="w", font="Helvetica 11", padx='2',
                         bg="black", fg="orange", text="Quote Type")
        quote_type.grid(sticky="w", row=1, column=5)
        quote_type_value = tk.Label(security_frame, anchor="w", font="Helvetica 11", padx='2',
                               bg="black", fg="white", text=self.info.get('quoteType'))
        quote_type_value.grid(sticky="w", row=1, column=6)

        # Exchange where the security is being traded
        exchg = tk.Label(security_frame, anchor="w", font="Helvetica 11", padx='2',
                         bg="black", fg="orange", text="Exchange")
        exchg.grid(sticky="w", row=2, column=5)
        exchg_value = tk.Label(security_frame, anchor="w", font="Helvetica 11", padx='2',
                               bg="black", fg="white", text=self.info.get('exchange'))
        exchg_value.grid(sticky="w", row=2, column=6)

    def description(self):
        """The description of the stock"""
        desc_frame = tk.LabelFrame(self.page_frame, bg="black", fg="white", text="Description")
        desc_frame.grid(sticky="w", row=2, column=0)
        desc = tk.Message(
            desc_frame,
            anchor="w",
            width=self.win_width - 20,
            bg="black",
            fg="orange",
            text=self.info.get("longBusinessSummary"),
        )
        desc.grid(row=3, column=0)

    def price_metrics(self):
        """A measure on how price relates to other metrics like time or earnings"""
        price_frame = tk.LabelFrame(self.third_row_master, bg="black", fg="white", text="Price Metrics")
        price_frame.grid(sticky="nw", row=3, column=0)

        # Price change since last update
        px_chg = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Px/Chg {'1D'} ({self.info.get('currency')})")
        px_chg.grid(sticky="w", row=0, column=0)
        px_chg_value = tk.Label(price_frame, anchor="e", bg="black", fg="white", text=f"{1403.5} | {'+0.11'}%")
        px_chg_value.grid(sticky="e", row=0, column=1)

        # 52-week high date
        year_high = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"52 Wk H")
        year_high.grid(sticky="w", row=1, column=0)
        year_high_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                                   text=self.info.get('fiftyTwoWeekHigh'))
        year_high_value.grid(sticky="e", row=1, column=1)

        # 52-week low date
        year_low = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"52 Wk L")
        year_low.grid(sticky="w", row=2, column=0)
        year_low_value = tk.Label(price_frame, anchor="e", bg="black", fg="white", text=self.info.get('fiftyTwoWeekLow'))
        year_low_value.grid(sticky="e", row=2, column=1)

        # Year to date % change
        ytd_chg = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"YTD Chg/%")
        ytd_chg.grid(sticky="w", row=3, column=0)
        ytd_chg_value = tk.Label(price_frame, anchor="e", bg="black", fg="white", text=f"{'-61.814'} | {'-4.9'}%")
        ytd_chg_value.grid(sticky="e", row=3, column=1)

        separator = ttk.Separator(price_frame, orient="horizontal")
        separator.grid(sticky="ew", row=4, column=0, padx="2", pady="5", columnspan=2)

        # Market cap
        mkt_cap = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Mkt Cap ({self.info.get('currency')})")
        mkt_cap.grid(sticky="w", row=5, column=0)
        mkt_cap_value = tk.Label(price_frame, anchor="e", bg="black", fg="white", text=f"{round(self.info.get('marketCap')/1000000, 0)} M")
        mkt_cap_value.grid(sticky="e", row=5, column=1)

        # Shares outstanding and float shares
        shrs_out_float = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Shrs Out/Float")
        shrs_out_float.grid(sticky="w", row=6, column=0)
        shrs_value = tk.Label(price_frame, anchor="e", bg="black", fg="white",
                              text=f"{round(self.info.get('sharesOutstanding')/1000000, 0)} | {round(self.info.get('floatShares')/1000000, 0)} M")
        shrs_value.grid(sticky="e", row=6, column=1)

        # total cash
        cash = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Cashflow")
        cash.grid(sticky="w", row=7, column=0)
        cash_value= tk.Label(price_frame, anchor="e", bg="black", fg="white", text=f"{round(self.info.get('totalCash')/1000000, 0)} M")
        cash_value.grid(sticky="e", row=7, column=1)

        # total debt
        debt = tk.Label(price_frame, anchor="w", bg="black", fg="orange", text=f"Debt")
        debt.grid(sticky="w", row=8, column=0)
        debt_value = tk.Label(price_frame, anchor="e", bg="black", fg="white", text=f"{round(self.info.get('totalDebt')/1000000, 0)} M")
        debt_value.grid(sticky="e", row=8, column=1)

    def earnings_dividends(self):
        """The companies earnings compared to other metrics as well as dividends"""
        earnings_frame = tk.LabelFrame(self.third_row_master, bg="black", fg="white", text="Earnings & Dividends")
        earnings_frame.grid(sticky="n", row=3, column=1)

        # Trailing 12 month eps
        t12_eps = tk.Label(earnings_frame, bg="black", fg="orange", text=f"T12M EPS ({self.info.get('currency')})")
        t12_eps.grid(sticky="w", row=0, column=0)
        t12_eps_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info.get('trailingEps'))
        t12_eps_value.grid(sticky="e", row=0, column=1)

        # Estimated future eps
        projected_eps= tk.Label(earnings_frame, bg="black", fg="orange", text=f"Est Projected EPS")
        projected_eps.grid(sticky="w", row=1, column=0)
        projected_eps_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info.get('forwardEps'))
        projected_eps_value.grid(sticky="e", row=1, column=1)

        # earnings before interest tax depreciation amortization
        ebitda= tk.Label(earnings_frame, bg="black", fg="orange", text='EBITDA')
        ebitda.grid(sticky="w", row=2, column=0)
        ebitda_value = tk.Label(earnings_frame, bg="black", fg="white", text=f"{round(self.info.get('ebitda')/1000000, 0)} M")
        ebitda_value.grid(sticky="e", row=2, column=1)

        # Trailing 12 month p/e ratio
        t12_pe = tk.Label(earnings_frame, bg="black", fg="orange", text="T12M P/E" )
        t12_pe.grid(sticky="w", row=3, column=0)
        t12_pe_value = tk.Label(earnings_frame, bg="black", fg="white", text=self.info.get('trailingPE'))
        t12_pe_value.grid(sticky="e", row=3, column=1)

        # Estimated future p/e ratio
        forecasted_eps = tk.Label(earnings_frame, bg="black", fg="orange", text="Forward P/E")
        forecasted_eps.grid(sticky="w", row=4, column=0)
        forecasted_eps_value= tk.Label(earnings_frame, bg="black", fg="white", text=self.info.get('forwardPE'))
        forecasted_eps_value.grid(sticky="e", row=4, column=1)

        separator = ttk.Separator(earnings_frame, orient="horizontal")
        separator.grid(row=5, column=0, sticky="we", columnspan=2, padx=2, pady=5)

        # Dividend Rate = dividend dollar amount per share
        dividend_rate = tk.Label(earnings_frame, bg="black", fg="orange", text=f"Dividend Rate")
        dividend_rate.grid(sticky="w", row=6, column=0)
        dividend_rate_value = self.info.get('dividendRate')
        if not dividend_rate_value:
            dividend_rate_value = tk.Label(earnings_frame, bg="black", fg="white", text="N/A")
            dividend_rate_value.grid(sticky="e", row=6, column=1)
        else:
            dividend_rate_value = tk.Label(earnings_frame, bg="black", fg="white", text=dividend_rate_value)
            dividend_rate_value.grid(sticky="e", row=6, column=1)

        # Dividend Yield = Annual dividends per share / price per share
        dividend_yield = tk.Label(earnings_frame, bg="black", fg="orange", text="Dividend Yield% (A)")
        dividend_yield.grid(sticky="w", row=7, column=0)
        dividend_yield_value = self.info.get('dividendYield')
        if dividend_yield_value:
            dividend_yield_value = tk.Label(earnings_frame, bg="black", fg="white",
                                            text=f"{round(dividend_yield_value*100, 3)}%")
            dividend_yield_value.grid(sticky="e", row=7, column=1)
        else:
            dividend_yield_value = tk.Label(earnings_frame, bg="black", fg="white",
                                            text="N/A")
            dividend_yield_value.grid(sticky="e", row=7, column=1)

        # ex Dividend Date = date that dividends are paid out to shareholders
        exDividendDate = tk.Label(earnings_frame, bg="black", fg="orange", text="ex Dividend Date")
        exDividendDate.grid(sticky="w", row=8, column=0)
        exDividendDate_value = self.info.get('exDividendDate')
        if not exDividendDate_value:
            exDividendDate_value = tk.Label(earnings_frame, bg="black", fg="white", text="N/A")
            exDividendDate_value.grid(sticky="e", row=8, column=1)
        else:
            date_time = datetime.fromtimestamp(exDividendDate_value)
            formatted_date = date_time.strftime("%Y/%m/%d")
            exDividendDate_value = tk.Label(earnings_frame, bg="black", fg="white", text=formatted_date)
            exDividendDate_value.grid(sticky="e", row=8, column=1)


    def corporate_info(self):
        """Information on the corporation and management"""
        corporate_frame = tk.LabelFrame(self.third_row_master, bg="black", fg="white", text="Corporate Info")
        corporate_frame.grid(sticky="ne", row=3, column=2)

        # Corporate Website
        website = tk.Label(corporate_frame, bg="black", fg="orange", text="Website")
        website.grid(sticky="w", row=0, column=0)
        website_value = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('website'))
        website_value.grid(sticky="e", row=0, column=1)

        # Location of the Headquarters
        website = tk.Label(corporate_frame, bg="black", fg="orange", text="Location")
        website.grid(sticky="w", row=1, column=0)
        website_value = tk.Label(corporate_frame, bg="black", fg="white",
                                 text=f"{self.info.get('city')}, {self.info.get('state')}, {self.info.get('country')}")
        website_value.grid(sticky="e", row=1, column=1)

        # Number of employees
        empls = tk.Label(corporate_frame, bg="black", fg="orange", text=f"Employees")
        empls.grid(sticky="w", row=2, column=0)
        empls_value = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('fullTimeEmployees'))
        empls_value.grid(sticky="e", row=2, column=1)

        # Chief Executive Officer
        ceo = tk.Label(corporate_frame, bg="black", fg="orange", text=self.info.get('companyOfficers')[0]['title'])
        ceo.grid(sticky="w", row=3, column=0)
        ceo_value = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('companyOfficers')[0]['name'])
        ceo_value.grid(sticky="e", row=3, column=1)

        # Key executive 2
        exec_2 = tk.Label(corporate_frame, bg="black", fg="orange", text=self.info.get('companyOfficers')[1]['title'])
        exec_2.grid(sticky="w", row=4, column=0)
        exec_2 = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('companyOfficers')[1]['name'])
        exec_2.grid(sticky="e", row=4, column=1)

        # Key executive 3
        exec_3 = tk.Label(corporate_frame, bg="black", fg="orange", text=self.info.get('companyOfficers')[2]['title'])
        exec_3.grid(sticky="w", row=5, column=0)
        exec_3 = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('companyOfficers')[2]['name'])
        exec_3.grid(sticky="e", row=5, column=1)

        separator = ttk.Separator(corporate_frame, orient="horizontal")
        separator.grid(row=6, column=0, sticky="we", columnspan=2, padx=2, pady=5)

        # Estimated p/e to growth ratio
        peg = tk.Label(corporate_frame, bg="black", fg="orange", text='Est PEG Ratio')
        peg.grid(sticky="w", row=7, column=0)
        peg_value = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('pegRatio'))
        peg_value.grid(sticky="e", row=7, column=1)

        # Measure of stock volatility
        beta_ukx = tk.Label(corporate_frame, bg="black", fg="orange", text=f"Beta")
        beta_ukx.grid(sticky="w", row=8, column=0)
        beta_ukx_value = tk.Label(corporate_frame, bg="black", fg="white", text=self.info.get('beta'))
        beta_ukx_value.grid(sticky="e", row=8, column=1)
