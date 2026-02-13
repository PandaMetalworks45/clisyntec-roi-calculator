import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
import numpy as np

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Branding and Browser
st.set_page_config(
    page_title="Consultant Lubricant's TCO Calculator", 
    page_icon="💧",
    layout="wide"
)

# Custom CSS
def apply_custom_styling():
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #8e44ad15, #0e1117 50%),
                    radial-gradient(circle at bottom left, #00b5ad10, #0e1117 50%);
        color: #ffffff !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    /* Input Box Styling */
    div[data-baseweb="input"], [data-testid="stNumberInput"] input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    image_path = "CLI_Cap_Label2.jpg"
    if os.path.exists(image_path):
        img_base64 = get_base64_of_bin_file(image_path)
        st.markdown(f'<a href="/?nav=menu" target="_self"><img src="data:image/jpeg;base64,{img_base64}" style="width: 100%;"></a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("MAIN MENU", use_container_width=True):
        st.session_state.page = 'menu'
        st.rerun()
    st.link_button("Request a Sample", "https://surveyhero.com/c/consultantlubricants", use_container_width=True)

# Session State
