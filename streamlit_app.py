import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- BRANDING & SETUP ---
st.set_page_config(page_title="CLISYNTEC Master ROI Calculator", layout="wide")
st.link_button("Request a Sample", "https://surveyhero.com/c/consultantlubricants", use_container_width=True)

# --- Animation CSS ---
st.markdown("""
<style> 
.stApp{animation: fadeIn 1.0s ease-in;}
@keyframes fadeIn {
    0%{opacity: 0; transform: translateY(10px);}
    100%{opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

# --- WEBSITE CONSTANTS (From HTML Script) ---
SAVINGS_RATES = {
    "die_coating": 0.30,
    "dilution": 0.50,
    "volume": 0.50,
    "scrap": 0.30,
    "maint_cost": 0.30,
    "cleaning_time": 0.50,
    "downtime": 0.20,
    "labor": 0.30,
    "disposal": 0.30,
    "unit_cost": 0.10
}

# --- PAGE 1: THE WELCOME MENU ---
if st.session_state.page == 'menu':
    st.title("Welcome to CLISYNTEC'S TCO Calculator!")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Forming Calculator", use_container_width=True):
            st.session_state.page = 'calculator'
            st.rerun()
    with col2:
        if st.button("Subtracting Calculator", use_container_width=True):
            st.session_state.page = 'calculator' 
            st.rerun()
    with col3:
        st.link_button("View All Products", "https://consultantlubricants.com/clisyntec", use_container_width=True)

# --- PAGE 2: THE CALCULATOR (Synced with HTML) ---
elif st.session_state.page == 'calculator':
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

    st.title("Lubricant Cost Comparison")
    st.markdown("Compare existing costs with projected savings from **3900 Stamping Lubricant**.")

    # --- INPUTS (Matched to HTML IDs) ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Core Process Metrics")
        die_coating_costs = st.number_input("Die Coating Costs ($)", value=5000.0)
        lub_volume_annually = st.number_input("Lubricant Volume Annually (gal)", value=1000.0)
        dilution_input = st.text_input("Dilution at Press (X:Y)", value="4:1")
        scrap_rate = st.number_input("Scrap Rate (%)", value=5.0)
        cost_per_unit = st.number_input("Cost Per Unit / Blank ($)", value=0.50)

    with col2:
        st.subheader("Maintenance & Labor")
        press_maint_costs = st.number_input("Cost per Press Maintenance ($)", value=2500.0)
        labor_costs = st.number_input("Labor Costs ($)", value=5000.0)
        cleaning_time_per = st.number_input("Time per Cleaning (hrs)", value=150.0)
        downtime_per = st.number_input("Avg. Downtime per Maintenance (hrs)", value=80.0)
        disposal_costs = st.number_input("Disposal Costs ($)", value=750.0)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Time-Related Metrics")
        annual_cleanings = st.number_input("Annual Cleanings (times/year)", value=10)
        maint_frequency = st.number_input("Annual Maintenance Frequency (times/year)", value=4)

    # --- CALCULATION ENGINE (Forming Calculator Section) ---
    
    # 1. Monetary Calculations
    curr_maint_annual = press_maint_costs * maint_frequency
    proj_maint_annual = curr_maint_annual * (1 - SAVINGS_RATES["maint_cost"])
    
    # Savings breakdown
    savings_die = die_coating_costs * SAVINGS_RATES["die_coating"]
    savings_vol = lub_volume_annually * SAVINGS_RATES["volume"] # Note: website treats volume as a direct monetary save in your JS logic
    savings_labor = labor_costs * SAVINGS_RATES["labor"]
    savings_disposal = disposal_costs * SAVINGS_RATES["disposal"]
    savings_unit = cost_per_unit * SAVINGS_RATES["unit_cost"]
    savings_maint = curr_maint_annual - proj_maint_annual

    total_monetary_savings = savings_die + savings_vol + savings_labor + savings_disposal + savings_unit + savings_maint

    # 2. Time Calculations
    curr_cleaning_hrs = cleaning_time_per * annual_cleanings
    proj_cleaning_hrs = curr_cleaning_hrs * (1 - SAVINGS_RATES["cleaning_time"])
    
    curr_downtime_hrs = downtime_per * maint_frequency
    proj_downtime_hrs = curr_downtime_hrs * (1 - SAVINGS_RATES["downtime"])

    total_time_savings = (curr_cleaning_hrs - proj_cleaning_hrs) + (curr_downtime_hrs - proj_downtime_hrs)

    # --- OUTPUT DASHBOARD ---
    st.header("Projected Savings with 3900")
    res1, res2 = st.columns(2)
    res1.metric("Estimated Total Annual Savings", f"${total_monetary_savings:,.2f}", delta_color="normal")
    res2.metric("Estimated Total Time Savings", f"{total_time_savings:,.1f} hrs", delta_color="normal")

    # Comparison Table
    comparison_data = {
        "Metric": ["Press Maintenance (Annual)", "Die Coating", "Lubricant Volume (Value)", "Labor Costs", "Disposal Costs", "Scrap Rate (%)"],
        "Current": [curr_maint_annual, die_coating_costs, lub_volume_annually, labor_costs, disposal_costs, scrap_rate],
        "With 3900": [proj_maint_annual, die_coating_costs * 0.7, lub_volume_annually * 0.5, labor_costs * 0.7, disposal_costs * 0.7, scrap_rate * 0.7],
        "Total Savings": [savings_maint, savings_die, savings_vol, savings_labor, savings_disposal, "30% Reduction"]
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)

    # --- TCO VISUALIZATION ---
    st.subheader("12-Month Cumulative Cost Comparison")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Totals for plotting
    current_annual_total = curr_maint_annual + die_coating_costs + lub_volume_annually + labor_costs + disposal_costs
    projected_annual_total = current_annual_total - total_monetary_savings

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=[(current_annual_total/12)*i for i in range(1,13)], name="Current Costs", line=dict(color='#FF4B4B')))
    fig.add_trace(go.Scatter(x=months, y=[(projected_annual_total/12)*i for i in range(1,13)], name="3900 Projected Costs", line=dict(color='#00CC96')))
    st.plotly_chart(fig, use_container_width=True)

# --- SHARED PROPRIETARY FOOTER ---
st.markdown("---")
st.caption("PROPRIETARY TOOL: © 2026 Consultant Lubricants, Inc. Internal formulas synced with Web-Forming Calculator 3900-v1.")
