from datetime import datetime,time
import pandas_market_calendars as mcal
import customtkinter as ctk
import matplotlib.pyplot as plt
import mplcursors
import yfinance as yf
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox  # for popup
from datetimes import *
from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.geometry('900x800')
        self.title('Stock Market App')
        self.iconbitmap('empty.ico')

        self.input_string = ctk.StringVar(value='AAPL')
        self.time_string = ctk.StringVar(value=TIME_OPTIONS[0])
        self.start_date = ctk.StringVar(value='2023-01-01')
        self.end_date = ctk.StringVar(value=str(datetime.today().date()))
        self.time_string.trace_add('write', self.create_graph)

        self.has_data = False
        self.graph_panel = None

        InputPanel(self, self.input_string, self.time_string, self.start_date, self.end_date)

        self.market_clock = ctk.CTkLabel(self, text="", text_color="orange", font=("Arial", 12))
        self.market_clock.place(x=10, y=10)
        self.update_clock()

        self.bind('<Return>', self.input_handler)
        self.mainloop()

    def update_clock(self):
        now = datetime.now().strftime('%H:%M:%S')
        status = "Market Open" if self.is_market_open() else "Market Closed"
        self.market_clock.configure(text=f"{now} | {status}")
        self.after(1000, self.update_clock)

    def is_market_open(self):
        now = datetime.now().time()
        return time(9, 15) <= now <= time(16, 30)

    def input_handler(self, event=None):
        ticker = yf.Ticker(self.input_string.get())
        start = datetime.strptime(self.start_date.get(), '%Y-%m-%d')
        end = datetime.today()
        self.max = ticker.history(start=start, end=end)
        self.year = self.max.iloc[-290:]
        self.six_months = self.max.iloc[-230:]
        self.ninety_Days = self.max.iloc[-190:]
        self.two_months = self.max.iloc[-120:]
        self.one_month = self.max.iloc[-80:]
        self.fifteen_days = self.max.iloc[-47:]
        self.one_week = self.max.iloc[-5:]
        self.has_data = True
        self.create_graph()
        self.show_gainers_losers_popup()  # ⬅️ Show popup after loading data
    def create_graph(self, *args):
        if self.graph_panel:
            self.graph_panel.pack_forget()
        if self.has_data:
            match self.time_string.get():
                case 'Max': data = self.max
                case '1 Year': data = self.year
                case '6 Months': data = self.six_months
                case 'Month': data = self.one_month
                case 'Week': data = self.one_week
            self.graph_panel = GraphPanel(self, data)

    def show_gainers_losers_popup(self):
        if self.max is not None and not self.max.empty:
            ticker = yf.Ticker(self.input_string.get())
            info = ticker.info
            country = info.get('country', 'Unknown')

            close_prices = self.max['Close']
            diffs = close_prices.diff().dropna()
            gainers = (diffs > 0).sum()
            losers = (diffs < 0).sum()
            total = gainers + losers
            if total > 0:
                gainer_pct = (gainers / total) * 100
                loser_pct = (losers / total) * 100
                messagebox.showinfo("Gainers vs Losers",
                                    f"Company Country: {country}\n\n"
                                    f"Gainers: {gainer_pct:.2f}%\nLosers: {loser_pct:.2f}%")
            else:
                messagebox.showinfo("Gainers vs Losers",
                                    f"Company Country: {country}\n\nNo data to calculate gainers/losers.")

class InputPanel(ctk.CTkFrame):
    def __init__(self, parent, input_string, time_string, start_date, end_date):
        super().__init__(master=parent, fg_color=INPUT_BG_COLOR)
        self.pack(fill='both', side='bottom')

        self.parent = parent
        ctk.CTkEntry(self, textvariable=input_string).pack(side='left', padx=10, pady=10)

        ctk.CTkLabel(self, text="Start Date (YYYY-MM-DD):").pack(side='left')
        ctk.CTkEntry(self, textvariable=start_date, width=100).pack(side='left')

        # Indicators
        self.sma_var = ctk.BooleanVar(value=False)
        self.ema_var = ctk.BooleanVar(value=False)
        self.rsi_var = ctk.BooleanVar(value=False)
        self.macd_var = ctk.BooleanVar(value=False)
        self.bb_var = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(self, text="50-Day SMA", text_color=TICK_COLOR, variable=self.sma_var, command=self.trigger_update).pack(side='left')
        ctk.CTkCheckBox(self, text="200-Day EMA", text_color=TICK_COLOR, variable=self.ema_var, command=self.trigger_update).pack(side='left')
        ctk.CTkCheckBox(self, text="RSI", text_color=TICK_COLOR, variable=self.rsi_var, command=self.trigger_update).pack(side='left')
        ctk.CTkCheckBox(self, text="MACD", text_color=TICK_COLOR, variable=self.macd_var, command=self.trigger_update).pack(side='left')
        ctk.CTkCheckBox(self, text="Bollinger Bands", text_color=TICK_COLOR, variable=self.bb_var, command=self.trigger_update).pack(side='left')

        parent.sma_var = self.sma_var
        parent.ema_var = self.ema_var
        parent.rsi_var = self.rsi_var
        parent.macd_var = self.macd_var
        parent.bb_var = self.bb_var



        self.buttons = [TextButton(self, text, time_string) for text in TIME_OPTIONS]
        time_string.trace_add('write', self.unselect_all_buttons)

    def trigger_update(self):
        self.parent.create_graph()

    def unselect_all_buttons(self, *args):
        for button in self.buttons:
            button.unselect()
class TextButton(ctk.CTkLabel):
    def __init__(self, parent, text, time_string):
        super().__init__(master=parent, text=text)
        self.pack(side='right', padx=10, pady=10)
        self.bind('<Button>', self.select_handler)
        self.time_string = time_string
        self.text = text
        if time_string.get() == text:
            self.select_handler()

    def select_handler(self, event=None):
        self.time_string.set(self.text)
        self.configure(text_color=HIGHLIGHT_COLOR)

    def unselect(self):
        self.configure(text_color=TEXT_COLOR)
class GraphPanel(ctk.CTkFrame):
    def __init__(self, parent, data):
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.pack(expand=True, fill='both')

        self.data = data
        x = data.index
        y = data['Close']

        figure, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6),
                                         gridspec_kw={'height_ratios': [3, 1]})
        figure.patch.set_facecolor(BG_COLOR)
        ax.set_facecolor(BG_COLOR)
        ax2.set_facecolor(BG_COLOR)

        # Price chart with color based on daily change
        for i in range(1, len(x)):
            if y.iloc[i] > y.iloc[i - 1]:
                color='green'
            else:
                color='red'
            ax.plot(x[i - 1:i + 1], y.iloc[i - 1:i + 1], color=color)

        # Volume bar
        ax2.bar(x, data['Volume'], color='gray', width=1)

        # Indicators
        if hasattr(parent, 'sma_var') and parent.sma_var.get():
            sma = y.rolling(50).mean()
            sma_line, = ax.plot(x, sma, color='orange', label='50-day SMA')
            mplcursors.cursor(sma_line, hover=True)

        if hasattr(parent, 'ema_var') and parent.ema_var.get():
            ema = y.ewm(span=200).mean()
            ema_line, = ax.plot(x, ema, color='cyan', label='200-day EMA')
            mplcursors.cursor(ema_line, hover=True)

        if hasattr(parent, 'bb_var') and parent.bb_var.get():
            sma = y.rolling(20).mean()
            std = y.rolling(20).std()
            ax.plot(x, sma + 2 * std, linestyle='--', color='yellow', label='Upper BB')
            ax.plot(x, sma - 2 * std, linestyle='--', color='pink', label='Lower BB')

        if hasattr(parent, 'rsi_var') and parent.rsi_var.get():
            delta = y.diff()
            gain = delta.clip(lower=0)
            loss = -delta.clip(upper=0)
            avg_gain = gain.rolling(14).mean()
            avg_loss = loss.rolling(14).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            ax2.plot(x, rsi, color='purple', label='RSI')

        if hasattr(parent, 'macd_var') and parent.macd_var.get():
            ema_12 = y.ewm(span=12).mean()
            ema_26 = y.ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            ax2.plot(x, macd, label='MACD', color='blue')
            ax2.plot(x, signal, label='Signal', color='red')

        # Axis ticks & labels color
        ax.tick_params(axis='x', colors=TICK_COLOR)
        ax.tick_params(axis='y', colors=HIGHLIGHT_COLOR)
        ax2.tick_params(axis='x', colors=TICK_COLOR)
        ax2.tick_params(axis='y', colors=HIGHLIGHT_COLOR)

        # Set axis label colors
        ax.yaxis.label.set_color(HIGHLIGHT_COLOR)
        ax2.yaxis.label.set_color(HIGHLIGHT_COLOR)

        # Set titles if needed
        ax.set_title("Price Chart", color=HIGHLIGHT_COLOR, fontsize=12)
        ax2.set_title("Volume & Indicators", color=HIGHLIGHT_COLOR, fontsize=10)

        # Legend customization
        handles, labels = ax.get_legend_handles_labels()

        if handles:
            legend = ax.legend(
                loc='upper left',
                fontsize='small',
                facecolor=BG_COLOR
            )

            for text in legend.get_texts():
                text.set_color(HIGHLIGHT_COLOR)

        # Interactive cursor
        line = ax.plot(x, y, alpha=0)[0]
        cursor = mplcursors.cursor(line, hover=True)

        @cursor.connect("add")
        def on_add(sel):
            i = sel.index
            date = x[i].strftime('%Y-%m-%d')
            price = y.iloc[i]
            change = ((y.iloc[i] - y.iloc[i - 1]) / y.iloc[i - 1] * 100) if i > 0 else 0
            sel.annotation.set_text(f"Date: {date}\nPrice: ₹{price:.2f}\nChange: {change:.2f}%")
            sel.annotation.get_bbox_patch().set(fc=BG_COLOR, alpha=0.9)
            sel.annotation.get_text().set_color(HIGHLIGHT_COLOR)

        self.figure = figure
        FigureCanvasTkAgg(figure, self).get_tk_widget().pack(fill='both', expand=True)

App()