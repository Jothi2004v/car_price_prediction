import os
import pickle as pk
import pandas as pd
import streamlit as st
import numpy as np
from bing_image_downloader import downloader
import base64

MODEL_PATH = "models.pkl"
DATASET_PATH = "Cardetails.csv"
IMAGE_PATH ="car_image.csv"

BRAND_MAPPING = {"Maruti": 1, "Skoda": 2, "Honda": 3, "Hyundai": 4, "Toyota": 5, "Ford": 6, "Renault": 7, "Mahindra": 8, "Tata": 9, "Chevrolet": 10, "Datsun": 11, "Jeep": 12,"Mercedes-Benz": 13, "Mitsubishi": 14, "Audi": 15, "Volkswagen": 16, "BMW": 17, "Nissan": 18, "Lexus": 19, "Jaguar": 20, "Land": 21, "MG": 22, "Volvo": 23, "Daewoo": 24, "Kia": 25,"Fiat": 26, "Force": 27,"Ambassador": 28, "Ashok": 29, "Isuzu": 30, "Opel": 31,}
FUEL_MAPPING = {"Diesel": 1, "Petrol": 2, "LPG": 3, "CNG": 4}
SELLER_MAPPING = {"Individual": 1, "Dealer": 2, "Trustmark Dealer": 3}
TRANSMISSION_MAPPING = {"Manual": 1, "Automatic": 2}
OWNER_MAPPING = {"First Owner": 1,"Second Owner": 2,"Third Owner": 3,"Fourth & Above Owner": 4,"Test Drive Car": 5,}

def show_predict():

    if not os.path.exists(MODEL_PATH):
        st.warning("⚠️ Please train the models first from the About page.")
        return

    try:
        with open(MODEL_PATH, "rb") as file:
            saved_data = pk.load(file)
    except Exception as e:
        st.error(f"❌ Unable to load models.pkl: {e}")
        return

    if isinstance(saved_data, dict) and "models" in saved_data:
        models = saved_data.get("models", {})
        model_scores = saved_data.get("metrics", {})
        feature_columns = saved_data.get("feature_columns", [])
        target_scaler = saved_data.get("target_scaler")

    else:
        models = saved_data
        model_scores = {}
        feature_columns = []

    if not models:
        st.error("❌ No trained models were found.")
        return

    if not os.path.exists(DATASET_PATH):
        st.error(f"❌ Dataset '{DATASET_PATH}' was not found.")
        return

    try:
        cars_data = pd.read_csv(DATASET_PATH)
    except Exception as e:
        st.error(f"❌ Unable to read dataset: {e}")
        return

    st.header("🎯 Car Price Prediction System")
    st.markdown("***Get Instant Valuation for Your Used Car***")

    cars_data["brand"] = cars_data["name"].astype(str).str.split().str[0].str.strip()
    cars_data["model"] = (cars_data["name"].astype(str).str.split().str[1:].str.join(" ").str.strip())

    st.subheader("📈 Select Prediction Model")
    model_choice = st.selectbox("Choose Machine Learning Model", list(models.keys()), key="model_selection")
    selected_scores = model_scores.get(model_choice, {})

    if isinstance(selected_scores, dict):
        r2 = selected_scores.get("r2", 0)
        mae = selected_scores.get("mae", 0)
        rmse = selected_scores.get("rmse", 0)
        st.info(f"📌 Selected Model: {model_choice} | R² Score: {r2:.4f}")
    else:
        r2 = 0
        mae = 0
        rmse = 0
        st.info(f"📌 Selected Model: {model_choice}")

    st.divider()

    st.subheader("📝 Car Information")
    brand_list = sorted(cars_data["brand"].dropna().unique().tolist())
 
    
    col1,col2 = st.columns(2)
    with col1:
        brand = st.selectbox("🏷️ Select Car Brand", brand_list, key="car_brand")
        st.markdown(
        f"""
        <div style="
            padding:10px;
            margin-top:-10px;
            margin-bottom:15px;
            border-radius:8px;
            background-color:#f0f2f6;
        ">
            <b>Selected Car Brand:</b> {brand}
        </div>
        """,
        unsafe_allow_html=True)
        filtered_cars = cars_data[cars_data["brand"] == brand]
        model_list = sorted(filtered_cars["model"].dropna().unique().tolist())
    
        if not model_list:
            st.warning("No car models found for the selected brand.")
            return
   
        model = st.selectbox("🚘 Select Car Model", model_list, key="car_model")
        st.markdown(
            f"""
            <div style="
                padding:10px;
                margin-top:-10px;
                margin-bottom:15px;
                border-radius:8px;
                background-color:#f0f2f6;
            ">
                <b>Selected Car Model:</b> {model}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
            IMAGE_FOLDER = "Car_Images"
            brand_folder = os.path.join(IMAGE_FOLDER,brand)
            possible_extensions = [".jpg",".jpeg",".png",".webp"]
            image_path = None
            for ext in possible_extensions:
                temp_path = os.path.join(brand_folder,model + ext)

                if os.path.exists(temp_path):
                    image_path = temp_path
                    break
            if image_path:
                    st.markdown(
                        f"""
                        <div style="
                            width: 100%;
                            height: 250px;
                            border: 1px solid #dddddd;
                            border-radius: 8px;
                            background-color: #f5f5f5;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            overflow: hidden;
                        ">
                            <img
                                src="data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()}"
                                style="
                                    width: 100%;
                                    height: 100%;
                                    object-fit: contain;
                                    padding: 10px;
                                ">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # If image is not found
            else:
                    st.markdown(
                        """
                        <div style="
                            width: 100%;
                            height: 250px;
                            border: 1px solid #dddddd;
                            border-radius: 8px;
                            background-color: #f5f5f5;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            color: #777777;
                            font-size: 25px;
                        ">
                            🚘 No image available
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
 

    col1, col2 = st.columns(2)
    with col1:
        year = st.number_input("📆 Manufactured Year", min_value=1994, max_value=2026, value=2018, step=1)
        km_driven = st.number_input("⏲ Kilometers Driven",min_value=0.0,max_value=500000.0,value=30000.0,step=1000.0,)
        fuel_list = sorted(cars_data["fuel"].dropna().unique().tolist())
        fuel = st.selectbox("⛽ Fuel Type", fuel_list)
        seller_list = sorted(cars_data["seller_type"].dropna().unique().tolist())
        seller_type = st.selectbox("👨‍💼 Seller Type", seller_list)
        transmission_list = sorted(cars_data["transmission"].dropna().unique().tolist())
        transmission = st.selectbox("⚙️ Transmission Type", transmission_list)
        owner_list = sorted(cars_data["owner"].dropna().unique().tolist())
    with col2:
        owner = st.selectbox("👤 Car Owner", owner_list)
        mileage = st.number_input("⚡ Mileage (kmpl)", min_value=0.0, max_value=100.0, value=20.0, step=0.1)
        engine = st.number_input("🛠 Engine (CC)", min_value=0.0, max_value=10000.0, value=1200.0, step=50.0)
        max_power = st.number_input("🚀 Max Power (bhp)", min_value=0.0, max_value=2000.0, value=80.0, step=1.0)
        seats = st.number_input("👥 Number of Seats", min_value=2, max_value=20, value=5, step=1)

    st.markdown("<br>",unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🪄 Predict Car Price", use_container_width=True)
    if predict_button:
        brand_numeric = BRAND_MAPPING.get(brand)
        fuel_numeric = FUEL_MAPPING.get(fuel)
        seller_numeric = SELLER_MAPPING.get(seller_type)
        transmission_numeric = TRANSMISSION_MAPPING.get(transmission)
        owner_numeric = OWNER_MAPPING.get(owner)

        if brand_numeric is None:
            st.error(f"❌ Brand '{brand}' was not found in the training mapping.")
            return

        if fuel_numeric is None:
            st.error(f"❌ Fuel type '{fuel}' was not found in the training mapping.")
            return

        if seller_numeric is None:
            st.error(f"❌ Seller type '{seller_type}' was not found in the training mapping.")
            return

        if transmission_numeric is None:
            st.error(f"❌ Transmission '{transmission}' was not found ""in the training mapping.")
            return
        if owner_numeric is None:
            st.error(f"❌ Owner '{owner}' was not found in the training mapping.")
            return

        input_data = pd.DataFrame({
                "name": [brand_numeric],
                "year": [year],
                "km_driven": [km_driven],
                "fuel": [fuel_numeric],
                "seller_type": [seller_numeric],
                "transmission": [transmission_numeric],
                "owner": [owner_numeric],
                "mileage": [mileage],
                "engine": [engine],
                "max_power": [max_power],
                "seats": [seats],})

        if feature_columns:
            try:
                input_data = input_data[feature_columns]
            except KeyError as e:
                st.error(f"❌ Feature mismatch: {e}")
                return
        selected_model = models[model_choice]

        try:
            with st.spinner("Calculating car price... ⏳"):
                prediction_scaled = selected_model.predict(input_data)

                if target_scaler is not None:
                    prediction_original = target_scaler.inverse_transform(np.array(prediction_scaled).reshape(-1, 1))
                    predicted_price = float(
                    prediction_original[0][0])

                else:
                    predicted_price = float(prediction_scaled[0])
        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")
            return

        if predicted_price < 0:
            predicted_price = 0


        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """<div style="display: inline-block;">
                <h3 style="margin-bottom: 0px;font-size: 18px;">💰 Estimated Price</h3>
                <div style="height: 2px; background-color: #6666ff; width: 90%; margin-top: -5px;"></div>
                </div>
                """,
                unsafe_allow_html=True)
            st.markdown(f"""
                    <div style="
                        padding:30px;
                        margin-top:20px;
                        margin-bottom:20px;
                        border-radius:18px;
                        text-align:center;
                        background:linear-gradient(135deg,
                            #129E8C,
                            #1EB985,
                            #33E77E
                        );
                        color:white;
                        box-shadow:0px 5px 15px rgba(0,0,0,0.15);
                    ">
                    <div style="
                        font-size:18px;
                        letter-spacing:1px;
                        margin-bottom:15px;
                    ">
                        ESTIMATED RESALE VALUE
                    </div>

                    <div style="
                        font-size:42px;
                        font-weight:bold;
                        margin-bottom:5px;
                    ">
                        ₹ {predicted_price / 100000:.2f}
                    </div>

                    <div style="
                        font-size:16px;
                        margin-top:5px;
                    ">
                        Lakhs
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with col2:
            st.markdown(
                            """<div style="display: inline-block;">
                            <h3 style="margin-bottom: 0px;font-size: 18px;">📊 Model Performance</h3>
                            <div style="height: 2px; background-color: #6666ff; width: 90%; margin-top: -5px; margin-bottom:50px"></div>
                            </div>
                            """,
                            unsafe_allow_html=True)
            metric1, metric2, metric3 = st.columns(3)
            with metric1:
                st.markdown(f"""<div style="
                    padding:25px;
                    text-align:center;
                    font-size:16px;
                    border-radius:18px;
                    color:white;
                    background:#3BBEFD;
                    ">
                R² Score<br>
                <span style="font-weight:bold;font-size:20px;">{r2:.4f}</span>
                </div>
                """,unsafe_allow_html=True)
                   
                  
            with metric2:
                st.markdown(
                    f"""
                    <div style="
                        padding:25px;
                        text-align:center;
                        font-size:16px;
                        border-radius:18px;
                        color:white;
                        background:#3BBEFD;
                    ">
                        MAE<br>
                         <span style="font-weight:bold;font-size:20px;">{mae:,.4f}</span>
                    </div>
                    """,unsafe_allow_html=True)

            with metric3:
                st.markdown(
                    f"""
                    <div style="
                        padding:25px;
                        text-align:center;
                        font-size:16px;
                        border-radius:18px;
                        color:white;
                        background:#3BBEFD;
                    ">
                        RMSE<br>
                         <span style="font-weight:bold;font-size:20px;">{rmse:,.4f}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,)
        st.info(
            "***Tip: This estimate is based on ML model "
            "predictions. Actual price may vary based on "
            "car condition, location, and market demand.***"
        )