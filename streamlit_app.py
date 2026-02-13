import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import base64
import numpy as np

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

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
    /* Black text on Teal buttons for high contrast */
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
    }
    div[data-baseweb="input"], [data-testid="stNumberInput"] input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Plotly Config: Remove all clutter, keep PNG export
CHART_CONFIG = {
    'displayModeBar': True,
    'modeBarButtonsToRemove': [
        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 
        'zoomOut2d', 'autoScale2d', 'resetScale2d', 'hoverClosestCartesian', 
        'hoverCompareCartesian', 'toggleSpikelines'
    ],
    'displaylogo': False
}

if 'page' not in st.session_state:
    st.session_state.page = 'menu'

# Sidebar
with st.sidebar:
    image_path = "CLI_Cap_Label2.jpg"
    img_b64 = get_base64_of_bin_file(image_path)
    if img_b64:
        st.markdown(f'<a href="/?nav=menu" target="_self"><img src="data:image/jpeg;base64,{img_b64}" style="width: 100%;"></a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("MAIN MENU", use_container_width=True):
        st.session_state.page = 'menu'
        st.rerun()
    st.link_button("Request a Sample", "https://surveyhero.com/c/consultantlubricants", use_container_width=True)

# Main App Logic
if st.session_state.page == 'menu':
    apply_custom_styling()
    st.markdown("<h1 style='text-align: center;'>Consultant Lubricant's TCO Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🏗️\n\nSTART FORMING CALCULATOR", use_container_width=True):
        st.session_state.page = 'calculator'
        st.rerun()

elif st.session_state.page == 'calculator':
    apply_custom_styling()
    if st.button("← Back"):
        st.session_state.page = 'menu'
        st.rerun()

    st.title("Forming Lubricant TCO Analysis")

    # --- INPUT SECTION ---
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Production Variables")
            die_maint = st.number_input("Annual Die Coating/Polishing ($)", value=10000.0)
            die_changes = st.number_input("Annual Die Changeovers (#)", value=24)
            change_cost = st.number_input("Labor/Downtime per Changeover ($)", value=250.0)
            scrap_rate = st.number_input("Current Scrap Rate (%)", value=4.0) / 100
        with col2:
            st.subheader("Fluid Variables")
            fill_cost = st.number_input("Cost per Sump Fill ($)", value=1200.0)
            fills_per_year = st.number_input("Fills Per Year (#)", value=6, min_value=1)
            monthly_adds = st.number_input("Monthly Additives ($)", value=200.0)
            disposal = st.number_input("Annual Disposal Fees ($)", value=2000.0)

    # --- MATH LOGIC ---
    changeover_total = die_changes * change_cost
    fluid_annual = (fill_cost * fills_per_year) + (monthly_adds * 12) + disposal
    base_cost = die_maint + changeover_total + fluid_annual
    scrap_burden = base_cost * scrap_rate
    current_total = base_cost + scrap_burden

    # CLISYNTEC Projected Savings
    s_maint = die_maint * 0.30
    s_labor = changeover_total * 0.20
    s_fluid = (fill_cost * fills_per_year) * 0.40 
    s_adds = (monthly_adds * 12) * 0.50
    s_scrap = scrap_burden * 0.25
    total_savings = s_maint + s_labor + s_fluid + s_adds + s_scrap
    projected_total = current_total - total_savings

    # --- METRICS ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Annual Burden", f"${current_total:,.0f}")
    m2.metric("Projected Savings", f"${total_savings:,.0f}", delta=f"{(total_savings/current_total)*100:.1f}%")
    m3.metric("Projected ROI", f"{(total_savings/(fluid_annual if fluid_annual > 0 else 1))*100:.0f}%")

    # --- WATERFALL CHART ---
    st.markdown("### Financial Impact Breakdown")
    fig_water = go.Figure(go.Waterfall(
        orientation = "v",
        measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
        x = ["Current Total", "Die Life", "Changeovers", "Fluid/Sump", "Scrap", "Consultant Lubricants"],
        text = [f"${current_total:,.0f}", f"-${s_maint:,.0f}", f"-${s_labor:,.0f}", f"-${s_fluid+s_adds:,.0f}", f"-${s_scrap:,.0f}", f"${projected_total:,.0f}"],
        y = [current_total, -s_maint, -s_labor, -(s_fluid+s_adds), -s_scrap, projected_total],
        connector = {"line":{"color":"#30363d"}},
        increasing = {"marker":{"color":"#00b5ad"}},
        decreasing = {"marker":{"color":"#8e44ad"}},
        totals = {"marker":{"color":"#00b5ad"}}
    ))
    fig_water.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
    st.plotly_chart(fig_water, use_container_width=True, config=CHART_CONFIG)

    # --- COMPARATIVE SECTION ---
    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### Yield: Current vs. Consultant Lubricants")
        curr_yield = (1 - scrap_rate) * 100
        proj_yield = (1 - (scrap_rate * 0.75)) * 100 # Showing 25% scrap reduction
        
        fig_yield = go.Figure(go.Bar(
            x=['Current Process', 'Consultant Lubricants'],
            y=[curr_yield, proj_yield],
            marker_color=['#30363d', '#00b5ad'],
            text=[f"{curr_yield:.1f}%", f"{proj_yield:.1f}%"],
            textposition='auto'
        ))
        fig_yield.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                yaxis=dict(title="Yield (%)", range=[min(curr_yield, proj_yield)-2, 100]))
        st.plotly_chart(fig_yield, use_container_width=True, config=CHART_CONFIG)

    with c2:
        st.markdown("### Maintenance Frequency Reduction")
        m_curr = 12 / fills_per_year
        p_fills = max(1, int(fills_per_year * 0.6))
        m_proj = 12 / p_fills
        
        fig_gantt = go.Figure()
        for i in range(int(fills_per_year)):
            fig_gantt.add_trace(go.Bar(x=[m_curr-0.1], y=["Current"], base=i*m_curr, orientation='h', marker_color='#8e44ad', showlegend=False, text="DUMP", textposition='inside'))
        for i in range(p_fills):
            fig_gantt.add_trace(go.Bar(x=[m_proj-0.1], y=["CLISYNTEC"], base=i*m_proj, orientation='h', marker_color='#00b5ad', showlegend=False, text="STABLE", textposition='inside'))
            
        fig_gantt.update_layout(template="plotly_dark", barmode='stack', xaxis=dict(title="Months"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_gantt, use_container_width=True, config=CHART_CONFIG)

st.markdown("---")
st.caption("Proprietary Financial Modeling | © 2026 Consultant Lubricants, Inc.")
