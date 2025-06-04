import json
import pandas as pd
import os

# Step 1: Load the saved raw match data
file_path = "data_training/epl_2023_completed_matches.json"

if not os.path.exists(file_path):
    print("❌ Match file not found. Please run get_past_fixtures.py first.")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

print(f"Loaded {len(raw_data)} matches.")

# Step 2: Flatten useful fields
flattened = []

for match in raw_data:
    fixture = match["fixture"]
    teams = match["teams"]
    score = match["score"]
    league = match["league"]

    row = {
        "fixture_id": fixture["id"],
        "date": fixture["date"],
        "venue": fixture["venue"]["name"] if fixture["venue"] else None,
        "home_team": teams["home"]["name"],
        "away_team": teams["away"]["name"],
        "home_score": score["fulltime"]["home"],
        "away_score": score["fulltime"]["away"],
        "league": league["name"],
        "season": league["season"],
        "round": league["round"],
        "home_winner": teams["home"]["winner"],
        "away_winner": teams["away"]["winner"]
    }

    flattened.append(row)

# Step 3: Convert to DataFrame
df = pd.DataFrame(flattened)

# Step 4: Save to CSV
os.makedirs("data_cleaned", exist_ok=True)
csv_path = "data_cleaned/epl_2023_flat.csv"
df.to_csv(csv_path, index=False)

print(f"✅ Flattened data saved to: {csv_path}")
print(df.head(3))  # Show a sample of the cleaned table
