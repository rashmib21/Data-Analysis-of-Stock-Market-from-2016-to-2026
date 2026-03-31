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
