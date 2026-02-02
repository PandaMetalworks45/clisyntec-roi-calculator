import streamlit as st
import pandas as pd

# --- BRANDING & SETUP ---
st.set_page_config(page_title="CLISYNTEC Master ROI Calculator", layout="wide")
st.title("Consultant Lubricants Master ROI Calculator")
st.markdown("### Integration of Process Physics and Financial Metrics")

# --- SIDEBAR: TECHNICAL CHARACTERISTICS (The Physics) ---
st.sidebar.header("1. Physical Characteristics")
metal_type = st.sidebar.selectbox("Metal Type", ["Carbon Steel", "Stainless Steel", "Aluminum", "High-Strength Steel (AHSS)"])

st.sidebar.subheader("Fluid Properties")
comp_visc = st.sidebar.number_input("Competitor Viscosity (cSt @ 40C)", value=40)
cli_visc = st.sidebar.number_input("CLISYNTEC Viscosity (cSt @ 40C)", value=52)

st.sidebar.header("2. Maintenance & Disposal")
disposal_cost_gal = st.sidebar.number_input("Disposal Cost per Gallon ($)", value=1.50)
die_coating_cost = st.sidebar.number_input("Annual Die Coating Costs ($)", value=2500.0)

# --- MAIN INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Process (Competitor)")
    c_price = st.number_input("Lubricant Price per Gallon ($)", value=18.00, key="c_p")
    c_usage = st.number_input("Annual Lubricant Volume (Gal)", value=5000.0, key="c_u")
    c_scrap = st.number_input("Scrap Rate (%)", value=2.5, key="c_s")
    c_maint_freq = st.number_input("Annual Maintenance Frequency (times/year)", value=12)
    c_downtime_cost = st.number_input("Avg. Downtime Cost per Event ($)", value=1200.0)

with col2:
    st.subheader("Projected Process (CLISYNTEC)")
    p_price = st.number_input("CLISYNTEC Price per Gallon ($)", value=28.00, key="p_p")
    
    # Technical Logic: Better viscosity reduces consumption
    suggested_usage = c_usage * 0.88 if cli_visc > comp_visc else c_usage
    p_usage = st.number_input("Projected Annual Volume (Gal)", value=float(suggested_usage), key="p_u")
    
    p_scrap = st.number_input("Projected Scrap Rate (%)", value=0.5, key="p_s")
    
    # Better lubrication reduces maintenance frequency
    p_maint_freq = st.number_input("Projected Maint. Frequency", value=int(c_maint_freq * 0.5))
    p_downtime_cost = c_downtime_cost # Assuming cost per event stays same, frequency drops

# --- CALCULATION CONSTANTS ---
st.markdown("---")
with st.expander("Process Metrics & Material Costs"):
    blank_cost = st.number_input("Cost Per Unit / Blank ($)", value=3.25)
    annual_production = st.number_input("Total Annual Units Produced", value=1250000)

# --- THE UNIFIED MATH ENGINE ---
def calculate_tco(price, volume, scrap, maint_freq, downtime_val):
    # 1. Direct Fluid Cost
    fluid_total = price * volume
    # 2. Disposal Cost
    disposal_total = volume * disposal_cost_gal
    # 3. Scrap Cost
    scrap_total = annual_production * (scrap/100) * blank_cost
    # 4. Maintenance/Downtime Cost
    maintenance_total = (maint_freq * downtime_val) + die_coating_cost
    
    total_tco = fluid_total + disposal_total + scrap_total + maintenance_total
    return fluid_total, disposal_total, scrap_total, maintenance_total, total_tco

# Run calculations
c_f, c_dis, c_s, c_m, c_total = calculate_tco(c_price, c_usage, c_scrap, c_maint_freq, c_downtime_cost)
p_f, p_dis, p_s, p_m, p_total = calculate_tco(p_price, p_usage, p_scrap, p_maint_freq, p_downtime_cost)

annual_savings = c_total - p_total

# --- OUTPUT DASHBOARD ---
st.header("Financial Impact Summary")
m1, m2, m3 = st.columns(3)
m1.metric("Total Annual Savings", f"${annual_savings:,.2f}")
m2.metric("Maintenance Reduction", f"{int(((c_m - p_m)/c_m)*100)}%")
m3.metric("Fluid ROI", f"{round(annual_savings / p_f, 1)}x")

# Comparison Table
comparison_data = {
    "Expense Category": ["Lubricant Purchase", "Fluid Disposal", "Scrap & Waste", "Maintenance & Die Costs", "Total Process Cost"],
    "Current ($)": [c_f, c_dis, c_s, c_m, c_total],
    "CLISYNTEC ($)": [p_f, p_dis, p_s, p_m, p_total],
    "Savings ($)": [c_f-p_f, c_dis-p_dis, c_s-p_s, c_m-p_m, annual_savings]
}
st.table(pd.DataFrame(comparison_data).style.format({
    "Current ($)": "${:,.2f}", 
    "CLISYNTEC ($)": "${:,.2f}", 
    "Savings ($)": "${:,.2f}"
}))

st.info(f"Technical Analysis: Based on {metal_type} and a viscosity advantage ({cli_visc} vs {comp_visc} cSt), we have modeled a significant reduction in maintenance frequency and disposal volume.")

# --- LEGAL FOOTER ---
st.markdown("---")
st.caption("""
    PROPRIETARY TOOL: © 2026 Consultant Lubricants, Inc. 
    Unauthorized modification, reverse engineering, or diagnosis of 
    internal formulas is strictly prohibited. For visualization purposes only.
""")
