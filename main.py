import tkinter as tk
from models.des_model import DesModel
from models.eqrv_model import EqrvModel
from views.des_views import Des
from views.eqrv_views import Eqrv
from views.eqs_views import Eqs
from views.watc_views import Watc
import datetime


class MainView:
    def __init__(self):
        """
        Initializes the Tkinter Window
        """
        # The root frame
        self.root = tk.Tk()
        self.root.title("Stock Terminal")
        self.root.config(bg="black")
        self.root.geometry("880x785")
        self.root.update_idletasks()
        self.root.columnconfigure(0, weight=1)

        # the root frame width
        self.win_width = self.root.winfo_width()
        # the root frame height
        self.win_height = self.root.winfo_height()
        # state management for storing the search bar component
        self.search_bar = None
        # state management for storing the currently active page
        self.selection = None
        # state management for storing the currently active grid slaves
        self.active_frame = None
        # state management for storing the information on the company
        self.info_data = None
        # state management for storing news about the company
        self.news_data = None
        # state management for storing past historical market data on the company
        self.history_data = None
        # state management for storing past earnings data
        self.historical_earnings = None

        # master widget for all top row widgets
        self.top_row_master = tk.Frame(self.root, bg="black")
        self.top_row_master.grid(sticky="ew", row=0, column=0)
        self.top_row_master.rowconfigure(0, weight=1)
        self.top_row_master.columnconfigure(0, weight=1)

        # master widget for all navigation widgets
        self.nav_master = tk.Frame(self.top_row_master, bg="black")
        self.nav_master.grid(sticky="nsew", row=0, column=0)

        self.main()
        # Event listener for closing the window
        self.root.protocol("WM_DELETE_WINDOW", self.handle_closing)
        self.root.mainloop()

    def main(self):
        # live clock
        # self.clock()
        # Used for changing functions
        self.function_dropdown_view()
        # Used for typing in securities
        self.search_bar_view()
        # Used for searching securities
        self.search_button_view()

    def handle_closing(self):
        """Event handler for closing the window"""
        self.root.quit()

    def clock(self):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d, %H:%M:%S")
        time = tk.Label(self.top_row_master, bg="black", fg="orange",
                        text=formatted_time, font="helvetica 12 bold")
        time.grid(row=0, column=3, sticky="ne")
        self.root.after(1000, self.clock)

    def search_bar_view(self):
        """
        Search bar widget that is permanently visible, used to search for securities
        """
        # Search bar for typing in query
        self.search_bar = tk.Entry(self.nav_master, width=45, borderwidth=5)
        self.search_bar.insert(0, "Enter a Ticker Symbol...")
        self.search_bar.grid(sticky="nw", row=0, column=0, ipadx=1, ipady=1)

    def search_button_view(self):
        """
        Search bar button widget that is permanently visible, used to submit query
        """
        # The user can choose to submit the query by pressing enter
        def handle_search(event):
            self.search_query(self.selection)

        self.search_bar.bind('<Return>', handle_search)

        # Search button also available for submitting the search query
        search_button = tk.Button(self.nav_master, overrelief="solid", text="Search",
                                  command=lambda: self.search_query(self.selection))
        search_button.grid(row=0, column=1, ipady=1, sticky="nw")

    def search_query(self, selection):
        """
        Callback function for handling search queries, fetching relevant info on the security
        depending on the function selected
        :param selection: Inherits dropdown menu item locally and globally
        """
        self.root.config(width=100)
        query = self.search_bar.get()
        # load functions from DesModel
        if selection == "DES":
            dc = DesModel(query)
            self.info_data = dc.get_info()
            self.news_data = dc.get_news()
            self.history_data = dc.get_history()
        # load functions from EqrvModel
        elif selection == "EQRV":
            ec = EqrvModel(query)
            dc = DesModel(query)
            self.historical_earnings = ec.get_earnings()
            self.info_data = dc.get_info()
        # call the function here to get the function instead of selecting an item from the dropdown menu again
        self.function_navigate(selection)

    def function_dropdown_view(self):
        """
        Dropdown menu widget used to navigate to various functions (default function is des)
        """
        # The default selected option in the dropdown selection menu
        default_function = "DES"
        placeholder = tk.StringVar()
        placeholder.set(default_function)

        # If dropdown menu item hasn't been selected yet
        if not self.selection:
            # The default function to be displayed
            self.function_navigate(default_function)

        # Dropdown menu for function navigation
        option_menu = tk.OptionMenu(self.nav_master, placeholder, "DES", "EQRV", "EQS", "WATC",
                                    command=lambda selection: (self.search_query(selection)))
        option_menu.grid(row=0, column=2, sticky='nw')

    def function_navigate(self, selection):
        """
        Callback function for the function dropdown component
        :param selection: Inherits the dropdown menu item locally or globally
        """
        # Make self.selection accessible globally
        self.selection = selection
        # For initialization: if there is an active frame already then unmount it
        if self.active_frame:
            self.active_frame.destroy()

        # no active frame? then assign one
        self.active_frame = tk.Frame(self.root, bg="black")
        self.active_frame.grid(row=1, column=0, sticky='nsew')
        # All Available function views
        if self.info_data:
            des = Des(self.active_frame, self.info_data, self.history_data, self.news_data, self.win_width, self.win_height)
            eqrv = Eqrv(self.active_frame, self.info_data, self.historical_earnings, self.win_width, self.win_height)
            eqs = Eqs(self.active_frame, self.info_data, self.win_width, self.win_height)
            watc = Watc(self.active_frame, self.info_data, self.win_width, self.win_height)

            functions = {"DES": des, "EQRV": eqrv, "EQS": eqs, "WATC": watc}
            function = functions[self.selection]
            return function.main()

        elif not self.info_data:
            # TODO default state terminal
            return


if __name__ == "__main__":
    # pricing metrics as name for widget instead of price charts
    view = MainView()
