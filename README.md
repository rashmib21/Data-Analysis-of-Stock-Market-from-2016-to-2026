# NSE Stock Data Downloader
### Powered by Angel One SmartAPI

Download 10 years of daily stock price data for 42 Nifty companies — automatically, cleanly, and saved into one CSV file.

---

## What This Script Does

1. Downloads the master list of all NSE instruments from Angel One
2. Finds the unique token ID for each stock
3. Logs in to your Angel One account securely
4. Downloads daily OHLCV data from **January 1, 2016** to today
5. Saves everything into a single file — `50_companies_data.csv`

---

## Output Format

The final CSV has these columns:

| Column | Description |
|---|---|
| symbol | Stock name (e.g. RELIANCE, TCS) |
| datetime | Date of the trading day |
| open | Opening price |
| high | Highest price of the day |
| low | Lowest price of the day |
| close | Closing price |
| volume | Total shares traded |

---

## Stocks Covered (42 Companies)

```
ADANIPORTS   ASIANPAINT   AXISBANK     BAJAJ-AUTO   BAJAJFINSV
BAJFINANCE   BHARTIARTL   BPCL         BRITANNIA    CIPLA
COALINDIA    DRREDDY      EICHERMOT    GAIL         GRASIM
HCLTECH      HDFCBANK     HEROMOTOCO   HINDALCO     HINDUNILVR
ICICIBANK    INDUSINDBK   INDUSTOWER   INFY         IOC
ITC          JSWSTEEL     KOTAKBANK    LT           MARUTI
M&M          NESTLEIND    NTPC         ONGC         POWERGRID
RELIANCE     SBIN         SHREECEM     SUNPHARMA    TATAMOTORS
TATASTEEL    TCS
```

> **Note on symbol corrections:**
> - `HDFC` was removed — it merged into HDFCBANK in July 2023
> - `INFRATEL` was renamed to `INDUSTOWER` in December 2020
> - `MM` was corrected to `M&M` (official NSE symbol)

---

## Setup

### Step 1 — Install the required libraries

```bash
pip install smartapi-python pyotp pandas requests python-dotenv
```

### Step 2 — Create your `.env` file

Create a file named `.env` in the same folder as the script and fill in your Angel One credentials:

```
API_KEY=your_api_key_here
CLIENT_ID=your_client_id_here
PASSWORD=your_login_password_here
TOTP_SECRET=your_totp_secret_here
```

> Where to find these?
> - `API_KEY` — Angel One developer portal → My Apps
> - `CLIENT_ID` — Your Angel One login ID (e.g. A12345)
> - `PASSWORD` — Your Angel One login password or MPIN
> - `TOTP_SECRET` — The base-32 key shown when you first set up 2FA in Angel One app (not the 6-digit OTP — the secret key behind it)

### Step 3 — Run the script

```bash
python download_stocks.py
```

---

## How It Works Internally

**Why does it download in chunks?**
Angel One's API allows a maximum of 1 year of data per request. So for 10 years, the script makes 11 requests per stock — one chunk per year — and stitches them together.

**Why does it re-login every 5 stocks?**
Angel One sessions expire after a few minutes. With 42 stocks and a 0.5 second delay between each request, the total download takes several minutes. The script automatically refreshes the login every 5 stocks to prevent session timeouts — which was the reason earlier runs returned only ~10,000 rows instead of ~96,000.

**What does the delay do?**
The 0.5 second pause between each API call is to avoid hitting Angel One's rate limit (too many requests too fast will get you temporarily blocked).

---

## Expected Output

When it finishes you will see something like:

```
done! saved 96,267 rows to 50_companies_data.csv
stocks downloaded: 42
date range: 2016-01-01 to 2026-03-31

rows per stock:
  ADANIPORTS  :  2318 rows
  ASIANPAINT  :  2518 rows
  AXISBANK    :  2518 rows
  ...
```

---

## File Structure

```
your-project-folder/
│
├── download_stocks.py     the main script
├── .env                   your secret credentials (never share this)
├── README.md              this file
└── 50_companies_data.csv  created after running the script
```

---

## Common Errors

**Login failed**
Double check your `CLIENT_ID`, `PASSWORD`, and `TOTP_SECRET` in the `.env` file. Make sure there are no extra spaces.

**Stock not found**
The stock may be delisted, renamed, or the symbol may be slightly different on NSE. Check the Angel One scrip master file for the correct symbol.

**Got zero rows for a stock**
This usually means the session expired mid-download. The script re-logins every 5 stocks to handle this, but if it still happens, try reducing the number of stocks or increasing the re-login frequency.

**Module not found**
Run `pip install smartapi-python pyotp pandas requests python-dotenv` again and make sure you are using the correct Python environment.

---

## Requirements

- Python 3.7 or above
- An active Angel One trading account
- API access enabled on your Angel One account
- Internet connection
