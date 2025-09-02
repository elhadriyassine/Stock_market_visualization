import yfinance as yf
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from ipywidgets import interact, widgets
import pandas as pd
import plotly.io as pio

pio.templates.default = "plotly_dark"

# Sector & stock options
sector_stocks = {
    'Technology': ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META'],
    'Finance': ['JPM', 'BAC', 'GS', 'WFC', 'MS'],
    'Healthcare': ['JNJ', 'PFE', 'UNH', 'MRK', 'ABBV'],
    'Energy': ['XOM', 'CVX', 'COP', 'SLB', 'HAL'],
    'Consumer Discretionary': ['AMZN', 'TSLA', 'NKE', 'HD', 'MCD']
}

time_horizon_options = {
    '1 Day': '1d', '5 Days': '5d', '1 Month': '1mo',
    '6 Months': '6mo', '1 Year': '1y', '5 Years': '5y'
}

# Data fetching + indicators
def get_stock_data(symbol, period):
    if period == '1d': interval = '5m'
    elif period == '5d': interval = '15m'
    elif period == '1mo': interval = '1h'
    elif period == '6mo': interval = '1d'
    else: interval = '1d'

    df = yf.Ticker(symbol).history(period=period, interval=interval)

    if df.empty:
        return None

    df['MA10'] = df['Close'].rolling(10).mean()
    df['MA50'] = df['Close'].rolling(50).mean()

    # RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Bollinger Bands
    ma20 = df['Close'].rolling(20).mean()
    std20 = df['Close'].rolling(20).std()
    df['BB_Upper'] = ma20 + 2 * std20
    df['BB_Lower'] = ma20 - 2 * std20

    return df.dropna()

# Plotting
def plot_with_indicators(symbol, horiz_label):
    if symbol is None:
        print("Please select a stock.")
        return

    period = time_horizon_options[horiz_label]
    df = get_stock_data(symbol, period)

    if df is None:
        print("No data found.")
        return

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.5, 0.25, 0.25],
        subplot_titles=("Price + MA + Bollinger Bands", "Volume", "RSI")

    )

    # Price + MA + BB
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close', line=dict(color='#FF4F1F')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA10'], name='MA10', line=dict(color='#00ECC2', dash='dot')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50', line=dict(color='#0078FF', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='#DCD3e2')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='#DCD3e2')), row=1, col=1)

    # Volume
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='lightblue'), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='lime')), row=3, col=1)
    fig.add_shape(type='line', x0=df.index[0], x1=df.index[-1], y0=70, y1=70, line=dict(dash='dash', color='red'), row=3, col=1)
    fig.add_shape(type='line', x0=df.index[0], x1=df.index[-1], y0=30, y1=30, line=dict(dash='dash', color='green'), row=3, col=1)

    fig.update_layout(
        title=f"{symbol} — {horiz_label} (Indicators)",
        height=1200,
        width=1460,
        hovermode="x unified"
    )

    fig.show()

# Dropdowns
sector_dropdown = widgets.Dropdown(options=list(sector_stocks.keys()), description=" Sector : ")
stock_dropdown = widgets.Dropdown(description=" Stock : ")
time_dropdown = widgets.Dropdown(options=list(time_horizon_options.keys()), description=" Time Horizon : ")

def update_stock_dropdown(*args):
    selected_sector = sector_dropdown.value
    stocks = sector_stocks[selected_sector]
    stock_dropdown.options = stocks
    stock_dropdown.value = stocks[0]  # Set default to first stock

sector_dropdown.observe(update_stock_dropdown, 'value')
update_stock_dropdown()  # Initialize on load

@interact
def update_plot(sector=sector_dropdown, symbol=stock_dropdown, horiz_label=time_dropdown):
    plot_with_indicators(symbol, horiz_label)
