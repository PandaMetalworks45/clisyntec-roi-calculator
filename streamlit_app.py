import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 1. BRANDING & BROWSER SETUP ---
st.set_page_config(
    page_title="Consultant Lubricant's TCO Calculator", 
    page_icon="💧",
    layout="wide"
)

# --- 2. CUSTOM CSS (FORCING BRAND THEME & HIDING FULLSCREEN) ---
def apply_custom_styling():
    st.markdown("""
    <style>
    /* Force Global Dark Background and White Text */
    .stApp {
        background: radial-gradient(circle at top right, #8e44ad15, #0e1117 50%),
                    radial-gradient(circle at bottom left, #00b5ad10, #0e1117 50%);
        color: #ffffff !important;
    }

    /* Target all headers, subheaders, and labels to be white */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stMetricLabel"] {
        color: #ffffff !important;
    }

    /* HIDES THE FULLSCREEN BUTTON ON EVERYTHING (Images and Graphs) */
    button[title="View fullscreen"] {
        display: none !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #00b5ad15 100%);
        border-right: 1px solid #30363d;
    }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #ffffff !important;
    }

    /* Buttons - BLACK TEXT on Teal Background */
    .stButton>button, .stLinkButton>a {
        background-color: #00b5ad !important;
        color: #000000 !important; 
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }
    
    .stButton>button:hover, .stLinkButton>a:hover {
        background-color: #8e44ad !important;
        color: #ffffff !important; 
        box-shadow: 0 4px 15px rgba(142, 68, 173, 0.4) !important;
    }

    /* Input Box Styling */
    div[data-baseweb="input"], [data-testid="stNumberInput"] input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }

    /* Animation Logic */
    @keyframes pressStroke {
        0% { transform: translateY(-100%); }
        40% { transform: translateY(0%); }
        60% { transform: translateY(0%); }
        100% { transform: translateY(-100%); }
    }
    .press-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(to bottom, #161b22, #30363d, #161b22);
        z-index: 9999;
        animation: pressStroke 1.5s cubic-bezier(0.85, 0, 0.15, 1) forwards;
        pointer-events: none;
        border-bottom: 5px solid #00b5ad; 
    }
    .stApp {
        animation: contentReveal 2.2s ease-in;
    }
    @keyframes contentReveal {
        0% { opacity: 0; }
        60% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    <div class="press-overlay"></div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (LARGE LINKED LOGO & CONTACT INFO) ---
with st.sidebar:
    image_path = "CLI_Cap_Label2.jpg"
    
    if os.path.exists(image_path):
        # This converts image to clickable HTML
        img_base64 = get_base64_of_bin_file(image_path)
        
        # WE CREATE AN HTML BUTTON THAT LOOKS LIKE THE IMAGE
        # When clicked, it refreshes the page with the query param 'reset'
        html_code = f'''
            <a href="/?nav=menu" target="_self" style="text-decoration: none;">
                <img src="data:image/jpeg;base64,{img_base64}" style="width: 100%; cursor: pointer;">
            </a>
        '''
        st.markdown(html_code, unsafe_allow_html=True)
        
        # Check if the URL tells us to go home
        params = st.query_params
        if params.get("nav") == "menu":
            st.session_state.page = 'menu'
            # Clear params so it doesn't loop
            st.query_params.clear()
            st.rerun()
    else:
        if st.button("MAIN MENU", use_container_width=True):
            st.session_state.page = 'menu'
            st.rerun()

    st.markdown("---")
    
    st.link_button("Request a Sample", "https://surveyhero.com/c/consultantlubricants", use_container_width=True)
    st.link_button("View Products", "https://consultantlubricants.com/store", use_container_width=True)
    
    st.markdown("---")
    st.caption("Consultant Lubricants, Inc.")
    st.caption("9 Research Park Dr.")
    st.caption("St. Peters, MO 63376")
    st.caption("636.926.9903")

# --- 4. SESSION STATE & DATA ---
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

SAVINGS_RATES = {
    "die_coating": 0.30, "volume": 0.50, "scrap": 0.30,
    "maint_cost": 0.30, "labor": 0.30, "disposal": 0.30
}

# --- 5. PAGE: WELCOME MENU ---
if st.session_state.page == 'menu':
    apply_custom_styling()
    st.title("Consultant Lubricant's TCO Calculator")
    st.write("Select a process below to start the financial comparison.")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("FORMING CALCULATOR", use_container_width=True):
            st.session_state.page = 'calculator'
            st.session_state.calc_type = 'Forming'
            st.rerun()
    with col2:
        if st.button("SUBTRACTIVE CALCULATOR", use_container_width=True):
            st.session_state.page = 'calculator'
            st.session_state.calc_type = 'Subtractive'
            st.rerun()

# --- 6. PAGE: THE CALCULATOR ---
elif st.session_state.page == 'calculator':
    apply_custom_styling() 
    
    # Check which mode we are in
    calc_mode = st.session_state.get('calc_type', 'Forming')
    
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

    st.title(f"{calc_mode} Cost Comparison")
    st.markdown(f"Projected Savings using **Consultant Lubricants Technology**.")

    # --- INPUT SECTION ---
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Process Productivity")
            if calc_mode == 'Subtractive':
                # INDUSTRY: MACHINING
                primary_label = "Annual Tooling / Insert Spend ($)"
                primary_val = st.number_input(primary_label, value=15000.0)
                lub_label = "Annual Coolant Concentrate Spend ($)"
                lub_volume_annually = st.number_input(lub_label, value=8000.0)
                scrap_label = "Annual Part Rejection/Rework Cost ($)"
                scrap_rate_cost = st.number_input(scrap_label, value=5000.0)
            else:
                # INDUSTRY: FORMING/BENDING
                primary_label = "Annual Die Coating Costs ($)"
                primary_val = st.number_input(primary_label, value=5000.0)
                lub_label = "Annual Lubricant Spend ($)"
                lub_volume_annually = st.number_input(lub_label, value=10000.0)
                scrap_label = "Annual Scrap/Defect Cost ($)"
                scrap_rate_cost = st.number_input(scrap_label, value=8000.0)
        
        with col2:
            st.subheader("Maintenance & Labor")
            maint_label = "Cost per Sump Clean-out ($)" if calc_mode == 'Subtractive' else "Cost per Press Clean-out ($)"
            maint_event_cost = st.number_input(maint_label, value=2500.0)
            maint_frequency = st.number_input("Clean-outs Per Year", value=4)
            labor_annual = st.number_input("Total Annual Fluid Labor ($)", value=5000.0)
            disposal_annual = st.number_input("Total Annual Disposal Fees ($)", value=1500.0)

    # --- CALCULATION LOGIC ---
    current_maint = maint_event_cost * maint_frequency
    
    # Dynamic Savings Percentages based on Industry
    if calc_mode == 'Subtractive':
        s_primary = primary_val * 0.25  # 25% Tool Life Improvement
        s_vol = lub_volume_annually * 0.20 # 20% reduced drag-out/stability
        s_maint = current_maint * 0.50     # 50% longer sump life
    else:
        s_primary = primary_val * 0.30  # 30% Die Coating Savings
        s_vol = lub_volume_annually * 0.50 # 50% Volume reduction
        s_maint = current_maint * 0.30     # 30% cleaner operation

    s_scrap = scrap_rate_cost * 0.30
    s_labor = labor_annual * 0.30
    
    total_savings = s_primary + s_vol + s_scrap + s_labor + s_maint

    # --- DASHBOARD OUTPUT ---
    st.markdown("---")
    d1, d2 = st.columns(2)
    d1.markdown(f"""
        <div style="background: rgba(0, 181, 173, 0.1); padding: 25px; border-radius: 12px; border: 2px solid #00b5ad; text-align: center;">
            <p style="color: #ffffff !important; margin: 0; font-weight: bold;">Total Estimated Annual Savings</p>
            <h1 style="color: #00b5ad; margin: 10px 0;">${total_savings:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # ROI based on fluid spend
    roi = (total_savings / (lub_volume_annually if lub_volume_annually > 0 else 1) * 100)

# --- 7. FOOTER ---
st.markdown("---")
st.caption("PROPRIETARY & CONFIDENTIAL: © 2026 Consultant Lubricants, Inc.")
