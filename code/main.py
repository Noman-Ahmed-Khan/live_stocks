import yfinance as yf
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
# import pytz 
import ta
import currencyapicom


def fetch_data(ticker, period, interval):
    if period=='1wk':
        end_date=datetime.now()
        start_date = end_date - timedelta(days=7)
        data=yf.download(ticker, start=start_date, end=end_date, interval=interval)
    else:
        data=yf.download(ticker, period=period, interval=interval)
    return data


def process_data(data,time_zone="US/Eastern",currency="USD"):

    if data.index.tzinfo is None:
        data.index=data.index.tz_localize('UTC')
    data.index = data.index.tz_convert(time_zone)
    data=data.reset_index()
    data=data.rename(columns={'Date':'Datetime'})

    if (currency!="USD"):
        try:
            client = currencyapicom.Client('cur_live_VSWJyndJL2fYsXbxYk2E8i3WKDYLtHq7nmLR0yKc')
            result = client.latest('USD', currencies=[currency])
            exchange = result['data'][currency]['value']
            data['Close'] = data['Close'] * exchange
            data['High'] = data['High'] * exchange
            data['Low'] = data['Low'] * exchange
            data['Volume'] = data['Volume'] * exchange
        except Exception as e:
            st.error(f"Failed to fetch currency conversion data: {str(e)}")
            currency = "USD"

    return data,currency


def metrics(data):

    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close-prev_close
    pct_change = (change/prev_close)*100
    high = data['High'].max()
    low = data['Low'].min()
    volume= data['Volume'].sum()

    return last_close, prev_close, change, pct_change, high, low, volume


def ta_indicators(data):
    data['SMA_20']=ta.trend.sma_indicator(data['Close'],window=20)
    data['EMA_20']=ta.trend.ema_indicator(data['Close'],window=20)

    return data


interval_map={
    '1d':'1m',
    '1wk':'30m',
    '1mo':'1d',
    '1y':'1wk',
    'max':'1wk',    
}


currencies = [('US Dollar', 'USD'),
('Pound Sterling', 'GBP'),
('Japanese Yen', 'JPY'),
('Renminbi Yuan', 'CNY'),
('Euro', 'EUR'),
('Indian Rupee', 'INR'),
('Brazilian Real', 'BRL'),
('Russian Ruble', 'RUB'),
('Canadian Dollar', 'CAD'),
('Australian Dollar', 'AUD'),
('South African Rand', 'ZAR'),
('Mexican Peso', 'MXN'),
('Indonesian Rupiah', 'IDR'),
('Turkish Lira', 'TRY'),
('South Korean Won', 'KRW'),
('Thai Baht', 'THB'),
('Philippine Peso', 'PHP'),
('Vietnamese Dong', 'VND'),
('Malaysian Ringgit', 'MYR'),
('Singapore Dollar', 'SGD'),
('Saudi Riyal', 'SAR'),
('Iranian Rial', 'IRR'),
('Israeli Shekel', 'ILS'),
('Kuwaiti Dinar', 'KWD'),
('Qatari Riyal', 'QAR'),
('UAE Dirham', 'AED'),
('Omani Rial', 'OMR'),
('Bahraini Dinar', 'BHD'),
('Pakistani Rupee', 'PKR'),
('Bangladeshi Taka', 'BDT'),
('Sri Lankan Rupee', 'LKR'),
('Nepalese Rupee', 'NPR'),
('Bhutanese Ngultrum', 'BTN'),
('Maldivian Rufiyaa', 'MVR'),
('Myanmar Kyat', 'MMK'),
('Lao Kip', 'LAK'),
('Cambodian Riel', 'KHR'),
('Brunei Dollar', 'BND'),
('United States Dollar', 'USD'),
(' New Guinean Kina',	'PGK'),
('Solomon Islands Dollar', 'SBD'),
('Vanuatu Vatu', 'VUV'),
('Fiji Dollar', 'FJD'),
('Tongan Pa\'anga', 'TOP'),
('Samoan Tala', 'WST')]


st.set_page_config(layout='wide')
st.title("Real Time Stock DashBoard")


st.sidebar.header("Parameters")
ticker = st.sidebar.text_input('Ticker', 'MSFT')
time_zone = st.sidebar.text_input('Time Zone', 'US/Eastern')
time_period = st.sidebar.selectbox('Time Duration',['1d','1wk','1mo','1y','max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick','Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20','EMA 20'])
currency_name, currency_code = st.sidebar.selectbox('Currency', currencies)


if st.sidebar.button('Update'):
    data=fetch_data(ticker,time_period,interval_map[time_period])
    data,currency_code=process_data(data,time_zone,currency_code)
    data=ta_indicators(data)

    last_close, prev_close, change, pct_change, high, low, volume=metrics(data)

    st.metric(label=f"{ticker} Last Price",value=f"{last_close:.2f} {currency_code}",delta=f"{change:.2f} ({pct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high:.2f} {currency_code}")
    col2.metric("Low", f"{low:.2f} {currency_code}")
    col3.metric("Volume", f"{volume:.2f} {currency_code}")

    fig = go.Figure()

    if chart_type == 'Candlestick':
        fig.add_trace(go.Candlestick(x=data['Datetime'],
                                     open=data['Open'],
                                     high=data['High'],
                                     low=data['Low'],
                                     close=data['Close']))

    else:
        fig = px.line(data, x = 'Datetime', y='Close')
    

    for indicator in indicators:
        if indicator=='SMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'],y=data['SMA_20'], name='SMA 20'))
        else:
            fig.add_trace(go.Scatter(x=data['Datetime'],y=data['EMA_20'], name='EMA 20'))


    fig.update_layout(title=f"{ticker} {time_period.upper()} Chart",
                      xaxis_title='Time',
                      yaxis_title='Price (USD)',
                      height=600)
    st.plotly_chart(fig,use_container_width=True)

    st.subheader('Historical Data')
    st.dataframe(data[['Datetime','Open','High','Low','Close','Volume']])
    
    st.subheader('Technical Indicators')
    st.dataframe(data[['Datetime','SMA_20','EMA_20']])

    st.sidebar.header("Real-Time Stock Prices")
    stocks=['AAPL','GOOGL','AMZN','ADBE']

    for stock in stocks:
        data=fetch_data(stock,'1d','1m')
        if data is not None:
            data,currency_code=process_data(data,time_zone,currency_code)
            last_price=data['Close'].iloc[-1]
            prev_price=data['Close'].iloc[0]
            change=last_price-prev_price
            pct_change=(change/prev_price)*100
            st.sidebar.metric(f"{stock}", f"{last_price:.2f} USD", f"{change:.2f} ({pct_change:.2f})")

st.sidebar.subheader("About")
st.sidebar.info("This is a real time stock graphing app")
