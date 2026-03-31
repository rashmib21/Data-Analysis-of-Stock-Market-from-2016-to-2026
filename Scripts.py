from SmartApi import SmartConnect
import pyotp
import pandas as pd
import requests
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

API_KEY     = os.getenv("API_KEY")
CLIENT_ID   = os.getenv("CLIENT_ID")
PASSWORD    = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")


START_DATE  = datetime(2016, 1, 1, 9, 15)
OUTPUT_FILE = "50_companies_data3.csv"
DELAY       = 0.5
CHUNK_DAYS  = 365


STOCK_NAMES = [
    "ADANIPORTS", "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE",
    "BHARTIARTL", "BPCL", "BRITANNIA", "CIPLA", "COALINDIA", "DRREDDY", "EICHERMOT", "GAIL",
    "GRASIM", "HCLTECH", "HDFCBANK", "HEROMOTOCO", "HINDALCO", "HINDUNILVR", "ICICIBANK",
    "INDUSINDBK", "INDUSTOWER", "INFY", "IOC", "ITC", "JSWSTEEL", "KOTAKBANK", "LT", "MARUTI",
    "M&M", "NESTLEIND", "NTPC", "ONGC", "POWERGRID", "RELIANCE", "SBIN", "SHREECEM", "SUNPHARMA",
    "TATAMOTORS", "TATASTEEL", "TCS"
]

print("total stocks we want:", len(STOCK_NAMES))


# step 1 - download the master list of all stocks from angel one
print("downloading master stock list...")
master_url  = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
master_data = requests.get(master_url).json()
print("master list downloaded, total instruments:", len(master_data))


# step 2 - find the token number for each stock we want
print("finding tokens for our stocks...")
token_map = {}

for item in master_data:
    symbol   = item.get("symbol", "").upper()
    token    = item.get("token", "")
    exchange = item.get("exch_seg", "")

    if exchange == "NSE" and symbol.endswith("-EQ"):
        clean_name = symbol.replace("-EQ", "")
        token_map[clean_name] = token


found     = []
not_found = []

for name in STOCK_NAMES:
    if name in token_map:
        found.append(name)
    else:
        not_found.append(name)

print("stocks found:", len(found))
print("stocks not found:", len(not_found))

if len(not_found) > 0:
    print("these stocks were not found:")
    for name in not_found:
        print("  ", name)


# step 3 - login function
# we make this a function so we can call it again if the session expires
def login():
    print("logging in to angel one...")
    obj     = SmartConnect(api_key=API_KEY)
    otp     = pyotp.TOTP(TOTP_SECRET).now()
    session = obj.generateSession(CLIENT_ID, PASSWORD, otp)

    if session.get("status") == False:
        print("login failed:", session.get("message"))
        return None

    print("login successful")
    return obj


# step 4 - download price data for each stock
# angel one sessions expire after some time
# so after every 5 stocks we log in again to keep the session fresh
end_date = datetime.now().replace(hour=15, minute=30, second=0, microsecond=0)

print("downloading data from", START_DATE.date(), "to", end_date.date())

all_data     = []
stocks_done  = 0
obj          = login()

for symbol in found:

    # re-login after every 5 stocks to avoid session expiry
    # angel one sessions can time out during long downloads
    if stocks_done > 0 and stocks_done % 5 == 0:
        print("refreshing session to avoid timeout...")
        obj = login()

    token = token_map[symbol]
    print("fetching", symbol, "  (", stocks_done + 1, "of", len(found), ")")

    symbol_data = []
    chunk_start = START_DATE

    while chunk_start < end_date:
        chunk_end = chunk_start + timedelta(days=CHUNK_DAYS)

        if chunk_end > end_date:
            chunk_end = end_date

        params = {
            "exchange":    "NSE",
            "symboltoken": token,
            "interval":    "ONE_DAY",
            "fromdate":    chunk_start.strftime("%Y-%m-%d %H:%M"),
            "todate":      chunk_end.strftime("%Y-%m-%d %H:%M"),
        }

        try:
            response = obj.getCandleData(params)

            if response.get("status") and response.get("data"):
                df = pd.DataFrame(response["data"], columns=["datetime", "open", "high", "low", "close", "volume"])
                df["symbol"]   = symbol
                df["datetime"] = pd.to_datetime(df["datetime"])
                symbol_data.append(df)
                print("  got", len(df), "rows from", chunk_start.date(), "to", chunk_end.date())
            else:
                print("  no data from", chunk_start.date(), "to", chunk_end.date(), "| reason:", response.get("message", "unknown"))

        except Exception as error:
            print("  something went wrong:", error)

        chunk_start = chunk_end + timedelta(days=1)
        time.sleep(DELAY)

    if len(symbol_data) > 0:
        stock_df = pd.concat(symbol_data, ignore_index=True)
        all_data.append(stock_df)
        print("  total rows for", symbol, ":", len(stock_df))
    else:
        print("  WARNING: got zero rows for", symbol)

    stocks_done = stocks_done + 1


# step 5 - combine all stocks into one table and save to csv
if len(all_data) == 0:
    print("no data was downloaded, please check your login and try again")
else:
    combined = pd.concat(all_data, ignore_index=True)
    combined = combined[["symbol", "datetime", "open", "high", "low", "close", "volume"]]
    combined.sort_values(["symbol", "datetime"], inplace=True)
    combined.reset_index(drop=True, inplace=True)

    combined.to_csv(OUTPUT_FILE, index=False)

    print("done! saved", len(combined), "rows to", OUTPUT_FILE)
    print("stocks downloaded:", combined["symbol"].nunique())
    print("date range:", combined["datetime"].min().date(), "to", combined["datetime"].max().date())

    # show how many rows each stock has so we can spot any stock with missing data
    print("rows per stock:")
    rows_per_stock = combined.groupby("symbol").size()
    for stock_name, row_count in rows_per_stock.items():
        print("  ", stock_name, ":", row_count, "rows")