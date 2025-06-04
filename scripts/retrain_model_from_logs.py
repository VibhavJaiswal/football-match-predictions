import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Step 1: Load prediction logs
log_file = "logs/predictions.csv"
if not os.path.exists(log_file):
    print("❌ Log file missing.")
    exit()

df = pd.read_csv(log_file)

# Step 2: Filter only rows with actual results
df = df[df["actual_result"].notna()]
print(f"✅ Using {len(df)} logged predictions for retraining")

# Step 3: Select features and label
feature_cols = [
    "home_win_pct",
    "away_win_pct",
    "home_goal_diff_avg",
    "away_goal_diff_avg"
]

X = df[feature_cols]
y = df["actual_result"]

# Step 4: Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 🚨 Check class diversity
if len(set(y_encoded)) < 2:
    print(f"⚠️ Only one class ({label_encoder.classes_[0]}) present in data — skipping retraining.")
    exit()

# Step 5: Split if enough data
if len(X) >= 5:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42)

    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("\n📊 Retrained Model Evaluation:")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
else:
    print(f"\n⚠️ Only {len(X)} rows available — training on all without test split.")
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="mlogloss")
    model.fit(X, y_encoded)

# Step 6: Save model
os.makedirs("model", exist_ok=True)
model.save_model("model/xgb_model.json")
joblib.dump(label_encoder, "model/label_encoder.pkl")
print("\n✅ Retrained model saved to /model/")
