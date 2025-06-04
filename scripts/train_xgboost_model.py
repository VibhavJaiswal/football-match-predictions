import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import os

# Step 1: Load enhanced data
file_path = "data_features/epl_2023_with_team_stats.csv"
if not os.path.exists(file_path):
    print("❌ Enhanced feature file missing.")
    exit()

df = pd.read_csv(file_path)

# Step 2: Define smart features (pre-match only)
X = df[[
    "home_win_pct",
    "away_win_pct",
    "home_goal_diff_avg",
    "away_goal_diff_avg"
]]

y = df["match_result"]

# Step 3: Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Step 4: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42)

# Step 5: Train model
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
model.fit(X_train, y_train)

# Step 6: Evaluate
y_pred = model.predict(X_test)
print("✅ Model Accuracy:", accuracy_score(y_test, y_pred))
print("📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Save trained model to disk
os.makedirs("model", exist_ok=True)
model.save_model("model/xgb_model.json")

# Save label encoder too (optional for future)
import joblib
joblib.dump(label_encoder, "model/label_encoder.pkl")
