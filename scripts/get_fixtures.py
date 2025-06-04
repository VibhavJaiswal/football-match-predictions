import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime

# Load API key
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

print("API Key loaded:", API_KEY)
if not API_KEY:
    print("❌ ERROR: API key is missing. Check your .env file.")
    exit()

# API endpoint and headers
url = "https://v3.football.api-sports.io/fixtures"
headers = {
    "x-apisports-key": API_KEY
}

# Use today's date
today = datetime.today().strftime('%Y-%m-%d')
params = {
    "date": today
}

# Send request
response = requests.get(url, headers=headers, params=params)
print("Status Code:", response.status_code)

# Save response if successful
if response.status_code == 200:
    data = response.json()
    matches = data['response']
    print("Number of matches today:", len(matches))

    if matches:
        # Create data_raw folder if not exists
        os.makedirs("data_raw", exist_ok=True)

        # File path
        filename = f"data_raw/matches_{today}.json"

        # Save data
        with open(filename, "w", encoding='utf-8') as f:
            json.dump(matches, f, indent=2)

        print(f"✅ Matches saved to: {filename}")
    else:
        print("⚠️ No matches scheduled for today.")
else:
    print("❌ API Request Failed")
    print("Response Text:", response.text)
