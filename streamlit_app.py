import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- BRANDING & SETUP ---
# Deep Purple: #8e44ad | Teal/Cyan: #00b5ad | Dark Background: #0e1117
st.set_page_config(page_title="Consultant Lubricant's TCO Calculator", layout="wide")

# --- CUSTOM CSS FOR BRANDING & ANIMATION ---
def apply_custom_styling():
    st.markdown("""
    <style>
    /* Main App Background and Font */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #00b5ad22 100%);
        border-right: 1px solid #00b5ad;
    }

    /* Buttons - Using the Teal from the logo */
    .stButton>button {
        background-color: #00b5ad;
        color: white;
        border-radius: 5px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #8e44ad; /* Swaps to the Purple on hover */
        transform: scale(1.02);
    }

    /* Metric Cards Styling */
    [data-testid="stMetricValue"] {
        color: #00b5ad;
    }

    /* The Press Ram (Overlay) */
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
        background: linear-gradient(to bottom, #161b22, #8e44ad33, #161b22);
        z-index: 9999;
        animation: pressStroke 1.5s cubic-bezier(0.85, 0, 0.15, 1) forwards;
        pointer-events: none;
        border-bottom: 5px solid #00b5ad; 
    }

    @keyframes contentReveal {
        0% { opacity: 0; }
        60% { opacity: 0; }
        100% { opacity: 1; }
    }

    .stApp {
        animation: contentReveal 2.0s ease-in;
    }
    </style>
    <div class="press-overlay"></div>
    """, unsafe_allow_html=True)

# --- SIDEBAR LOGO & LINKS ---
with st.sidebar:
    # Replace 'CLIsyntec WIDE2Main.jpg' with the actual path if hosted, 
    # or ensure it's in the same folder as your script.
    st.image("CLIsyntec WIDE2Main.jpg", use_container_width=True)
    st.markdown("---")
    st.link_button("Request a Sample", "https://surveyhero.com/c/consultantlubricants", use_container_width=True)
    st.link_button("Full Product Catalog", "https://consultantlubricants.com/clisyntec", use_container_width=True)
    st.markdown("---")
    st.info("Sales Tool: Use these inputs to demonstrate the TCO value of CLISYNTEC 3900.")

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

SAVINGS_RATES = {
    "die_coating": 0.30, "dilution": 0.50, "volume": 0.50, "scrap": 0.30,
    "maint_cost": 0.30, "cleaning_time": 0.50, "downtime": 0.20,
    "labor": 0.30, "disposal": 0.30, "unit_cost": 0.10
}

# --- PAGE 1: THE WELCOME MENU ---
if st.session_state.page == 'menu':
    apply_custom_styling()
    st.title("Consultant Lubricant's TCO Calculator")
    st.subheader("Select your process to begin the ROI analysis")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Forming / Stamping Calculator", use_container_width=True):
            st.session_state.page = 'calculator'
            st.rerun()
    with col2:
        if st.button("Subtractive / Machining Calculator", use_container_width=True):
            st.session_state.page = 'calculator' 
            st.rerun()

# --- PAGE 2: THE CALCULATOR ---
elif st.session_state.page == 'calculator':
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

    st.title("Lubricant Cost Comparison")
    st.markdown("Compare existing costs with projected savings from **3900 Stamping Lubricant**.")

    # --- INPUTS ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Core Process Metrics")
        die_coating_costs = st.number_input("Die Coating Costs ($)", value=5000.0)
        lub_volume_annually = st.number_input("Lubricant Volume Annually (gal)", value=1000.0)
        scrap_rate = st.number_input("Scrap Rate (%)", value=5.0)
        cost_per_unit = st.number_input("Cost Per Unit / Blank ($)", value=0.50)

    with col2:
        st.subheader("Maintenance & Labor")
        press_maint_costs = st.number_input("Cost per Press Maintenance ($)", value=2500.0)
        labor_costs = st.number_input("Labor Costs ($)", value=5000.0)
        disposal_costs = st.number_input("Disposal Costs ($)", value=750.0)
        maint_frequency = st.number_input("Annual Maintenance Frequency", value=4)

    # --- CALCULATION ENGINE ---
    curr_maint_annual = press_maint_costs * maint_frequency
    proj_maint_annual = curr_maint_annual * (1 - SAVINGS_RATES["maint_cost"])
    
    savings_total = (die_coating_costs * SAVINGS_RATES["die_coating"]) + \
                    (lub_volume_annually * SAVINGS_RATES["volume"]) + \
                    (labor_costs * SAVINGS_RATES["labor"]) + \
                    (disposal_costs * SAVINGS_RATES["disposal"]) + \
                    (curr_maint_annual - proj_maint_annual)

    # --- OUTPUT DASHBOARD ---
    st.markdown("---")
    st.header("Projected Savings with 3900")
    st.metric("Estimated Total Annual Savings", f"${savings_total:,.2f}")

    # --- CHART WITH LOGO COLORS ---
    st.subheader("12-Month Cumulative Cost Comparison")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    current_annual_total = curr_maint_annual + die_coating_costs + lub_volume_annually + labor_costs + disposal_costs
    projected_annual_total = current_annual_total - savings_total

    fig = go.Figure()
    # Current Costs in Purple
    fig.add_trace(go.Scatter(x=months, y=[(current_annual_total/12)*i for i in range(1,13)], 
                             name="Current Costs", line=dict(color='#8e44ad', width=4)))
    # Projected Costs in Teal
    fig.add_trace(go.Scatter(x=months, y=[(projected_annual_total/12)*i for i in range(1,13)], 
                             name="3900 Projected Costs", line=dict(color='#00b5ad', width=4)))
    
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.caption("PROPRIETARY TOOL: © 2026 Consultant Lubricants, Inc. | CLISYNTEC™ Process Fluids")
