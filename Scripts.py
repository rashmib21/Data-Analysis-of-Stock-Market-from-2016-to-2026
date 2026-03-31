from SmartApi import SmartConnect   # AngelOne API library
import pyotp                        # For generating OTP
import pandas as pd                 # For working with tables (DataFrames)
import requests                     # For downloading files from internet
import time                         # For adding delays
from datetime import datetime, timedelta  # For working with dates

import os 
from dotenv import load_dotenv

load_dotenv()

#   LOGIN DETAILS
API_KEY     = os.getenv("API_KEY")
CLIENT_ID   = os.getenv("CLIENT_ID")
PASSWORD    = os.getenv("PASSWORD")
TOTP_SECRET = os.getenv("TOTP_SECRET")

#Settings  

DAYS=365*10 #10 years data 
OUTPUT_FILE="50_companies_data.xlsx"
DELAY=0.5
CHUNK_DATA=365

#List of stocks 
STOCK_NAMES=[
    "ADANIPORTS",  "ASIANPAINT", "AXISBANK", "BAJAJ-AUTO", "BAJAJFINSV", "BAJFINANCE",
    "BHARTIARTL","BPCL", "BRITANNIA","CIPLA","COALINDIA","DRREDDY", "EICHERMOT","GAIL",
    "GRASIM","HCLTECH","HDFC","HDFCBANK","HEROMOTOCO","HINDALCO","HINDUNILVR","ICICIBANK",
    "INDUSINDBK","INFRATEL","INFY","IOC","ITC","JSWSTEEL","KOTAKBANK","LT","MARUTI","MM",
    "NESTLEIND","NTPC","ONGC","POWERGRID","RELIANCE","SBIN","SHREECEM","SUNPHARMA",
    "TATAMOTORS","TATASTEEL","TCS"
]