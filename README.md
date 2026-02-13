# Stock_market_visualization
Stock Market Visualization Tool
This is an interactive tool for visualizing stock market data with key technical indicators built using Python. It provides a user-friendly interface to select a stock and a time horizon, automatically fetching the relevant data and generating a detailed, multi-panel chart for analysis.

# Purpose
The primary goal of this tool is to help users quickly analyze a stock's performance by displaying its price movements alongside commonly used technical indicators. This enables traders and investors to identify trends, potential entry/exit points, and overall market sentiment.

# How It Works
The tool is built on three core libraries:

- yfinance: Used to fetch historical market data (Open, High, Low, Close, Volume) from Yahoo Finance.

- plotly: A powerful plotting library that creates dynamic and interactive charts, allowing for features like zooming, panning, and hovering for data points. The plotly_dark theme is used to provide a modern, eye-pleasing aesthetic.

- ipywidgets: Provides the interactive dropdown menus that allow the user to select the sector, stock, and time horizon without modifying the code.

The tool's core logic is handled by the get_stock_data and plot_with_indicators functions:

  - Data Fetching: The get_stock_data function uses yfinance to download historical data for a specified stock and time period. It also calculates several technical indicators:

  - Moving Averages (MA10 & MA50): The average closing price over the last 10 and 50 periods, respectively.

  - Relative Strength Index (RSI): A momentum oscillator that measures the speed and change of price movements.

  - Bollinger Bands (BB_Upper & BB_Lower): A volatility channel that shows a stock's typical price range.

  - Interactive Plotting: The plot_with_indicators function takes the fetched data and constructs a multi-panel chart using plotly.subplots.
    
It separates the visualization into three distinct subplots for clarity:

  - Price Chart: Displays the stock's closing price along with the Moving Averages and Bollinger Bands.

  - Volume Chart: Shows the trading volume for each period, indicating market activity.

  - RSI Chart: Plots the RSI value, with horizontal lines at 30 (oversold) and 70 (overbought) to assist in interpretation.

  - The @interact decorator from ipywidgets links the dropdown menus to the plotting function, so any change in the dropdowns automatically triggers a data fetch and plot refresh.

# What to Expect
When you execute the tool in an environment like Jupyter Notebook or an interactive Python session, you will be presented with three dropdown menus:

Sector: Choose from a predefined list of sectors (e.g., Technology, Finance, Energy).

Stock: Select a specific ticker symbol from the stocks available in the chosen sector.

Time Horizon: Define the period for which you want to view data (e.g., 1 Day, 1 Month, 1 Year).

Upon selecting your desired options, an interactive chart will be displayed below the menus. You can use your mouse to zoom in, pan, and hover over specific points on the chart to see detailed data for that moment in time.
