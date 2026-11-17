import streamlit as st
import pandas as pd


def show_home():

    # =========================================================
    # PAGE TITLE
    # =========================================================

    st.subheader("💾Upload the dataset")

    # =========================================================
    # INITIALIZE SESSION STATE
    # =========================================================

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if "uploaded_df" not in st.session_state:
        st.session_state.uploaded_df = None

    if "uploaded_filename" not in st.session_state:
        st.session_state.uploaded_filename = None

    # =========================================================
    # UPLOAD DATASET
    # =========================================================

    with st.expander("Upload the DataSet", expanded=True):

        file = st.file_uploader(
            "📂 Upload your file (Excel)",
            type=["xlsx"],
            key="dataset_uploader"
        )

        st.markdown(
            """
            <style>
            div.block-container {
                padding-top: 7em;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

    # =========================================================
    # NEW FILE UPLOADED
    # =========================================================

    if file is not None:

        # Save uploaded file
        st.session_state.uploaded_file = file

        # Save file name
        st.session_state.uploaded_filename = file.name

        # Read Excel file
        with st.spinner("File Uploading... ⏳"):

            df = pd.read_excel(file)

        # Save DataFrame in session state
        st.session_state.uploaded_df = df

    # =========================================================
    # CHECK IF DATASET ALREADY EXISTS
    # =========================================================

    if st.session_state.uploaded_df is None:

        st.info(
            "⚠︎ Please upload an Excel (.xlsx) file to continue."
        )

        return

    # =========================================================
    # LOAD SAVED DATASET
    # =========================================================

    df = st.session_state.uploaded_df

    # =========================================================
    # FILE INFORMATION
    # =========================================================

    st.success("✅ Dataset loaded successfully.")

    st.write(
        "**Uploaded file name:**",
        st.session_state.uploaded_filename
    )

    st.divider()

    # =========================================================
    # DISPLAY DATASET
    # =========================================================

    st.subheader("***Data set***📄")

    st.write(df.head(8))

    st.divider()

    # =========================================================
    # DATA EXPLANATION
    # =========================================================

    st.markdown(
        """
        <h1 style='text-align: center;'>
        Data Explanation 📝
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <ul style='list-style-type: square; font-size:20px;'>

        <li>
        <b><i>Name -</i></b> car brand and model name.
        </li>

        <li>
        <b><i>Year -</i></b> manufactured Year.
        </li>

        <li>
        <b><i>Selling Price -</i></b> price of the Car.
        </li>

        <li>
        <b><i>Km_driven -</i></b> kilometers driven.
        </li>

        <li>
        <b><i>Fuel -</i></b> type of fuel.

            <ul style='list-style-type: circle;'>
                <li>Petrol</li>
                <li>Diesel</li>
            </ul>

        </li>

        <li>
        <b><i>Seller -</i></b> type of seller.

            <ul style='list-style-type: circle;'>
                <li>Individual</li>
                <li>Dealer</li>
            </ul>

        </li>

        <li>
        <b><i>Transmission -</i></b> type of transmission.

            <ul style='list-style-type: circle;'>
                <li>Manual</li>
                <li>Automatic</li>
            </ul>

        </li>

        <li>
        <b><i>Owner -</i></b> type of owner.

            <ul style='list-style-type: circle;'>
                <li>First Owner</li>
                <li>Second Owner</li>
                <li>Third Owner and so on.</li>
            </ul>

        </li>

        <li>
        <b><i>Mileage -</i></b> car mileage.
        </li>

        <li>
        <b><i>Engine -</i></b> engine capacity.
        </li>

        <li>
        <b><i>Max Power -</i></b> car bhp (brake horsepower).
        </li>

        <li>
        <b><i>Torque -</i></b> twisting or rotational force.
        </li>

        <li>
        <b><i>Seats -</i></b> number of persons who can sit.

            <ul style='list-style-type: circle;'>
                <li>Five seats</li>
                <li>Seven seats and so on.</li>
            </ul>

        </li>

        </ul>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================================================
    # DATA SHAPE
    # =========================================================

    st.markdown(
        """
        <h1 style='text-align: center;'>
        Data Shape
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h4 style='font-style: italic;'>
        Number of Rows:
        <span style='color:#808080;'>
        {df.shape[0]}
        </span>
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h4 style='font-style: italic;'>
        Number of Columns:
        <span style='color:#808080;'>
        {df.shape[1]}
        </span>
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================================================
    # DATASET INFORMATION
    # =========================================================

    st.markdown(
        """
        <h1 style='text-align: center;'>
        Dataset Information 📋
        </h1>
        """,
        unsafe_allow_html=True
    )

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Non-null Count": df.count().values,
        "Data Type": df.dtypes.astype(str).values
    })

    st.dataframe(
        info_df,
        use_container_width=False
    )

    st.divider()

    # =========================================================
    # DATA CLEANING
    # =========================================================

    st.markdown(
        """
        <h1 style='text-align: center;'>
        Data Cleaning 🧼
        </h1>
        """,
        unsafe_allow_html=True
    )

    # =========================================================
    # FIND DUPLICATES
    # =========================================================

    duplicates = df[df.duplicated()]

    st.subheader("Duplicate Rows searching...🔍")

    if duplicates.empty:

        st.success(
            "No duplicate rows found ✅"
        )

    else:

        st.error(
            "***Duplicate Rows Found ❌***"
        )

    # =========================================================
    # ROW COUNTS
    # =========================================================

    total_rows = len(df)

    duplicate_rows = df.duplicated().sum()

    unique_rows = df.drop_duplicates().shape[0]

    col1, col2, col3 = st.columns(3)

    # Total Rows
    col1.markdown(
        f"""
        <div style="
            background-color:#0096FF;
            padding:10px;
            border-radius:10px;
            text-align:center
        ">

        <h3 style="color:white;">
        Total Rows
        </h3>

        <h1 style="color:white;">
        {total_rows}
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )

    # Duplicate Rows
    col2.markdown(
        f"""
        <div style="
            background-color:#FF2800;
            padding:10px;
            border-radius:10px;
            text-align:center
        ">

        <h3 style="color:white;">
        Duplicate Rows
        </h3>

        <h1 style="color:white;">
        {duplicate_rows}
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )

    # Unique Rows
    col3.markdown(
        f"""
        <div style="
            background-color:#00A86B;
            padding:10px;
            border-radius:10px;
            text-align:center
        ">

        <h3 style="color:white;">
        Unique Rows
        </h3>

        <h1 style="color:white;">
        {unique_rows}
        </h1>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================================================
    # TOTAL DUPLICATE ROWS
    # =========================================================

    st.markdown(
        f"""
        <h4 style='font-style: italic;'>

        Total Duplicate Rows:

        <span style='color:#808080;'>
        {duplicates.shape[0]}
        </span>

        </h4>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        duplicates,
        use_container_width=True
    )

    st.divider()

    # =========================================================
    # REMOVE DUPLICATES
    # =========================================================

    df_cleaned = df.drop_duplicates()

    st.subheader(
        "🧹 After Removing Duplicates"
    )

    st.markdown(
        f"""
        <h4 style='font-style: italic;'>

        Original Rows:

        <span style='color:#808080;'>
        {df.shape[0]}
        </span>

        </h4>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h4 style='font-style: italic;'>

        Cleaned Rows:

        <span style='color:#808080;'>
        {df_cleaned.shape[0]}
        </span>

        </h4>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "***No duplicate rows found ✅***"
    )

    st.dataframe(
        df_cleaned,
        use_container_width=True
    )

    st.divider()

    # =========================================================
    # CHECK NULL VALUES
    # =========================================================

    st.subheader(
        "🧹 Checking Null Values"
    )

    col1, col2, col3 = st.columns(3)

    # ---------------------------------------------------------
    # BEFORE REMOVING NULL VALUES
    # ---------------------------------------------------------

    with col1:

        st.markdown(
            "<h4>Before Removing Null Values</h4>",
            unsafe_allow_html=True
        )

        st.dataframe(
            df_cleaned.isnull().sum(),
            use_container_width=False
        )

    # ---------------------------------------------------------
    # REMOVE NULL VALUES
    # ---------------------------------------------------------

    null_before = df_cleaned.shape[0]

    df_cleaned = df_cleaned.dropna()

    null_after = df_cleaned.shape[0]

    null_rows_removed = null_before - null_after

    # ---------------------------------------------------------
    # AFTER REMOVING NULL VALUES
    # ---------------------------------------------------------

    with col2:

        st.markdown(
            "<h4>After Removing Null Values</h4>",
            unsafe_allow_html=True
        )

        st.dataframe(
            df_cleaned.isnull().sum(),
            use_container_width=False
        )

    # ---------------------------------------------------------
    # NULL ROWS REMOVED
    # ---------------------------------------------------------

    with col3:

        st.markdown(
            "<h4>Null Rows Removed</h4>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <h3 style='color:#808080;'>
            {null_rows_removed}
            </h3>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # =========================================================
    # CLEANED DATA SHAPE
    # =========================================================

    st.subheader(
        "🧹 Data Shape"
    )

    st.markdown(
        f"""
        <h5 style='font-style: italic;'>

        Number of Rows:

        <span style='color:#808080;'>
        {df_cleaned.shape[0]}
        </span>

        </h5>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <h5 style='font-style: italic;'>

        Number of Columns:

        <span style='color:#808080;'>
        {df_cleaned.shape[1]}
        </span>

        </h5>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # =========================================================
    # DOWNLOAD CLEANED DATA
    # =========================================================

    st.download_button(
        label="⬇️ Download Cleaned Data",
        data=df_cleaned.to_csv(index=False),
        file_name="Car_details.csv",
        mime="text/csv",
        key="download_cleaned_data"
    )

    st.divider()


# =============================================================
# BRAND NAME FUNCTION
# =============================================================

def get_brand_name(car_name):

    car_name = str(car_name)

    car_name = car_name.split(" ")[0]

    return car_name.strip()
