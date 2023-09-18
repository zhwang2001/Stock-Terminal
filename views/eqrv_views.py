import requests
import pandas as pd
from models.eqrv_model import EqrvModel
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from controllers.eqrv_controller import EqrvController
from utilities.utils import date_conversion


class Eqrv:
    """
    Assess whether stock is cheap compared to its peer group and index
    """
    def __init__(self, active_frame, info_data, historical_earnings, win_width, win_height):
        """
        :param active_frame: Master widget containing all the currently active slave widgets
        :param info: info on the security
        :param historical_earnings: All annual and quarterly earnings data
        :param win_width: the window's width
        :param win_height: the window's height
        """
        self.active_frame = active_frame
        self.info_data = info_data
        self.historical_earnings = historical_earnings
        self.win_width = win_width
        self.win_height = win_height
        # list of competitor tickers
        self.stock_list = None
        # list[dict] of competitor info
        self.stock_info = None
        # The stock's ticker symbol
        self.symbol = None
        # alpha vantage variable for storing eps history depth
        self.hist_range = 1
        # Master widget for all widgets in the eqrv function
        self.eqrv_master = tk.Frame(self.active_frame, bg="black")
        self.eqrv_master.grid(row=1, column=0, sticky="nsew")
        self.eqrv_master.rowconfigure(0, weight=1)
        self.eqrv_master.columnconfigure(0, weight=1)

    def main(self):
        self.current_vs_historical()
        self.summary_multiples()

    def current_vs_historical(self):
        """A table Compares current and historical metrics of selected stock and competitors"""

        cvh_frame = tk.LabelFrame(self.eqrv_master, bg="black", fg="white", labelanchor="n",
                                  text=f"Current vs {self.hist_range}yr Average Historical Premium")
        cvh_frame.grid(row=1, column=0, sticky="w")

        tab_system = ttk.Notebook(self.eqrv_master)
        tabs = ['Comps', 'Market', "Self"]
        for tab_name in tabs:
            tab = tk.Frame(tab_system, bg="black", relief="raised")
            tab_system.add(tab, text=tab_name)
        tab_system.grid(row=0, column=0, columnspan=2,
                        sticky="sw")

        separator_styles = ttk.Style()
        separator_styles.configure('Line.TSeparator', background='black')
        # initialize line dividers
        for column in range(1, 10, 2):
            separator = ttk.Separator(cvh_frame, orient="vertical", style='Line.TSeparator')
            separator.grid(sticky="ns", row=0, column=column, padx=5, rowspan=2)

        separator = ttk.Separator(cvh_frame, orient="horizontal", style='Line.TSeparator')
        separator.grid(sticky="ew", row=2, column=0, columnspan=12)

        def column():
            # Earnings metrics
            metric = tk.Label(cvh_frame, bg="black", fg="white", text="Metric")
            metric.grid(sticky="w", row=1, column=0)

            # current stock to comp price premium
            # how much more expensive is the stock compared to group mean right now
            # ex. current = (current BFpe - group mean BFpe) / group mean BFpe
            current = tk.Label(cvh_frame, bg="black", fg="white", text="Current Prem %")
            current.grid(sticky="e", row=1, column=2)

            # historical n year average, stock to comp price premium
            # how much more expensive was the stock compared to group mean throughout history
            # ex. hist_avg = y1 + y2 / 2
                # y1 = (current pe - group mean pe) / group mean pe
                # y2 = (current pe - group mean pe) / group mean pe
            #pe = Market cap / earnings = stock price / eps
            hist_avg = tk.Label(cvh_frame, bg="black", fg="white", text="Hist Avg Prem %")
            hist_avg.grid(sticky="e", row=1, column=4)

            # differences between premiums (current - hist_avg)
            diff = tk.Label(cvh_frame, bg="black", fg="white", text="Diff")
            diff.grid(sticky="e", row=1, column=6)

            # standard deviation
            sd = tk.Label(cvh_frame, bg="black", fg="white", text="SD")
            sd.grid(sticky="e", row=1, column=8)

            # 1 year trend of P/E
            year_trend = tk.Label(cvh_frame, bg="black", fg="white", text=f"{self.hist_range}Yr Trend")
            year_trend.grid(sticky="e", row=1, column=10)

        def row():
            # P/E ratio
            pe = tk.Label(cvh_frame, bg="black", fg="orange", text="P/E")
            pe.grid(sticky="w", row=3, column=0)

            # EV/EBITDA
            ebitda = tk.Label(cvh_frame, bg="black", fg="orange", text="EV/EBITDA")
            ebitda.grid(sticky="w", row=4, column=0)

        def values():

            forward_pe = self.info_data.get('forwardPE')
            pe_current_value = round(forward_pe, 2)
            pe_current = tk.Label(cvh_frame, bg="black", fg="deep sky blue", text=f"{pe_current_value}%")
            pe_current.grid(sticky="e", row=3, column=2)

            # P/E current percent premium
            pe_hist_avg_value = -13
            pe_hist_avg = tk.Label(cvh_frame, bg="black", fg="orange", text=f"{pe_hist_avg_value}%")
            pe_hist_avg.grid(sticky="e", row=3, column=4)

            # P/E difference between historical and current premiums
            pe_diff_value = pe_current_value - pe_hist_avg_value
            # Blended forward P/E standard deviation
            pe_sd_value = -0.9
            # if current is cheaper than historical average
            if pe_diff_value <= 0 or pe_sd_value <= 0:
                pe_diff = tk.Label(cvh_frame, bg="black", fg="green", text=f"{round(pe_diff_value, 2)}%")
                pe_diff.grid(sticky="e", row=3, column=6)
                pe_sd = tk.Label(cvh_frame, bg="black", fg="green", text=pe_sd_value)
                pe_sd.grid(sticky="e", row=3, column=8)
            # elif current is more expensive than historical average
            elif pe_diff_value > 0 or pe_sd_value <= 0:
                pe_diff = tk.Label(cvh_frame, bg="black", fg="red", text=f"{round(pe_diff_value, 2)}%")
                pe_diff.grid(sticky="e", row=3, column=6)
                pe_sd = tk.Label(cvh_frame, bg="black", fg="red", text=pe_sd_value)
                pe_sd.grid(sticky="e", row=3, column=8)

            # display a mini plot of the historical eps data
            self.hist_eps_plot(cvh_frame)

            # EV/EBITDA  current percent premium
            ebitda_current_value = -9
            ebitda_current = tk.Label(cvh_frame, bg="black", fg="deep sky blue", text=f"{ebitda_current_value}%")
            ebitda_current.grid(sticky="e", row=4, column=2)

            # EV/EBITDA historical group average percent premium
            ebitda_hist_avg_value = 1
            ebitda_hist_avg = tk.Label(cvh_frame, bg="black", fg="orange", text=f"{ebitda_hist_avg_value}%")
            ebitda_hist_avg.grid(sticky="e", row=4, column=4)

            # P/E difference between historical and current premiums
            ebitda_diff_value = ebitda_current_value - ebitda_hist_avg_value
            # EV/EBITDA standard deviation
            ebitda_sd_value = -1.2
            # if current is cheaper than historical average
            if ebitda_diff_value <= 0:
                ebitda_diff = tk.Label(cvh_frame, bg="black", fg="green", text=f"{ebitda_diff_value}%")
                ebitda_diff.grid(sticky="e", row=4, column=6)
                ebitda_sd = tk.Label(cvh_frame, bg="black", fg="green", text=ebitda_sd_value)
                ebitda_sd.grid(sticky="e", row=4, column=8)
            # elif current is more expensive than historical average
            elif ebitda_diff_value > 0:
                ebitda_diff = tk.Label(cvh_frame, bg="black", fg="red", text=f"{ebitda_diff_value}%")
                ebitda_diff.grid(sticky="e", row=4, column=6)
                ebitda_sd = tk.Label(cvh_frame, bg="black", fg="red", text=ebitda_sd_value)
                ebitda_sd.grid(sticky="e", row=4, column=8)


        column()
        row()
        values()

    def hist_eps_plot(self, master):
        """
        Subwidget of the 'current vs historical' widget
        A mini plot of the eps trends over time within the historical range
        """
        # Initializing figure that will contain plot, color outside the axes
        fig = Figure(facecolor="black", figsize=(1, 0.35), dpi=75)
        # historical eps data
        historical_earnings = self.historical_earnings
        # Initializing subplot (area within axes)
        eps_graph = fig.add_subplot(111)
        # color within the axes
        eps_graph.set_facecolor('black')
        # color of the spines
        eps_graph.spines['left'].set_color('none')
        eps_graph.spines['right'].set_color('none')
        eps_graph.spines['top'].set_color('none')
        eps_graph.spines['bottom'].set_color('none')

        # Extracting the eps values using the date key and historical range
        x_keys, y_values = [], []
        # extract historical data on a quarterly basis
        for index, date in enumerate(historical_earnings):
            if index + 1 == self.hist_range * 4 + 1:
                break
            reported_eps = historical_earnings[date][0]
            x_keys.append(date)
            y_values.append(float(reported_eps))

        # Hide X and Y axes label marks
        eps_graph.xaxis.set_tick_params(labelbottom=False)
        eps_graph.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        eps_graph.set_xticks([])
        eps_graph.set_yticks([])

        #Old to new eps
        eps_graph.plot(x_keys, y_values[::-1], color="white")

        # Initializing the tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=3, column=10, columnspan=1, sticky="nw")

    def summary_multiples(self):
        """Comparative summary of all stocks multiples"""
        summary_frame = tk.LabelFrame(self.eqrv_master, bg="black", fg="white", labelanchor='n', text='Summary of Current Multiples')
        summary_frame.grid(row=2, column=0, sticky="w")

        ec = EqrvController(self.historical_earnings, self.info_data, self.hist_range)
        # index information about the current stock and competitor stocks
        self.symbol = self.info_data.get('symbol')
        self.stock_list = [self.symbol, 'INTC', 'AAPL', 'AMD']
        self.stock_info = ec.handle_competitor_info(competitors=self.stock_list)
        self.current_stock = []

        # Column Labels
        def column_names():
            """The column names for the widget"""
            col_labels: tuple = ("Name", "Mkt Cap", 'P/E', 'EV/EBITDA', 'EV/REV','Current Ratio', 'Quick Ratio', 'PEG Ratio', 'Short Ratio')
            # Horizontal line
            separator = ttk.Separator(summary_frame, orient="horizontal", style='Line.TSeparator')
            separator.grid(sticky="ew", row=1, column=0, columnspan=20)
            for col_index, col_label in enumerate(range(0, len(col_labels) * 2, 2)):
                label = tk.Label(summary_frame, bg="black", fg="white", text=col_labels[col_index])
                # Vertical lines
                separator = ttk.Separator(summary_frame, orient="vertical", style='Line.TSeparator')
                if col_index == 0:
                    label.grid(row=0, column=col_label, sticky="w")
                    separator.grid(sticky="ns", row=0, column=col_label + 1, padx=5)
                elif col_label + 1 == len(col_labels) * 2 - 1:
                    label.grid(row=0, column=col_label, sticky="e")
                else:
                    label.grid(row=0, column=col_label, sticky="e")
                    separator.grid(sticky="ns", row=0, column=col_label + 1, padx=5)

        def stock_stats():
            """Displays all relevant metrics on the current and competitor stocks"""
            start_index = 2
            for row_index, comp in enumerate(self.stock_info, start_index):
                security_name: str = self.stock_info[comp]['long_name']
                mkt_cap: str = f"{round(self.stock_info[comp]['mkt_cap'] / 1000000000, 2)}B"
                current_pe_multiple: str = f"{round(self.stock_info[comp]['current_pe_multiple'], 1)}x"
                enterprise_ebitda: float = round(self.stock_info[comp]['enterprise/ebitda'], 1)
                enterprise_revenue: float = round(self.stock_info[comp]['enterprise/revenue'], 1)
                current_ratio: float = round(self.stock_info[comp]['currentRatio'], 1)
                quick_ratio: float = round(self.stock_info[comp]['quickRatio'], 1)
                peg_ratio: float = round(self.stock_info[comp]['pegRatio'], 1)
                short_ratio: float = round(self.stock_info[comp]['shortRatio'], 1)

                # the first index contains information on the current stock
                if row_index == start_index:
                    self.current_stock = (security_name, mkt_cap, current_pe_multiple,
                                         enterprise_ebitda, enterprise_revenue, current_ratio,
                                         quick_ratio, peg_ratio, short_ratio)


                competitor_metrics: tuple = (security_name, mkt_cap, current_pe_multiple,
                                      enterprise_ebitda, enterprise_revenue, current_ratio,
                                      quick_ratio, peg_ratio, short_ratio)

                for col_index, metric in enumerate(range(0, len(competitor_metrics) * 2, start_index)):
                    label = tk.Label(summary_frame, bg="black", fg="orange",
                                     text=competitor_metrics[col_index])
                    if comp == self.symbol:
                        label = tk.Label(summary_frame, bg="black", fg="deep sky blue",
                                         text=competitor_metrics[col_index])
                        if col_index == 0:
                            label.grid(row=row_index, column=metric, sticky="w", pady=8)
                        else:
                            label.grid(row=row_index, column=metric, sticky="e", pady=8)
                    elif col_index == 0:
                        label.grid(row=row_index, column=metric, sticky="w")
                    else:
                        label.grid(row=row_index, column=metric, sticky="e")
        # Mean stats row
        def mean_stats():
            name: str = 'Mean'
            mean_mkt_cap: str = f"{round(sum(self.stock_info.loc['mkt_cap'].values) / len(self.stock_info.loc['mkt_cap'].values) / 1000000000000, 2)}B"
            mean_current_pe_multiple: str = f"{round(sum(self.stock_info.loc['current_pe_multiple'].values) / len(self.stock_info.loc['current_pe_multiple'].values), 1)}x"
            mean_enterprise_ebitda: float = round(sum(self.stock_info.loc['enterprise/ebitda'].values) / len(self.stock_info.loc['enterprise/ebitda'].values), 1)
            mean_enterprise_revenue: float = round(sum(self.stock_info.loc['enterprise/revenue'].values) / len(self.stock_info.loc['enterprise/revenue'].values), 1)
            mean_current_ratio: float = round(sum(self.stock_info.loc['currentRatio'].values) / len(self.stock_info.loc['currentRatio'].values), 1)
            mean_quick_ratio: float = round(sum(self.stock_info.loc['quickRatio'].values) / len(self.stock_info.loc['quickRatio'].values), 1)
            mean_peg_ratio: float = round(sum(self.stock_info.loc['pegRatio'].values) / len(self.stock_info.loc['pegRatio'].values), 1)
            mean_short_ratio: float = round(sum(self.stock_info.loc['shortRatio'].values) / len(self.stock_info.loc['shortRatio'].values), 1)

            means: tuple = (name, mean_mkt_cap, mean_current_pe_multiple, mean_enterprise_ebitda,
                           mean_enterprise_revenue, mean_current_ratio, mean_quick_ratio,
                           mean_peg_ratio, mean_short_ratio)

            second_last_row = len(self.stock_list) + 4
            for col_index, metric in enumerate(range(0, len(means) * 2, 2)):
                    label = tk.Label(summary_frame, bg="black", fg="white",
                                     text=means[col_index])
                    if col_index == 0:
                        label.grid(row=second_last_row, column=metric, sticky="w")
                    else:
                        label.grid(row=second_last_row, column=metric, sticky="e")
            return means

        def premium_calculation(current_stock, means):

            premium = []
            for stock_data, mean_data in zip(current_stock[2:], means[2:]):
                if type(stock_data) is str or type(mean_data) is str:
                    stock_float, mean_float = float(stock_data.strip('x')), float(mean_data.strip('x'))
                    # remove the 'x' letter from the current_pe_multiple column, convert to float and round
                    premium.append(f"{round((mean_float - stock_float)/ mean_float * 100)}%")
                else:
                    premium.append(f"{round((mean_data - stock_data)/ mean_data * 100)}%")

            end_row = len(self.stock_list) + 5
            # title in first column
            label = tk.Label(summary_frame, bg="black", fg="deep sky blue",
                             text=f"{self.symbol} Premium")
            label.grid(row=end_row, column=0, sticky="w")
            for col_index, metric in enumerate(range(0, len(premium) * 2, 2)):
                label = tk.Label(summary_frame, bg="black", fg="deep sky blue",
                                 text=premium[col_index])
                label.grid(row=end_row, column=metric + 4, sticky="e")

            return means

        column_names()
        stock_stats()
        separator = ttk.Separator(summary_frame, orient='horizontal', style='Line.TSeparator')
        separator.grid(row=len(self.stock_list) + 3, column=0, sticky="ew", columnspan=20, pady=(10,0))
        means = mean_stats()
        premium_calculation(self.current_stock, means)









