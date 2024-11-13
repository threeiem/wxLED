"""Configuration management for Weather LED."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Settings
NWS_USER_AGENT = os.getenv("NWS_USER_AGENT", "(WxLED, wxled@cogbill.co)")
ZIP_CODE = os.getenv("ZIP_CODE", "28711")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "300"))

# Hardware Settings
RED_PIN = int(os.getenv("RED_PIN", "17"))
GREEN_PIN = int(os.getenv("GREEN_PIN", "27"))
BLUE_PIN = int(os.getenv("BLUE_PIN", "22"))