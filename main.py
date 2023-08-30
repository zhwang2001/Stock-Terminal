import tkinter as tk
from controller.des_controller import DesController
from views.des_views import Des
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
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # the root frame width
        self.win_width = self.root.winfo_width()
        # the root frame height
        self.win_height = self.root.winfo_height()
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

        #master widget for all top row widgets
        self.top_row_master = tk.Frame(self.root, bg="black")
        self.top_row_master.grid(sticky="ew", row=0, column=0)
        self.top_row_master.rowconfigure(0, weight=1)
        self.top_row_master.columnconfigure(0, weight=1)

        #master widget for all navigation widgets
        self.nav_master = tk.Frame(self.top_row_master, bg="black")
        self.nav_master.grid(sticky="nsew", row=0, column=0)

        # Used for searching up securities
        self.search_bar()
        # Used for changing functions
        self.function_dropdown()
        # live clock
        self.clock()

        self.root.mainloop()

    def clock(self):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d, %H:%M:%S")
        time = tk.Label(self.top_row_master, bg="black", fg="orange",
                        text=formatted_time, font="helvetica 12 bold")
        time.grid(row=0, column=3, sticky="ne")
        self.root.after(1000, self.clock)

    def search_bar(self):
        """
        Search bar widget that is permanently visible, used to search for securities
        :param root: the tkinter window
        """
        # Search bar for typing in query
        search_bar = tk.Entry(self.nav_master, width=45, borderwidth=5)
        search_bar.insert(0, "Enter a Ticker Symbol...")
        search_bar.grid(sticky="nw", row=0, column=0, ipadx=1, ipady=1)

        # The user can choose to submit the query by pressing enter
        def handle_search(event):
            self.search_query(search_bar)

        search_bar.bind('<Return>', handle_search)

        # Search button also available for submitting the search query
        search_button = tk.Button(self.nav_master, overrelief="solid", text="Search",
                                  command=lambda: self.search_query(search_bar))
        search_button.grid(row=0, column=1, ipady=1, sticky="nw")


    def search_query(self, search_bar):
        """
        Callback function for handling search queries, fetching info on the security
        :param search_bar: the search bar widget and search content
        """

        self.root.config(width=100)
        query = search_bar.get()
        dc = DesController(query)
        self.info_data = dc.get_info()
        self.news_data = dc.get_news()
        self.history_data = dc.get_history()
        # call the function here to get the function instead of selecting an item from the dropdown menu again
        self.function_navigate(self.selection, self.root, self.win_width, self.win_height)

    def function_dropdown(self):
        """
        Dropdown menu widget used to navigate to various functions (default function is des)
        :param root: the tkinter window
        :param win_width: the width of the tkinter window
        :param win_height: the height of the tkinter window
        """

        # The default selected option in the dropdown selection menu
        default = "DES"
        placeholder = tk.StringVar()
        placeholder.set("DES")

        # If dropdown menu item hasn't been selected yet
        if not self.selection:
            # The default function to be displayed
            self.function_navigate(default, self.root, self.win_width, self.win_height)

        # Dropdown menu for function navigation
        option_menu = tk.OptionMenu(self.nav_master, placeholder, "DES", "EQS", "WATC",
                                    command=lambda selection: self.function_navigate(selection,
                                                                                     self.root,
                                                                                     self.win_width,
                                                                                     self.win_height))
        option_menu.grid(row=0, column=2, sticky='nw')

    def function_navigate(self, selection, root, win_width, win_height):
        """
        Callback function for the function dropdown component
        :param selection: dropdown item selected
        :param root: the highest level master widget
        :param win_width: window width
        :param win_height: window height
        :return: mount the function to be displayed
        """
        self.selection = selection
        # For initialization: if there is an active frame already then unmount it
        if self.active_frame:
            self.active_frame.destroy()

        # else if no active frame then assign one
        self.active_frame = tk.Frame(root, bg="black")
        self.active_frame.grid(row=1, column=0, sticky='nsew')
        if self.info_data:
            # All Available functions
            des = Des(self.active_frame, self.info_data, self.history_data, self.news_data, win_width, win_height)
            eqs = Eqs(self.active_frame, self.info_data, win_width, win_height)
            watc = Watc(self.active_frame, self.info_data, win_width, win_height)

            functions = {"DES": des, "EQS": eqs, "WATC": watc}
            function = functions[self.selection]
            return function.main()

        elif not self.info_data:
            # TODO default state terminal
            return



if __name__ == "__main__":
    # pricing metrics as name for widget instead of price charts
    view = MainView()
