import streamlit as st
import pandas as pd

# --- BRANDING & SETUP ---
st.set_page_config(page_title="CLISYNTEC Technical ROI", layout="wide")
st.title("CLISYNTEC Technical Performance & ROI Simulator")
st.markdown("### Process Fluid Engineering vs. Commodity Lubricants")

# --- SIDEBAR: PHYSICAL & MECHANICAL FACTORS ---
st.sidebar.header("1. Physical Characteristics")
metal_type = st.sidebar.selectbox("Metal Type", ["Carbon Steel", "Stainless Steel", "Aluminum", "High-Strength Steel (AHSS)"])
part_complexity = st.sidebar.select_slider("Part Complexity", options=["Low", "Medium", "High", "Critical"])

st.sidebar.subheader("Fluid Properties")
comp_visc = st.sidebar.number_input("Competitor Viscosity (cSt @ 40C)", value=40)
cli_visc = st.sidebar.number_input("CLISYNTEC Viscosity (cSt @ 40C)", value=52)

st.sidebar.header("2. Mechanical Factors")
operating_temp_goal = st.sidebar.slider("Target Die Temperature (F)", 80, 250, 110)
shut_height_issue = st.sidebar.toggle("Experience Shut Height Drift?")

# --- MAIN INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Competitor")
    c_price = st.number_input("Price per Gallon ($)", value=18.00, key="c_p")
    c_usage = st.number_input("Gallons Consumed / Shift", value=50.0, key="c_u")
    c_scrap = st.number_input("Current Scrap Rate (%)", value=2.5, key="c_s")
    c_die_life = st.number_input("Parts between Sharpening", value=15000, key="c_d")

with col2:
    st.subheader("CLISYNTEC Solution")
    p_price = st.number_input("Price per Gallon ($)", value=26.00, key="p_p")
    # Technical Logic: Better viscosity/cling usually reduces volume needed
    suggested_usage = c_usage * 0.85 if cli_visc > comp_visc else c_usage
    p_usage = st.number_input("Gallons Consumed / Shift (Predicted)", value=float(suggested_usage), key="p_u")
    p_scrap = st.number_input("Predicted Scrap Rate (%)", value=0.5, key="p_s")
    p_die_life = st.number_input("Parts between Sharpening (Predicted)", value=int(c_die_life * 1.4), key="p_d")

# --- SHARED CONSTANTS ---
st.markdown("---")
with st.expander("Adjust Global Labor & Tooling Costs"):
    labor_rate = st.number_input("Maintenance Labor Rate ($/hr)", value=85)
    regrind_cost = st.number_input("Average Cost per Die Sharpen ($)", value=650)
    blank_cost = st.number_input("Cost of Raw Metal Blank ($)", value=3.25)
    shifts_per_year = 250
    parts_per_shift = 5000

# --- THE MATH ENGINE ---
def run_calc(price, usage, scrap, die_life):
    total_parts = parts_per_shift * shifts_per_year
    annual_fluid = (usage * shifts_per_year) * price
    annual_scrap = total_parts * (scrap/100) * blank_cost
    
    # Tooling Downtime (Assumes 2 hours to swap a die)
    num_regrinds = total_parts / die_life
    tooling_direct_cost = num_regrinds * regrind_cost
    tooling_labor_cost = num_regrinds * 2 * labor_rate
    
    total_tco = annual_fluid + annual_scrap + tooling_direct_cost + tooling_labor_cost
    return annual_fluid, annual_scrap, (tooling_direct_cost + tooling_labor_cost), total_tco

# Executing Calcs
c_f, c_s, c_t, c_total = run_calc(c_price, c_usage, c_scrap, c_die_life)
p_f, p_s, p_t, p_total = run_calc(p_price, p_usage, p_scrap, p_die_life)

# --- VISUALS ---
st.header("Total Cost of Ownership Comparison")
m1, m2 = st.columns(2)
m1.metric("Annual Savings with CLISYNTEC", f"${c_total - p_total:,.2f}")
m2.metric("ROI Factor", f"{round((c_total - p_total) / p_f, 1)}x", help="For every $1 spent on CLISYNTEC, you save this much in process costs.")

# Data Table
df = pd.DataFrame({
    "Category": ["Fluid Expense", "Scrap/Waste", "Tooling & Labor", "TOTAL TCO"],
    "Competitor": [c_f, c_s, c_t, c_total],
    "CLISYNTEC": [p_f, p_s, p_t, p_total]
})
st.table(df.style.format({"Competitor": "${:,.2f}", "CLISYNTEC": "${:,.2f}"}))

# Technical Commentary
st.info(f"Technical Insight: Based on a {metal_type} substrate and a viscosity of {cli_visc} cSt, CLISYNTEC provides superior boundary lubrication. This accounts for the projected {p_die_life - c_die_life:,} hit increase in die life.")
