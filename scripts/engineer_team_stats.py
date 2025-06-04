import pandas as pd
from datetime import datetime
import os

# Step 1: Load match data
input_path = "data_features/epl_2023_with_result.csv"
output_path = "data_features/epl_2023_with_team_stats.csv"

if not os.path.exists(input_path):
    print("❌ Input file missing.")
    exit()

df = pd.read_csv(input_path)

# Step 2: Convert date column to datetime and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# Step 3: Initialize empty lists to store features
home_win_pct_list = []
away_win_pct_list = []
home_goal_diff_avg = []
away_goal_diff_avg = []

# Step 4: Process each match
for idx, row in df.iterrows():
    match_date = row["date"]
    home = row["home_team"]
    away = row["away_team"]

    # Get past matches of each team
    past_home = df[(df["home_team"] == home) | (df["away_team"] == home)]
    past_home = past_home[past_home["date"] < match_date]

    past_away = df[(df["home_team"] == away) | (df["away_team"] == away)]
    past_away = past_away[past_away["date"] < match_date]

    # Home team stats
    if not past_home.empty:
        home_wins = 0
        home_goal_diff = []

        for _, m in past_home.iterrows():
            if m["home_team"] == home:
                result = m["match_result"]
                goal_diff = m["home_score"] - m["away_score"]
                if result == "H":
                    home_wins += 1
            else:  # played as away
                result = m["match_result"]
                goal_diff = m["away_score"] - m["home_score"]
                if result == "A":
                    home_wins += 1

            home_goal_diff.append(goal_diff)

        home_win_pct = home_wins / len(past_home)
        avg_goal_diff = sum(home_goal_diff) / len(home_goal_diff)
    else:
        home_win_pct = 0.5  # neutral default
        avg_goal_diff = 0

    # Away team stats
    if not past_away.empty:
        away_wins = 0
        away_goal_diff = []

        for _, m in past_away.iterrows():
            if m["home_team"] == away:
                result = m["match_result"]
                goal_diff = m["home_score"] - m["away_score"]
                if result == "H":
                    away_wins += 1
            else:
                result = m["match_result"]
                goal_diff = m["away_score"] - m["home_score"]
                if result == "A":
                    away_wins += 1

            away_goal_diff.append(goal_diff)

        away_win_pct = away_wins / len(past_away)
        avg_away_diff = sum(away_goal_diff) / len(away_goal_diff)
    else:
        away_win_pct = 0.5
        avg_away_diff = 0

    # Append to lists
    home_win_pct_list.append(round(home_win_pct, 2))
    away_win_pct_list.append(round(away_win_pct, 2))
    home_goal_diff_avg.append(round(avg_goal_diff, 2))
    away_goal_diff_avg.append(round(avg_away_diff, 2))

# Step 5: Add to DataFrame
df["home_win_pct"] = home_win_pct_list
df["away_win_pct"] = away_win_pct_list
df["home_goal_diff_avg"] = home_goal_diff_avg
df["away_goal_diff_avg"] = away_goal_diff_avg

# Step 6: Save result
df.to_csv(output_path, index=False)
print(f"✅ Enhanced data saved to: {output_path}")
print(df[["home_team", "away_team", "match_result", "home_win_pct", "away_win_pct"]].head(10))
