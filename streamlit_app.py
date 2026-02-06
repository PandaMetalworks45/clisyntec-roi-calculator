import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# --- 1. BRANDING & BROWSER SETUP ---
st.set_page_config(
    page_title="Consultant Lubricant's TCO Calculator", 
    page_icon="💧",
    layout="wide"
)

# --- 2. CUSTOM CSS (STAMPING ANIMATION & BRANDED THEME) ---
def apply_custom_styling():
    st.markdown("""
    <style>
    /* Main App Background and Font */
    .stApp {
        background: radial-gradient(circle at top right, #8e44ad15, #0e1117 50%),
                    radial-gradient(circle at bottom left, #00b5ad10, #0e1117 50%);
        color: #ffffff;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #00b5ad15 100%);
        border-right: 1px solid #30363d;
    }

    /* Buttons - Using the Teal from the logo */
    .stButton>button {
        background-color: #00b5ad;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #8e44ad; /* Swaps to Purple on hover */
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(142, 68, 173, 0.4);
    }

    /* Input Box Styling */
    div[data-baseweb="input"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* Subheader Accent */
    .stSubheader {
        color: #00b5ad !important;
        border-left: 4px solid #8e44ad;
        padding-left: 12px;
    }

    /* The Press Ram (Overlay Animation) */
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

    @keyframes contentReveal {
        0% { opacity: 0; }
        60% { opacity: 0; }
        100% { opacity: 1; }
    }

    .stApp {
        animation: contentReveal 2.2s ease-in;
    }
    </style>
    <div class="press-overlay"></div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (CONSTANT BRANDING) ---
with st.sidebar:
    # Safe Logo Loader
    image_path = "CLIsyntec WIDE2Main.jpg"
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        st.title("CLISYNTEC™")
    
    st.markdown("---")
    st.link_button("Request a Sample", "https://surveyhero.com/c/consultantlubricants", use_container_width=True)
    st.link_button("View Product Line", "https://consultantlubricants.com/clisyntec", use_container_width=True)
    st.markdown("---")
    st.caption("INTERNAL SALES TOOL v2.0")
    st.info("Present this to the prospect to quantify 'Total Cost of Ownership' vs Sticker Price.")

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
    st.write("Welcome back. Select a process below to start the financial comparison.")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("FORMING CALCULATOR", use_container_width=True):
            st.session_state.page = 'calculator'
            st.rerun()
    with col2:
        if st.button("SUBTRACTIVE CALCULATOR", use_container_width=True):
            st.session_state.page = 'calculator' 
            st.rerun()

# --- 6. PAGE: THE CALCULATOR ---
elif st.session_state.page == 'calculator':
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

    st.title("Lubricant Cost Comparison")
    st.markdown("Projected Savings using **CLISYNTEC 3900 Stamping Lubricant**.")

    # --- INPUT SECTION ---
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Core Process Metrics")
            die_coating_costs = st.number_input("Annual Die Coating Costs ($)", value=5000.0)
            lub_volume_annually = st.number_input("Annual Lubricant Spend ($)", value=10000.0)
            scrap_rate_cost = st.number_input("Annual Scrap/Defect Cost ($)", value=8000.0)

        with col2:
            st.subheader("Maintenance & Labor")
            maint_event_cost = st.number_input("Cost per Sump Clean-out ($)", value=2500.0)
            maint_frequency = st.number_input("Clean-outs Per Year", value=4)
            labor_annual = st.number_input("Total Annual Fluid Labor ($)", value=5000.0)
            disposal_annual = st.number_input("Total Annual Disposal Fees ($)", value=1500.0)

    # --- CALCULATION LOGIC ---
    current_maint = maint_event_cost * maint_frequency
    proj_maint = current_maint * (1 - SAVINGS_RATES["maint_cost"])
    
    # Savings Breakdown
    s_die = die_coating_costs * SAVINGS_RATES["die_coating"]
    s_vol = lub_volume_annually * SAVINGS_RATES["volume"]
    s_scrap = scrap_rate_cost * SAVINGS_RATES["scrap"]
    s_labor = labor_annual * SAVINGS_RATES["labor"]
    s_maint = current_maint - proj_maint
    
    total_savings = s_die + s_vol + s_scrap + s_labor + s_maint

    # --- DASHBOARD OUTPUT ---
    st.markdown("---")
    st.header("Financial Impact Analysis")
    
    d1, d2 = st.columns(2)
    d1.markdown(f"""
        <div style="background: rgba(0, 181, 173, 0.1); padding: 25px; border-radius: 12px; border: 2px solid #00b5ad; text-align: center;">
            <h3 style="color: #000000; margin: 0; font-size: 1.2rem;">Total Estimated Annual Savings</h3>
            <h1 style="color: #00b5ad; margin: 10px 0; font-size: 3rem;">${total_savings:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    d2.markdown(f"""
        <div style="background: rgba(142, 68, 173, 0.1); padding: 25px; border-radius: 12px; border: 2px solid #8e44ad; text-align: center;">
            <h3 style="color: #000000; margin: 0; font-size: 1.2rem;">Projected ROI</h3>
            <h1 style="color: #8e44ad; margin: 10px 0; font-size: 3rem;">{ (total_savings / (lub_volume_annually if lub_volume_annually > 0 else 1) * 100):.1f}%</h1>
        </div>
    """, unsafe_allow_html=True)

    # --- VISUALIZATION ---
  # --- VISUALIZATION (CORRECTED) ---
    st.markdown("### Cumulative 12-Month Cost Comparison")
    st.write("The gap between the lines represents your total annual savings.")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Calculate the total annual burden for the current process
    current_annual_burden = (current_maint + die_coating_costs + lub_volume_annually + labor_annual + disposal_annual)
    # The projected burden is the current minus the savings found by the calculator
    projected_annual_burden = current_annual_burden - total_savings

    fig = go.Figure()

    # Current Process (Higher Line = More Expensive)
    fig.add_trace(go.Scatter(
        x=months, 
        y=[(current_annual_burden/12)*i for i in range(1,13)], 
        name="Current Process (Higher Cost)", 
        line=dict(color='#8e44ad', width=4, dash='dot')
    ))

    # CLISYNTEC Process (Lower Line = Cost Savings)
    fig.add_trace(go.Scatter(
        x=months, 
        y=[(projected_annual_burden/12)*i for i in range(1,13)], 
        name="CLISYNTEC 3900 (Lower Cost)", 
        line=dict(color='#00b5ad', width=5),
        fill='tonexty', # This shades the area between the lines
        fillcolor='rgba(0, 181, 173, 0.1)' 
    ))
    
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title="Cumulative Spend ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 7. FOOTER ---
st.markdown("---")
st.caption("PROPRIETARY & CONFIDENTIAL: © 2026 Consultant Lubricants, Inc. | All Formulas Synced to V3900-Audit.")
