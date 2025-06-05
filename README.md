<<<<<<< HEAD
# ⚽ Football Match Prediction System

A full-stack AI/ML project that predicts the outcome of English Premier League (EPL) football matches using XGBoost classification based on historical performance, win ratios, and goal differences. This is **Phase 1** of a production-ready system designed with real-world deployment in mind.

---

## 🚀 Features (Phase 1)

- 📥 Fetches and flattens raw match data from Football API
- 🧼 Cleans and engineers features like win ratios and goal differentials
- 🧠 Trains a machine learning model (XGBoost) on past matches
- 🔍 Predicts match outcomes (Home win, Away win, Draw)
- 🧪 Logs predictions and allows model retraining from feedback
- 🧾 Fully containerized via Docker
- 📊 Interactive Streamlit dashboard
- 🌐 FastAPI backend with deployed API endpoints

---

## 🔗 Live Demo

- 🧠 **API (FastAPI on Render)**: [football-predictor-api.onrender.com/docs](https://football-predictor-api.onrender.com/docs)
- 📊 **Dashboard (Streamlit)**: Coming soon in Phase 2

---

## 🛠️ Tech Stack

- Python, Pandas, NumPy
- XGBoost
- FastAPI
- Streamlit
- Docker
- Render (Deployment)
- Git, GitHub

---

## 📂 Project Structure (Simplified)

```
.
├── api/                    # FastAPI backend
├── data_raw/              # Raw downloaded match data
├── data_cleaned/          # Flattened CSVs
├── data_features/         # Feature-engineered datasets
├── data_training/         # Model training JSON files
├── model/                 # Trained model + encoders
├── logs/                  # Prediction logs
├── dashboard.py           # Streamlit dashboard
├── train_xgboost_model.py # Model training script
├── get_fixtures.py        # API match data fetcher
├── main.py (in /api)      # FastAPI entrypoint
└── requirements.txt
```

---

## 📦 Setup & Deployment

1. Clone the repository  
2. Create `.env` file with your Football API key  
3. Install requirements:  
   ```bash
   pip install -r requirements.txt
   ```
4. Run FastAPI backend:  
   ```bash
   uvicorn api.main:app --reload
   ```
5. Run Streamlit dashboard:  
   ```bash
   streamlit run dashboard.py
   ```

---

## 🔮 Next Steps (Phase 2)

- 🔁 Automate model retraining from logs
- 🔄 Add CI/CD pipelines
- 🔐 Secure API with token-based auth
- 📊 Deploy Streamlit dashboard
- 📅 Add fixture-based batch prediction system

---

## 👤 Author

**Vibhav Jaiswal**  
AI/ML Engineer | [LinkedIn](https://www.linkedin.com/in/vibhavjaiswal)

---

> ⚠️ _This project is for educational and demonstration purposes. Match predictions are not guaranteed and should not be used for betting._
=======
# Football Match Prediction System

Phase 1: Initial ML model, FastAPI backend, and test API endpoint.

More features and dashboard integration coming soon.
>>>>>>> 4c38e94a0eceefbb4c02376b5cd043ec4c6030b9
