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
        self.root.geometry("855x600")
        self.root.update_idletasks()

        # the root frame width
        self.win_width = self.root.winfo_width()
        # the root frame height
        self.win_height = self.root.winfo_height()
        # state management for storing the currently active page
        self.selection = None
        # state management for storing the currently active grid slaves
        self.active_frame = None
        # state management for storing the information on the company
        self.info = None
        # Used for searching up securities
        self.search_bar()
        # Used for changing functions
        self.function_dropdown()

        # live clock
        self.clock()

        self.root.mainloop()

    def clock(self):
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        time = tk.Label(self.root, bg="black", fg="orange", text=formatted_time, anchor="ne", font="helvetica 12 bold")
        time.place(x=780, y=10)
        self.root.after(1000, self.clock)


    def search_bar(self):
        """
        Search bar widget that is permanently visible, used to search for securities
        :param root: the tkinter window
        """
        # Search bar for typing in query
        search_bar = tk.Entry(width=45, borderwidth=5)
        search_bar.insert(0, "Enter a Ticker Symbol...")
        search_bar.grid(sticky="w", row=0, column=0, ipadx=1, ipady=1)

        # Submit button for submitting the search query
        search_button = tk.Button(self.root, overrelief="sunken", text="Search",
                                  command=lambda: self.search_query(search_bar))
        search_button.place(x=382, y=1)


    def search_query(self, search_bar):
        """
        Callback function for handling search queries
        :param search_bar: the search bar widget and search content
        """
        query = search_bar.get()
        dc = DesController(query)
        self.info = dc.get_info()

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
        option_menu = tk.OptionMenu(self.root, placeholder, "DES", "EQS", "WATC",
                                    command=lambda selection: self.function_navigate(selection,
                                                                                     self.root,
                                                                                     self.win_width,
                                                                                     self.win_height))
        option_menu.place(x=460, y=0)

    def function_navigate(self, selection, root, win_width, win_height):
        """
        Callback function for the function dropdown component
        :param selection:
        :param root:
        :param win_width:
        :param win_height:
        :return: mount the function to be displayed
        """

        self.selection = selection
        # For initialization: if there is an active frame already then unmount it
        if self.active_frame:
            self.active_frame.destroy()

        # else if no active frame then assign one
        self.active_frame = tk.Frame(root, bg="black")
        self.active_frame.grid(row=1, column=0, sticky='NSEW')

        if self.info:
            # All Available functions
            des = Des(self.active_frame, self.info, win_width, win_height)
            eqs = Eqs(self.active_frame, self.info, win_width, win_height)
            watc = Watc(self.active_frame, self.info, win_width, win_height)

            functions = {"DES": des, "EQS": eqs, "WATC": watc}
            function = functions[self.selection]
            return function.main()

        elif not self.info:
            # TODO default state of hkg
            return



if __name__ == "__main__":
    # pricing metrics as name for widget instead of price charts
    view = MainView()
