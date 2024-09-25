# Disclaimer

This project is for visualization purposes only. It does not provide financial advice or recommendations on how to trade stocks. Users are advised to conduct their own research and consult with a financial advisor before making any investment decisions. The visualizations and data presented in this application should not be considered a substitute for professional financial advice.

# Real-Time Stock Dashboard

This project is a real-time stock dashboard application built using **Streamlit**, **yfinance**, **Plotly**, and **technical analysis** libraries. It allows users to visualize stock price data, apply technical indicators, and view historical stock information in a user-friendly interface.

## Features

- Fetch real-time stock data from Yahoo Finance.
- Visualize stock prices using **candlestick** or **line charts**.
- Display technical indicators such as **Simple Moving Average (SMA)** and **Exponential Moving Average (EMA)**.
- Convert stock prices to various currencies.
- Show real-time prices for selected stocks.
- Customize the time zone and duration for stock data.
- Display historical data and technical indicators in a tabular format.

## Requirements

To run this application, you need the following libraries:

- `yfinance`
- `streamlit`
- `plotly`
- `pandas`
- `datetime`
- `pytz`
- `ta`
- `currencyapicom`

You can install the required libraries using pip:

```bash
pip install yfinance streamlit plotly pandas pytz ta currencyapicom
```

## How to Run

1. Clone this repository to your local machine.

   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory.

   ```bash
   cd <project_directory>
   ```

3. Run the Streamlit application.

   ```bash
   streamlit run <filename>.py
   ```

4. Open your web browser and go to `http://localhost:8501` to view the application.

## Usage

1. **Ticker**: Input the stock ticker symbol you want to analyze (e.g., `MSFT` for Microsoft).
2. **Time Zone**: Enter the desired time zone (default is `US/Eastern`).
3. **Time Duration**: Select the time duration for the stock data (e.g., `1d`, `1wk`, `1mo`, `1y`, or `max`).
4. **Chart Type**: Choose the type of chart to display (Candlestick or Line).
5. **Technical Indicators**: Select any technical indicators you want to include (e.g., SMA 20, EMA 20).
6. **Currency**: Choose the currency for price conversion from the dropdown menu.

Click the **Update** button to refresh the data and view the updated charts and metrics.

### Real-Time Stock Prices

The sidebar displays real-time prices for popular stocks such as Apple (AAPL), Google (GOOGL), Amazon (AMZN), and Adobe (ADBE).

### About Section

The sidebar includes an "About" section that provides information about the application.

## Example

- **Input**: `Ticker: AAPL`, `Time Period: 1mo`, `Chart Type: Candlestick`, `Indicators: SMA 20`
- **Output**: Displays the Apple stock chart for the past month with a 20-period SMA overlayed.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [yfinance](https://pypi.org/project/yfinance/) for fetching stock data.
- [Streamlit](https://streamlit.io/) for creating the web application.
- [Plotly](https://plotly.com/python/) for interactive charting.
- [Technical Analysis Library (TA)](https://github.com/bashtage/ta) for calculating technical indicators.
- [Currency API](https://currencyapi.com/) for currency conversion.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you find any bugs or have suggestions for improvements.
