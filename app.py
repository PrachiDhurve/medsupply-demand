import json
import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MedSupply Demand Forecast", layout="centered")

st.title("MedSupply Demand Forecast")
st.write("Predict next-day demand for a selected pharmaceutical product.")

# Load model + features
model = joblib.load("outputs/demand_model.pkl")
with open("outputs/features.json", "r") as f:
    features = json.load(f)

# Product selector
product = st.selectbox(
    "Select product",
    ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
)

# Numeric inputs
lag_1 = st.number_input("lag_1", min_value=0.0, value=10.0)
lag_2 = st.number_input("lag_2", min_value=0.0, value=9.0)
lag_3 = st.number_input("lag_3", min_value=0.0, value=8.0)
lag_7 = st.number_input("lag_7", min_value=0.0, value=7.0)

rolling_3 = st.number_input("rolling_3", min_value=0.0, value=9.0)
rolling_7 = st.number_input("rolling_7", min_value=0.0, value=8.5)
rolling_14 = st.number_input("rolling_14", min_value=0.0, value=8.0)
rolling_std_7 = st.number_input("rolling_std_7", min_value=0.0, value=2.0)
expanding_mean = st.number_input("expanding_mean", min_value=0.0, value=8.0)

# Calendar inputs
day_of_week = st.selectbox("day_of_week", list(range(7)))
month = st.selectbox("month", list(range(1, 13)))
day_of_month = st.selectbox("day_of_month", list(range(1, 32)))
week_of_year = st.selectbox("week_of_year", list(range(1, 54)))
is_weekend = st.selectbox("is_weekend", [0, 1])

# Build input dictionary
input_data = {
    "lag_1": lag_1,
    "lag_2": lag_2,
    "lag_3": lag_3,
    "lag_7": lag_7,
    "rolling_3": rolling_3,
    "rolling_7": rolling_7,
    "rolling_14": rolling_14,
    "rolling_std_7": rolling_std_7,
    "day_of_week": day_of_week,
    "month": month,
    "day_of_month": day_of_month,
    "week_of_year": week_of_year,
    "is_weekend": is_weekend,
    "expanding_mean": expanding_mean
}

# Add one-hot encoded product columns
all_products = ["M01AB", "M01AE", "N02BA", "N02BE", "N05B", "N05C", "R03", "R06"]
for p in all_products:
    input_data[f"product_{p}"] = 1 if p == product else 0

# Align with trained feature list
input_df = pd.DataFrame([input_data]).reindex(columns=features, fill_value=0)

# Optional debug view
with st.expander("Show model input"):
    st.dataframe(input_df)

# Predict
if st.button("Predict"):
    pred = model.predict(input_df)[0]
    st.success(f"Predicted next-day demand: {pred:.2f}")