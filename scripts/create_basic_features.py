import pandas as pd
import os

# Step 1: Load cleaned CSV
csv_path = "data_cleaned/epl_2023_flat.csv"

if not os.path.exists(csv_path):
    print("❌ Cleaned CSV not found. Run flatten_match_data.py first.")
    exit()

df = pd.read_csv(csv_path)
print(f"✅ Loaded {len(df)} matches.")

# Step 2: Create match_result column
def get_result(row):
    if row["home_score"] > row["away_score"]:
        return "H"
    elif row["home_score"] < row["away_score"]:
        return "A"
    else:
        return "D"

df["match_result"] = df.apply(get_result, axis=1)

# Step 3: Save to new CSV
os.makedirs("data_features", exist_ok=True)
output_path = "data_features/epl_2023_with_result.csv"
df.to_csv(output_path, index=False)

print(f"✅ Feature-engineered file saved to: {output_path}")
print(df[["home_team", "away_team", "home_score", "away_score", "match_result"]].head(5))
