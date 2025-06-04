import requests
import os
import json
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

print("API Key loaded:", API_KEY)
if not API_KEY:
    print("❌ ERROR: API key is missing. Check your .env file.")
    exit()

# Endpoint and headers
url = "https://v3.football.api-sports.io/fixtures"
headers = {
    "x-apisports-key": API_KEY
}

# Pull completed matches for EPL season 2023
params = {
    "league": 39,        # Premier League
    "season": 2023,      # Past season for training
    "status": "FT",      # Only finished matches
    "timezone": "UTC"
}

# Send request
response = requests.get(url, headers=headers, params=params)
print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()
    matches = data['response']
    print("Number of past matches:", len(matches))

    if matches:
        # Create training data folder
        os.makedirs("data_training", exist_ok=True)
        filename = "data_training/epl_2023_completed_matches.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(matches, f, indent=2)

        print(f"✅ Historical matches saved to: {filename}")
    else:
        print("⚠️ No completed matches found.")
else:
    print("❌ API Request Failed")
    print("Response Text:", response.text)
