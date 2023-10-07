import webbrowser

def handle_open_link(e, news_link, news_widget):
    """event handler for opening up links in the browser"""
    webbrowser.open(news_link)


def handle_on_enter(e, news_link, news_widget):
    """event handler runs when mouse enters widget"""
    news_widget.config(bg="black", fg="orange", font="TkDefaultFont 10 underline")


def handle_on_leave(e, news_link, news_widget):
    """event handler runs when mouse leaves widget"""
    news_widget.config(bg="black", fg="white", font="TkDefaultFont 10")
