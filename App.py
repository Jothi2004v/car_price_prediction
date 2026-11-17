import streamlit as st
from streamlit_option_menu import option_menu

import Home
import About
import Prediction


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="wide"
)


# =========================================================
# LOGO
# =========================================================

logo = "car_logo.png"

st.logo(logo)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------
       Move main content slightly upward
    ------------------------------------------------- */

    div.block-container {
        margin-top: -60px;
    }


    /* -------------------------------------------------
       Centered title
    ------------------------------------------------- */

    .centered-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        font-style: italic;
        margin-top: 10px;
    }


    /* -------------------------------------------------
       Sidebar logo positioning
    ------------------------------------------------- */

    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    """
    <h1 class="centered-title">
        CAR PRICE ANALYSIS 🚙
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# SIDEBAR MENU
# =========================================================

with st.sidebar:

    selected_menu = option_menu(
        menu_title=None,

        options=[
            "Home",
            "About",
            "Prediction"
        ],

        icons=[
            "house-fill",
            "exclamation-circle-fill",
            "activity"
        ],

        default_index=0
    )


# =========================================================
# PAGE NAVIGATION
# =========================================================

if selected_menu == "Home":

    Home.show_home()


elif selected_menu == "About":

    About.show_about()


elif selected_menu == "Prediction":

    Prediction.show_predict()
