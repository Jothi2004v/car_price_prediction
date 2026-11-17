import streamlit as st
import pandas as pd

def show_home():
    st.subheader("💾Upload the dataset")

    if "uploaded_file" not in st.session_state: 
        st.session_state.uploaded_file = None

    with st.expander("Upload the DataSet"):
        file = st.file_uploader("📂 Upload your file (Excel)", type=["xlsx"],key="dataset_uploader")
        st.markdown("<style>div.block-container{padding-top:7em;}</style>", unsafe_allow_html=True)

    if file is not None:
        st.session_state.uploaded_file = file
    else:
        st.session_state.uploaded_file = None
        st.info("⚠︎ Please upload an Excel (.xlsx) file to continue." )

    if st.session_state.uploaded_file is not None:
        with st.spinner("File Uploading... ⏳"):df = pd.read_excel(st.session_state.uploaded_file)
        
        st.write("**Uploaded file name:**", st.session_state.uploaded_file.name)
        st.divider()

        #displaying the dataset
        st.subheader("***Data set***📄")
        st.write(df.head(8))
        st.divider()

        st.markdown("***<h1 style='text-align: center;'>Data Explanation📝</h1>***", unsafe_allow_html=True)
        st.markdown("<ul style='list-style-type: square; font-size:20px;'>"
        "<li><b><i>Name -</i></b> car brand and model name.</li>"
         "<li><b><i>Year -</i></b> manufactured Year.</li>"
        "<li><b><i>Selling Price -</i></b> price of the Car.</li>"
        "<li><b><i>Km_driven -</i></b> kilometers driven.</li>"
        "<li><b><i>Fuel -</i></b> type of fuel."
        "<ul style='list-style-type: circle;'>"
            "<li>Petrol</li>"
            "<li>Diesel</li>"
        "</ul>""</li>"

        "<li><b><i>Seller -</i></b> type of seller."
            "<ul style='list-style-type: circle;'>"
                "<li>Individual</li>"
                "<li>Dealer</li>"
            "</ul>""</li>"

        "<li><b><i>Transmission -</i></b> type of transmission."
            "<ul style='list-style-type: circle;'>"
                "<li>Manual</li>"
                "<li>Automatic</li>"
            "</ul>""</li>"

        "<li><b><i>Owner -</i></b> type of owner."
            "<ul style='list-style-type: circle;'>"
                "<li>First Owner</li>"
                "<li>Second Owner</li>"
                "<li>Third Owner and so on.</li>"
            "</ul>""</li>"

        "<li><b><i>Mileage -</i></b> car mileage.</li>"
        "<li><b><i>Engine -</i></b> engine capacity.</li>"
        "<li><b><i>Max Power -</i></b> car bhp (brake horsepower).</li>"
        "<li><b><i>Torque -</i></b> twisting or rotational force.</li>"
        "<li><b><i>Seats -</i></b> number of persons who can sit."
            "<ul style='list-style-type: circle;'>"
                "<li>Five seats</li>"
                "<li>Seven seats and so on.</li>"
            "</ul>""</li>"
        "</ul>",unsafe_allow_html=True)
        st.divider()

        st.markdown("***<h1 style='text-align: center;'>Data Shape</h1>***", unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic;'>Number of Rows: <span style = 'color: #808080';>{df.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic;'>Number of Columns:  <span style = 'color: #808080';>{df.shape[1]}</span></h4>",unsafe_allow_html=True)
        st.divider()

        st.markdown("***<h1 style='text-align: center;'>Dataset Information📋</h1>***", unsafe_allow_html=True)
        info_df = pd.DataFrame({
            "Column": df.columns,
            "Non-null Count": df.count().values,
            "Data Type": df.dtypes.values
        })
        st.dataframe(info_df,use_container_width=False)
        st.divider()

        #Data Cleaning
        st.markdown("***<h1 style='text-align: center;'>Data Cleaning🧼</h1>***", unsafe_allow_html=True)
        duplicates = df[df.duplicated()]
        st.subheader("Duplicate Rows searching...🔍 ")
        if duplicates.empty:
            st.success("No duplicate rows found ✅")
        else:
            st.error("***Duplicate Rows Found ❌*** ")

        total_rows = len(df)
        duplicate_rows = df.duplicated().sum()
        unique_rows = df.drop_duplicates().shape[0]
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div style="background-color:#0096FF;padding:10px;border-radius:10px;text-align:center">
            <h3 style="color:white;">Total Rows</h3>
            <h1 style="color:white;">{total_rows}</h1>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div style="background-color:#FF2800;padding:10px;border-radius:10px;text-align:center">
            <h3 style="color:white;">Duplicate Rows</h3>
            <h1 style="color:white;">{duplicate_rows}</h1>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div style="background-color:#00A86B;padding:10px;border-radius:10px;text-align:center">
            <h3 style="color:white;">Unique Rows</h3>
            <h1 style="color:white;">{unique_rows}</h1>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic;'>Total Duplicate Rows:  <span style = 'color: #808080';>{duplicates.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.dataframe(duplicates, use_container_width=True)
        st.divider()

        #removed duplicates
        df_cleaned = df.drop_duplicates()
        st.subheader("🧹 After Removing Duplicates")
        st.markdown(f"<h4 style='font-style: italic;'>Original Rows:  <span style = 'color: #808080';>{df.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.markdown(f"<h4 style='font-style: italic';>Cleaned Rows:  <span style = 'color: #808080';>{df_cleaned.shape[0]}</span></h4>",unsafe_allow_html=True)
        st.success("***No duplicate rows found ✅***")
        st.dataframe(df_cleaned, use_container_width=True)
        st.divider()

        st.subheader("🧹Checking Null Values")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.markdown("<h4>Columns</h4>",unsafe_allow_html=True)
            st.dataframe(df_cleaned.isnull().sum(),use_container_width=False)
        with col2:
            df_cleaned = df_cleaned.dropna()
            st.markdown("<h4>Columns</h4>",unsafe_allow_html=True)

            st.dataframe(df_cleaned.isnull().sum(),use_container_width=False)

        st.divider()
        st.subheader("🧹Data Shape")
        st.markdown(f"<h5 style='font-style: italic;'>Number of Rows: <span style = 'color: #808080';>{df_cleaned.shape[0]}</span></h5>",unsafe_allow_html=True)
        st.markdown(f"<h5 style='font-style: italic;'>Number of Columns:  <span style = 'color: #808080';>{df_cleaned.shape[1]}</span></h5>",unsafe_allow_html=True)


        #download the data
        st.download_button(
        label="⬇️ Download Cleaned Data",
        data=df_cleaned.to_csv(index=False),
        file_name="Car_details.csv",
        mime="text/csv"
        )
        st.divider()

        def get_brand_name(car_name):
            car_name = car_name.split(' ')[0]
            return car_name.strip()



