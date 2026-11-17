import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pickle as pk
from train_model import train_models


def show_about():
    
    st.header(" Car Price Prediction Model Comparison ↔️")
    data = pd.read_csv('Cardetails.csv')
    st.subheader("***Data set***📄")
    st.write(data.head(8))
    st.divider()

    st.subheader("***Missing Values***❓")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.markdown("<h4>Before</h4>",unsafe_allow_html=True)
        st.dataframe(data.isnull().sum(),use_container_width=False)
    data = data.dropna()
    with col2:
        st.markdown("<h4>After</h4>",unsafe_allow_html=True)
        st.dataframe(data.isnull().sum(),use_container_width=False)
    st.divider()

     # Remove duplicates
    data_dup = data.duplicated().any()
    st.subheader("Duplicate Rows searching...🔍 ")
    st.error(f"***Duplicates: {data_dup}❌***")
    data = data.drop_duplicates()
    st.subheader("***Removing the Duplicates***🧹")
    st.write(data.head(8))
    data_dup = data.duplicated().any()
    st.success(f"***Duplicates: {data_dup}✅***")
    st.divider()

    # Data processing
    st.subheader("⚙️***Data Processing***")
    def get_brand_name(car_name):
            car_name = car_name.split(' ')[0]
            return car_name.strip()

    def clean_data(value):
        value = value.split(' ')[0]
        value = value.strip()
        if value == '':
            value = 0
        return float(value)

    st.markdown(f"<h4 style='font-style: italic;'>Removing Unwanted Column - <span style = 'color: #808080';> Torque</span></h4>",unsafe_allow_html=True)
    data= data.drop(columns=['torque'])
    st.write(data.head(8))
    st.divider()

    st.subheader("***Processing Numerical Columns***")
   
    col1,col2,col3,col4,col5= st.columns(5)
    with col1:
        st.markdown(f"<h4>Brand Name</h4>",unsafe_allow_html=True)
        data['name'] = data['name'].apply(get_brand_name)
        st.dataframe(data['name'],use_container_width=False)
    with col2:
        st.markdown(f"<h4>Mileage</h4>",unsafe_allow_html=True)
        data['mileage'] = data['mileage'].apply(clean_data)
        st.dataframe(data['mileage'],use_container_width=False)
    with col3:
        st.markdown(f"<h4>Engine Capacity</h4>",unsafe_allow_html=True)
        data['engine'] = data['engine'].apply(clean_data)
        st.dataframe(data['engine'],use_container_width=False)
    with col4:
        st.markdown(f"<h4>Engine Power</h4>",unsafe_allow_html=True)
        data['max_power'] = data['max_power'].apply(clean_data) 
        st.dataframe(data['max_power'],use_container_width=False)
    with col5:
        st.markdown(f"<h4></h4>",unsafe_allow_html=True)
    st.divider()

    st.markdown(f"<h3><i>Categorical Values to Numerical Values: <span style = 'color: #808080';>A➡️1</span></i></h3>",unsafe_allow_html=True)

    col1,col2,col3,col4,col5,col6= st.columns(6)
    with col1:
        st.markdown(f"<h4>Brand Name</h4>",unsafe_allow_html=True)
        st.dataframe(data['name'],use_container_width=False)
    with col2:
        st.markdown(f"<h4></h4>",unsafe_allow_html=True)
        data['name'] = data['name'].replace(['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
                    'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
                    'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
                    'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
                    'Ambassador', 'Ashok', 'Isuzu', 'Opel'],
                    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31])
        st.dataframe(data['name'],use_container_width=False)
    with col3:
        st.markdown(f"<h4>Transmission</h4>",unsafe_allow_html=True)
        st.dataframe(data['transmission'],use_container_width=False)
    with col4:
        st.markdown(f"<h4></h4>",unsafe_allow_html=True)
        data['transmission'] = data['transmission'].replace(['Manual', 'Automatic'],[1,2])
        st.dataframe(data['transmission'],use_container_width=False)
    with col5:
        st.markdown(f"<h4>Seller Type</h4>",unsafe_allow_html=True)
        st.dataframe(data['seller_type'],use_container_width=False)
    with col6:
        st.markdown(f"<h4></h4>",unsafe_allow_html=True)
        data['seller_type'] = data['seller_type'].replace(['Individual', 'Dealer', 'Trustmark Dealer'],[1,2,3])
        st.dataframe(data['seller_type'],use_container_width=False)

    col1,col2,col3,col4,col5 = st.columns(5)
    with col1:
        st.markdown(f"<h4>Fuel Type</h4>",unsafe_allow_html=True)
        st.dataframe(data['fuel'],use_container_width=False)
    with col2:
        st.markdown(f"<h4></h4>",unsafe_allow_html=True)
        data['fuel'] = data['fuel'].replace(['Diesel', 'Petrol', 'LPG', 'CNG'],[1,2,3,4])
        st.dataframe(data['fuel'],use_container_width=False)
    with col3:
        st.markdown(f"<h4>Car Owner</h4>",unsafe_allow_html=True)
        st.dataframe(data['owner'],use_container_width=False)
    with col4:
        st.markdown(f"<h4></h4>",unsafe_allow_html=True)
        data['owner'] = data['owner'].replace(['First Owner', 'Second Owner', 'Third Owner','Fourth & Above Owner', 'Test Drive Car'],[1,2,3,4,5]   )
        st.dataframe(data['owner'],use_container_width=False)
    st.divider()

    st.subheader("***Splitting the Dataset*** ✂️")
    X = data.drop(columns=['selling_price'])
    Y = data['selling_price']
    st.markdown("<h4>X - Features</h4>",unsafe_allow_html=True)
    st.write(X)
    st.markdown("<h4>Y - Target",unsafe_allow_html=True)
    st.dataframe(Y,use_container_width=False)
    st.divider()

    # # Show table
    st.subheader("📊 Model Accuracy Comparison ⇄")
    if not os.path.exists("models.pkl"):
        st.warning( "Models have not been trained yet. " "Please train the models below." )
    else:
        try: 
            with open("models.pkl", "rb") as file: 
                saved_data = pk.load(file)
            if isinstance(saved_data, dict):
                models = saved_data.get("models", {}) 
                model_scores = saved_data.get("metrics", {})
            else:
                 models = {}
                 model_scores = {}
            if not models: 
                st.warning( "No trained models were found in models.pkl." )
            else:
                results = []
                for model_name in models.keys(): 
                    scores = model_scores.get( model_name, {} )
                    results.append({ "Models": model_name, "R² Score": scores.get("r2", 0), "MAE": scores.get("mae", 0), "RMSE": scores.get("rmse", 0) })
                final_data = pd.DataFrame(results)
                st.dataframe(final_data,use_container_width=False)
                st.subheader("📈 R² Score Visualization") 
                fig = px.bar( final_data, x="Models", y="R² Score", color="Models", text="R² Score", width=600, height=500 )
                fig.update_traces( texttemplate="%{text:.4f}", textposition="outside" )
                st.plotly_chart( fig, use_container_width=True )
        except Exception as e: 
            st.error( f"Unable to read model metrics: {e}" )
    st.divider()
    if os.path.exists("models.pkl"):
        st.info("✅ Models are already trained.")
        if st.button( "🔄 Retrain Models", key="retrain_models" ):
            with st.spinner( "Training models... ⏳" ):train_models()
            st.success( "✅ Models retrained successfully!" )
            st.rerun()
    else: 
        if st.button( "🚀 Train & Save Models", key="train_models" ):
            with st.spinner( "Training models... ⏳" ):train_models()
            st.success( "✅ Models trained and saved successfully!" )
            st.balloons()
            st.rerun()

