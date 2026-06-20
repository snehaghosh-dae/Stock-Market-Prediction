# Stock-Market-Prediction
# 📌Project Overview
This project is a stock market prediction that fetches percentages of gainers and loosers about stock market from yahoo finance data and displays it using a customtkinter-based graphical user interface (GUI).
# 🛠️ Tools & Technologies
- datetime
- pandas_market_calendars
-  customtkinter
-  matplotlib.pyplot
-  mplcursors
-  yfinance
-  numpy
-  pandas
-  FigureCanvasTkAgg
-  messagebox
-  SMA, EMA, RSI, MACD, Bollinger Bands(upper and lower)

# 📱Main Application (App class)
- Creates a 900x800 window for displaying stock charts
- Maintains a live market status indicator (shows if the market is open/closed)
- Manages data for multiple time periods: Max, 1 Year, 6 Months, 1 Month, Week, etc.
- Fetches stock data from Yahoo Finance via yfinance
  <img width="1440" height="847" alt="Stock Market App" src="https://github.com/user-attachments/assets/34b25c7b-db50-4c70-8cce-95395fe80385" />

# Input Panel (InputPanel class)
- Stock ticker entry field (defaults to 'AAPL')
- Date range selection (start and end dates)
- Technical indicator checkboxes:
- 50-Day SMA (Simple Moving Average)
- 200-Day EMA (Exponential Moving Average)
- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Bollinger Bands
- Time period buttons for quick selection

# Graph Panel (GraphPanel class)
- Dual-chart visualization:
  - Top chart: Price history with color-coded candles (green for gains, red for losses)
  - Bottom chart: Trading volume + selected technical indicators
- Interactive cursor with hover tooltips showing:
  - Date
  - Price (in ₹)
  - Daily percentage change
- Legend for all overlaid indicators
- Dark theme color scheme for professional appearance

