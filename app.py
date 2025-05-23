import streamlit as st
import json
import base64
from utils import get_stock_price, get_amfi_nav

# Load portfolio config
with open("portfolio_config.json") as f:
    portfolio = json.load(f)

stock_aliases = portfolio.get("stock_aliases", {})
mutual_fund_aliases = portfolio.get("mutual_fund_aliases", {})

# URLs for each stock
stock_urls = {
    "Nifty Bees": "https://www.moneycontrol.com/india/stockpricequote/etf/nipponindiaetfnifty50bees/NBE01",
    "Bajaj Hind": "https://www.moneycontrol.com/india/stockpricequote/sugar/bajajhindusthansugar/BH06",
    "Jindal Saw": "https://www.moneycontrol.com/india/stockpricequote/steel-tubespipes/jindalsaw/JS08",
    "Gateway": "https://www.moneycontrol.com/india/stockpricequote/miscellaneous/gatewaydistriparks/GD01",
    "Alkylamine": "https://www.moneycontrol.com/india/stockpricequote/chemicals/alkylamineschemicals/AAC",
    "IFCI": "https://www.moneycontrol.com/india/stockpricequote/finance-term-lending-institutions/ifci/IFC02",
    "IREDA": "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/indianrenewableenergydevelopmentagency/IREDAL",
    "BF Utilities": "https://www.moneycontrol.com/india/stockpricequote/power-generationdistribution/bfutilities/BFU",
    "MOIL": "https://www.moneycontrol.com/india/stockpricequote/miningminerals/moil/M18",
    "Morepen Labs": "https://www.moneycontrol.com/india/stockpricequote/pharmaceuticals/morepenlaboratories/ML06",
    "Genus Power": "https://www.moneycontrol.com/india/stockpricequote/electricals/genuspowerinfrastructures/GPI08",
    "PSB": "https://www.moneycontrol.com/india/stockpricequote/banks-public-sector/punjabsindbank/PSB",
    "MRPL": "https://www.moneycontrol.com/india/stockpricequote/refineries/mangalorerefinerypetrochemicals/MRP",
    "Triturbine": "https://www.moneycontrol.com/india/stockpricequote/electric-equipment/triveniturbine/TT14",
    "ACE": "https://www.moneycontrol.com/india/stockpricequote/engineering-heavy/actionconstructionequipment/ACE3",
    "Tejas Net": "https://www.moneycontrol.com/india/stockpricequote/telecommunications-equipment/tejasnetworks/TN",
    "Tata Tech": "https://www.moneycontrol.com/india/stockpricequote/diversified/tatatechnologies/TTL01",
    "Kirloskar Ferrous": "https://www.moneycontrol.com/india/stockpricequote/steel-pig-iron/kirloskarferrousindustries/KFI01",
    "CDSL": "https://www.moneycontrol.com/india/stockpricequote/finance-investment/centraldepositoryservicesltd/CDS",
    "Hind Zinc": "https://www.moneycontrol.com/india/stockpricequote/metals-non-ferrous/hindustanzinc/HZ",
    "Selan": "https://www.moneycontrol.com/india/stockpricequote/oil-drillingexploration/selanexplorationtechnology/SET"
}

# Load and encode background image
with open("your_background.jpg", "rb") as img_file:
    img_base64 = base64.b64encode(img_file.read()).decode()

# Set page config
st.set_page_config(page_title="Net Worth Dashboard", layout="wide")

# Inject CSS
st.markdown(f"""
    <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}

        [data-testid="stAppViewContainer"] > .main {{
            backdrop-filter: blur(10px);
            background-color: rgba(0, 0, 0, 0.4);
            border-radius: 16px;
            padding: 2rem;
            margin: 2rem;
            color: #ffffff;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }}

        h1, h2, h3, h4, p, .stMarkdown, .stAlert, .stText {{
            color: #ffffff !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            backdrop-filter: blur(8px);
            background-color: rgba(30, 30, 30, 0.3);
            border-radius: 12px;
            padding: 1rem;
        }}

        .separator {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.3);
            margin-bottom: 1rem;
            margin-top: 0.5rem;
        }}

        .pulse-hover {{
            transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
            display: inline-block;
        }}

        .pulse-hover:hover {{
            transform: scale(1.05);
            opacity: 0.95;
        }}

        a {{
            text-decoration: none;
            color: #00acee;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
""", unsafe_allow_html=True)

# App content
st.markdown("""
    <div style="
        max-width: 600px;
        margin: 1rem auto;
        padding: 1.5rem 2rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        background-color: rgba(0, 0, 0, 0.3);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        text-align: center;
        color: #ffffff;
        font-weight: 700;
        font-size: 2rem;
        white-space: nowrap;  /* prevents line breaks */
        overflow-x: auto;     /* allows scrolling if too long */
    ">
        💰 Dipan's Personal Finance Dashboard
    </div>
    <div style="
        max-width: 600px;
        margin: 0.2rem auto 1rem auto;
        padding: 0 1rem;
        text-align: center;
        color: #ffffff;
        font-weight: 400;
        font-size: 1.1rem;
    ">
        Live tracking of my Stocks, Mutual Funds, PPF and Savings Accounts.
    </div>
""", unsafe_allow_html=True)

total_value = 0

# -------------------- Stocks --------------------
st.header("📈 Stocks")
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
stock_total = 0

for alias, qty in portfolio["stocks"].items():
    symbol = stock_aliases.get(alias, alias)
    price = get_stock_price(symbol)
    url = stock_urls.get(alias, None)

    if price:
        value = price * qty
        stock_total += value
        if url:
            st.markdown(
                f'<div class="pulse-hover"><b><a href="{url}" target="_blank">{alias}</a></b>: ₹{value:,.2f} (Qty: {qty}, Price: ₹{price:.2f})</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="pulse-hover"><b>{alias}</b>: ₹{value:,.2f} (Qty: {qty}, Price: ₹{price:.2f})</div>',
                unsafe_allow_html=True,
            )
    else:
        st.warning(f"⚠️ Failed to fetch price for {symbol}")

st.subheader(f"**Total Stock Value:** ₹{stock_total:,.2f}")
total_value += stock_total

# -------------------- Mutual Funds --------------------
st.header("💼 Mutual Funds")
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
mf_total = 0

for alias, units in portfolio["mutual_funds"].items():
    scheme_code = mutual_fund_aliases.get(alias, alias)
    nav = get_amfi_nav(str(scheme_code))
    if nav:
        value = nav * units
        mf_total += value
        st.markdown(
            f'<div class="pulse-hover"><b>{alias} (Scheme: {scheme_code})</b>: ₹{value:,.2f} (Units: {units}, NAV: ₹{nav:.2f})</div>',
            unsafe_allow_html=True,
        )
    else:
        st.warning(f"⚠️ Failed to fetch NAV for scheme code {scheme_code}")

st.subheader(f"**Total Mutual Fund Value:** ₹{mf_total:,.2f}")
total_value += mf_total

# -------------------- PPF --------------------
st.header("🏦 Public Provident Fund (PPF)")
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
ppf = portfolio.get("ppf_balance", 0)
st.markdown(
    f'<div class="pulse-hover"><b>PPF Balance:</b> ₹{ppf:,.2f}</div>',
    unsafe_allow_html=True,
)
total_value += ppf

# -------------------- Savings Accounts --------------------
st.header("🏦 Savings Accounts")
st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
savings_total = sum(portfolio.get("savings_accounts", {}).values())

for name, amount in portfolio["savings_accounts"].items():
    st.markdown(
        f'<div class="pulse-hover">{name}: ₹{amount:,.2f}</div>',
        unsafe_allow_html=True,
    )

st.subheader(f"**Total Savings:** ₹{savings_total:,.2f}")
total_value += savings_total

# -------------------- Net Worth Summary --------------------
st.markdown("---")
st.markdown(f"""
    <div style="
        backdrop-filter: blur(10px);
        background-color: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 0.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    ">
        🧾 Total Net Worth
    </div>
    <div class="pulse-hover" style="
        display: inline-block;
        width: 100%;
        backdrop-filter: blur(10px);
        background-color: rgba(0, 0, 0, 0.3);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    ">
        ₹{total_value:,.2f}
    </div>
""", unsafe_allow_html=True)
