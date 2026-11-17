import os
import pickle as pk
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import (r2_score,mean_absolute_error,mean_squared_error)
from sklearn.linear_model import (LinearRegression,Lasso)
from sklearn.neighbors import (KNeighborsRegressor)
from sklearn.tree import (DecisionTreeRegressor)
from sklearn.ensemble import (RandomForestRegressor,GradientBoostingRegressor)

DATASET_PATH = "Cardetails.csv"
MODEL_PATH = "models.pkl"

def preprocess_data(data):

    data = data.copy()
    data = data.dropna().copy()
    data = data.drop_duplicates().copy()
    if "torque" in data.columns:
        data = data.drop(columns=["torque"])

    def get_brand_name(car_name):
        return str(car_name).split(" ")[0].strip()

    def clean_data(value):
        try:
            value = str(value).split(" ")[0].strip()
            if value == "":
                return np.nan
            return float(value)
        except (
            ValueError,TypeError):
            return np.nan

    if "name" in data.columns:
        data["name"] = data["name"].apply(get_brand_name)

    if "mileage" in data.columns:
        data["mileage"] = data["mileage"].apply(clean_data)

    if "engine" in data.columns:
        data["engine"] = data["engine"].apply(clean_data)

    if "max_power" in data.columns:
        data["max_power"] = data["max_power"].apply(clean_data)

    brand_mapping = {
        "Maruti": 1,
        "Skoda": 2,
        "Honda": 3,
        "Hyundai": 4,
        "Toyota": 5,
        "Ford": 6,
        "Renault": 7,
        "Mahindra": 8,
        "Tata": 9,
        "Chevrolet": 10,
        "Datsun": 11,
        "Jeep": 12,
        "Mercedes-Benz": 13,
        "Mitsubishi": 14,
        "Audi": 15,
        "Volkswagen": 16,
        "BMW": 17,
        "Nissan": 18,
        "Lexus": 19,
        "Jaguar": 20,
        "Land": 21,
        "MG": 22,
        "Volvo": 23,
        "Daewoo": 24,
        "Kia": 25,
        "Fiat": 26,
        "Force": 27,
        "Ambassador": 28,
        "Ashok": 29,
        "Isuzu": 30,
        "Opel": 31
    }

    transmission_mapping = {"Manual": 1, "Automatic": 2}
    seller_mapping = {"Individual": 1,"Dealer": 2,"Trustmark Dealer": 3}
    fuel_mapping = {"Diesel": 1,"Petrol": 2,"LPG": 3,"CNG": 4}
    owner_mapping = {"First Owner": 1,"Second Owner": 2,"Third Owner": 3,"Fourth & Above Owner": 4,"Test Drive Car": 5}
    if "name" in data.columns:
        data["name"] = data["name"].map(brand_mapping)

    if "transmission" in data.columns:
        data["transmission"] = data["transmission"].map(transmission_mapping)

    if "seller_type" in data.columns:
        data["seller_type"] = data["seller_type"].map(seller_mapping)

    if "fuel" in data.columns:
        data["fuel"] = data["fuel"].map(fuel_mapping)

    if "owner" in data.columns:
        data["owner"] = data["owner"].map(owner_mapping)

    data = data.dropna().copy()
    if "selling_price" not in data.columns:
        raise ValueError(
            "The dataset does not contain "
            "'selling_price' column.")
    return data

def train_models():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset '{DATASET_PATH}' "
            "was not found.")
    print("Loading dataset...")
    data = pd.read_csv(DATASET_PATH)
    print(f"Original dataset shape: "f"{data.shape}")

    print("Preprocessing dataset...")
    data = preprocess_data(data)
    print(f"Processed dataset shape: "f"{data.shape}")

    X = data.drop(columns=["selling_price"])
    y = data["selling_price"]
    feature_columns = list(X.columns)
    print("\nFeatures used for training:")
    print(feature_columns)
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20,random_state=10)
    print(f"\nTraining rows: "f"{len(X_train)}")
    print(f"Testing rows: "f"{len(X_test)}")

    target_scaler = StandardScaler()
    y_train_scaled = target_scaler.fit_transform(y_train.to_numpy().reshape(-1, 1)).ravel()
    y_test_scaled = target_scaler.transform( y_test.to_numpy().reshape(-1, 1)).ravel()
    y_test_scaled = target_scaler.transform(y_test.to_numpy().reshape(-1,1)).ravel()
    print("\nTarget scaling completed.")

    models = {
        "Linear Regression":LinearRegression(),
        "Lasso Regression":Lasso(),
        "KNN":KNeighborsRegressor(),
        "Decision Tree":DecisionTreeRegressor(random_state=42),
        "Random Forest":RandomForestRegressor(random_state=42),
        "Gradient Boosting":GradientBoostingRegressor(random_state=42)
    }
    metrics = {}
    print("\nTraining models...\n")

    for model_name, model in models.items():
        print(f"Training: "f"{model_name}")
        model.fit(X_train,y_train_scaled)
        y_pred_scaled = model.predict(X_test)
        r2 = r2_score(y_test_scaled,y_pred_scaled)
        mae = mean_absolute_error(y_test_scaled,y_pred_scaled)
        rmse = np.sqrt(mean_squared_error(y_test_scaled,y_pred_scaled))
        metrics[model_name] = {
            "r2": float(r2),"mae": float(mae),
            "rmse": float(rmse)
        }
        print(f"  R² Score : "f"{r2:.4f}")
        print(f"  MAE      : "f"{mae:.4f}")
        print(f"  RMSE     : "f"{rmse:.4f}")

    saved_data = {
        "models": models,
        "metrics": metrics,
        "feature_columns": feature_columns,
        "target_scaler": target_scaler
    }

    with open(MODEL_PATH,"wb") as file:
        pk.dump(saved_data,file)

    if os.path.exists(MODEL_PATH):
        print("Models trained successfully!")
        print(f"Saved file: "f"{MODEL_PATH}")
    else:
        raise RuntimeError("Training completed, but ""models.pkl was not created.")
    
    print("\nFinal Model Performance:")
    print("-" * 80)
    for model_name, score in metrics.items():
        print(f"{model_name:<25}"f" R²: "f"{score['r2']:.4f}"f" | MAE: "f"{score['mae']:.4f}"f" | RMSE: "f"{score['rmse']:.4f}")
    print("-" * 80)
    return saved_data

if __name__ == "__main__":
    train_models()

