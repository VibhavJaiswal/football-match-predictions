import streamlit as st
import pandas as pd
import os

# Load the predictions log
log_file = "logs/predictions.csv"

st.set_page_config(page_title="Football Match Prediction Dashboard", layout="wide")

st.title("⚽ Football Match Prediction Dashboard")

# Check file existence
if not os.path.exists(log_file):
    st.warning("No prediction logs found yet. Make some predictions first.")
    st.stop()

# Load data
df = pd.read_csv(log_file)

# Show summary
st.subheader("📈 Prediction Summary")
st.write(f"Total Predictions Logged: {len(df)}")

# Accuracy tracker
if "actual_result" in df.columns and df["actual_result"].notna().sum() > 0:
    eval_df = df[df["actual_result"].notna()]
    total = len(eval_df)
    correct = (eval_df["prediction"] == eval_df["actual_result"]).sum()
    accuracy = round((correct / total) * 100, 2)

    st.metric(label="🎯 Real-World Accuracy", value=f"{accuracy}%")
    st.write(f"{correct} correct out of {total} labeled predictions")

    st.subheader("📊 Confusion Matrix (Raw)")
    st.dataframe(eval_df.groupby(["prediction", "actual_result"]).size().unstack(fill_value=0))

else:
    st.info("Waiting for actual results to evaluate accuracy...")

# Detailed table
st.subheader("📋 Detailed Logs")
st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
