import pandas as pd
import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load API key
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

if not API_KEY:
    print("❌ API key not found in .env")
    exit()

headers = {
    "x-apisports-key": API_KEY
}

# Load log file
log_file = "logs/predictions.csv"
if not os.path.exists(log_file):
    print("❌ logs/predictions.csv not found")
    exit()

df = pd.read_csv(log_file)

# Add actual_result column if missing
if "actual_result" not in df.columns:
    df["actual_result"] = ""

# Helper function to fetch result from API-Football
def fetch_result(match_date):
    # Format date as YYYY-MM-DD
    date_str = match_date.strftime("%Y-%m-%d")
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "date": date_str
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        for match in data.get("response", []):
            score = match["score"]["fulltime"]
            if score["home"] is None or score["away"] is None:
                continue

            # Determine result
            if score["home"] > score["away"]:
                return "H"
            elif score["home"] < score["away"]:
                return "A"
            else:
                return "D"
    except Exception as e:
        print(f"Error fetching result for {date_str}: {e}")
    return None

# Go through logs and update empty actual_results
for idx, row in df[df["actual_result"] == ""].iterrows():
    try:
        # Use timestamp to get date
        match_time = datetime.fromisoformat(row["timestamp"])
        result = fetch_result(match_time)

        if result:
            df.at[idx, "actual_result"] = result
            print(f"✅ Row {idx}: Filled actual_result = {result}")
        else:
            print(f"⚠️  Row {idx}: No match data found.")
    except Exception as e:
        print(f"❌ Error at row {idx}: {e}")

# Save updated log
df.to_csv(log_file, index=False)
print("\n✅ logs/predictions.csv updated with actual results.")
