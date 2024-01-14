import tkinter as tk


class Watc:
    def __init__(self, active_frame, info_data, news_data, win_width, win_height):
        self.active_frame = active_frame
        self.info = info_data
        self.news_data = news_data
        self.win_width = win_width
        self.win_height = win_height

        # Master widget for all widgets in the watch function
        # self.watc_master = tk.Frame(self.active_frame, bg="white", width=self.win_width)
        # self.watc_master.grid(sticky="nsew", row=0, column=0)
        # self.watc_master.rowconfigure(0, weight=1)
        # self.watc_master.columnconfigure(0, weight=1)

    def main(self):
        self.news_feed()

    def news_feed(self):
        news_feed_frame = tk.LabelFrame(self.active_frame, bg="black", fg="white", text="News Feed")
        news_feed_frame.grid(row=0, column=0, sticky="w")
        all_links = []
        for index, news_article in enumerate(self.news_data):
            article_name = news_article.get("title")
            publisher_name = news_article.get('publisher')

            link = news_article.get("link")
            all_links.append(link)

            news_feed = tk.Label(news_feed_frame, bg="black", fg="white", text=f"{publisher_name}: {article_name}")
            news_feed.grid(row=index, column=0, sticky="w")
        # sns = StockNewsSpider()
        # sns.start_requests(all_links)

    def ai_suggestions(self):
        ai_frame = tk.LabelFrame(self.active_frame, bg="black", fg="white", text="AI Suggestions")
        ai_frame.grid(sticky="nsew", row=0, column=0)



