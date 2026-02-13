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
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

# Menu
if st.session_state.page == 'menu':
    apply_custom_styling()
    st.markdown("<h1 style='text-align: center;'>Consultant Lubricant's TCO Calculator</h1>", unsafe_allow_html=True)
    if st.button("🏗️\n\nFORMING CALCULATOR", use_container_width=True):
        st.session_state.page = 'calculator'
        st.rerun()

# Calculator
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

    # --- LOGIC ---
    changeover_total = die_changes * change_cost
    fluid_annual = (fill_cost * fills_per_year) + (monthly_adds * 12) + disposal
    base_cost = die_maint + changeover_total + fluid_annual
    scrap_burden = base_cost * scrap_rate
    current_total = base_cost + scrap_burden

    # Savings Logic
    s_maint = die_maint * 0.30
    s_labor = changeover_total * 0.20
    s_fluid = (fill_cost * fills_per_year) * 0.40 # Reducing fills by 40%
    s_adds = (monthly_adds * 12) * 0.50
    s_scrap = scrap_burden * 0.25
    
    total_savings = s_maint + s_labor + s_fluid + s_adds + s_scrap
    projected_total = current_total - total_savings

    # --- DASHBOARD ---
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Annual Burden", f"${current_total:,.0f}")
    m2.metric("Projected Savings", f"${total_savings:,.0f}", delta=f"{ (total_savings/current_total)*100:.1f}%", delta_color="normal")
    m3.metric("Projected ROI", f"{(total_savings/(fluid_annual if fluid_annual > 0 else 1))*100:.0f}%")

    # --- VISUALIZATIONS ---
    
    # 1. WATERFALL CHART
    st.markdown("### Cost Reduction Breakdown")
    fig_water = go.Figure(go.Waterfall(
        name = "Savings", orientation = "v",
        measure = ["absolute", "relative", "relative", "relative", "relative", "total"],
        x = ["Current Cost", "Die Maint.", "Changeovers", "Fluid/Sump", "Scrap reduction", "New Total"],
        textposition = "outside",
        text = [f"${current_total:,.0f}", f"-${s_maint:,.0f}", f"-${s_labor:,.0f}", f"-${s_fluid+s_adds:,.0f}", f"-${s_scrap:,.0f}", f"${projected_total:,.0f}"],
        y = [current_total, -s_maint, -s_labor, -(s_fluid+s_adds), -s_scrap, projected_total],
        connector = {"line":{"color":"#30363d"}},
        increasing = {"marker":{"color":"#00b5ad"}},
        decreasing = {"marker":{"color":"#8e44ad"}},
        totals = {"marker":{"color":"#00b5ad"}}
    ))
    fig_water.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_water, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        # 2. DONUT CHART (Scrap vs Yield)
        st.markdown("### Process Yield Improvement")
        # Comparing current vs projected yield
        labels = ['Good Parts (Yield)', 'Scrap/Waste']
        # Current
        fig_donut = go.Figure(data=[go.Pie(labels=labels, values=[1-scrap_rate, scrap_rate], hole=.6, marker_colors=['#00b5ad', '#30363d'])])
        fig_donut.update_layout(title_text="Current Process Yield", template="plotly_dark", showlegend=False, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_donut, use_container_width=True)

    with c2:
        # 3. SUMP LIFE GANTT (Stability Timeline)
        st.markdown("### Sump Stability Timeline (12 Months)")
        
        # Calculate months between changes based on user input
        months_between = 12 / fills_per_year
        # We estimate Consultant Lubricants doubles sump life or at least extends it significantly
        projected_fills = max(1, int(fills_per_year * 0.6)) 
        
        fig_gantt = go.Figure()
        
        # Current Process timeline
        for i in range(int(fills_per_year)):
            start = i * months_between
            fig_gantt.add_trace(go.Bar(
                x=[months_between - 0.1], y=["Current Process "],
                base=start, orientation='h', marker_color='#8e44ad', showlegend=False,
                text="Cleanout", textposition='inside'
            ))
            
        # Consultant Lubricants timeline
        proj_months = 12 / projected_fills
        for i in range(projected_fills):
            start = i * proj_months
            fig_gantt.add_trace(go.Bar(
                x=[proj_months - 0.1], y=["Consultant Lubricants "],
                base=start, orientation='h', marker_color='#00b5ad', showlegend=False,
                text="Stable", textposition='inside'
            ))

        fig_gantt.update_layout(
            template="plotly_dark", barmode='stack', 
            xaxis=dict(title="Months", tickvals=list(range(13))),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=300
        )
        st.plotly_chart(fig_gantt, use_container_width=True)

st.markdown("---")
st.caption("Proprietary Financial Modeling | © 2026 Consultant Lubricants, Inc.")
