import yfinance as yf
import requests
import streamlit as st

@st.cache_data(ttl=3600)  # Cache the NAV data for 1 hour (3600 seconds)
def fetch_amfi_nav_data():
    url = "https://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?frmdt=22-May-2025"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text

def get_stock_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        todays_data = ticker.history(period='1d')
        if not todays_data.empty:
            return round(todays_data['Close'].iloc[-1], 2)
        else:
            print(f"No data for {symbol}")
            return None
    except Exception as e:
        print(f"Error fetching stock price for {symbol}: {e}")
        return None

def get_amfi_nav(scheme_code):
    try:
        nav_data = fetch_amfi_nav_data()
        scheme_code_str = str(scheme_code)
        lines = nav_data.split('\n')

        for line in lines:
            if line.startswith(scheme_code_str + ';'):
                parts = line.strip().split(';')
                if len(parts) >= 6:
                    nav = parts[4]
                    return round(float(nav), 2)
        print(f"Scheme code {scheme_code} not found in NAV data.")
        return None
    except Exception as e:
        print(f"Error fetching NAV for scheme code {scheme_code}: {e}")
        return None
