from fastapi import FastAPI
from pydantic import BaseModel
import xgboost as xgb
import numpy as np
import joblib
import csv
import os
from datetime import datetime

# Load model and label encoder
model = xgb.XGBClassifier()
model.load_model("model/xgb_model.json")
label_encoder = joblib.load("model/label_encoder.pkl")

# Define input structure
class MatchFeatures(BaseModel):
    home_win_pct: float
    away_win_pct: float
    home_goal_diff_avg: float
    away_goal_diff_avg: float

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Football Match Predictor is Live!"}

@app.post("/predict/")
def predict_result(features: MatchFeatures):
    input_data = np.array([[
        features.home_win_pct,
        features.away_win_pct,
        features.home_goal_diff_avg,
        features.away_goal_diff_avg
    ]])

    pred = model.predict(input_data)[0]
    result_label = label_encoder.inverse_transform([pred])[0]

    # Log the prediction
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "home_win_pct": features.home_win_pct,
        "away_win_pct": features.away_win_pct,
        "home_goal_diff_avg": features.home_goal_diff_avg,
        "away_goal_diff_avg": features.away_goal_diff_avg,
        "prediction": result_label
    }

    # Ensure log directory exists
    os.makedirs("logs", exist_ok=True)
    log_file = "logs/predictions.csv"

    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

    return {"prediction": result_label}
