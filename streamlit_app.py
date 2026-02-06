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
    
    if 'calc_type' not in st.session_state:
        st.session_state.calc_type = 'Forming'
    
    calc_mode = st.session_state.calc_type
    
    if st.button("← Back to Menu"):
        st.session_state.page = 'menu'
        st.rerun()

    st.title(f"{calc_mode} Lubricant Cost Comparison")
    st.markdown(f"Projected Savings using **Consultant Lubricants Technology**.")

    # --- INPUT SECTION ---
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Process Productivity")
            if calc_mode == 'Subtractive':
                avg_tool_cost = st.number_input("Average Tool Replacement Cost ($)", value=30.0, key="sub_tool_avg")
                tool_changes = st.number_input("Annual Tool Changes (#)", value=500, key="sub_t_changes")
                
                # Hidden Calculation for Tooling
                primary_val = avg_tool_cost * tool_changes
                st.caption(f"Calculated Annual Tool Spend: **${primary_val:,.2f}**")
                
                cost_per_change = st.number_input("Labor/Downtime per Change ($)", value=25.0, key="sub_t_cost")
                
                # NEW: Scrap Rate as a Percentage
                scrap_rate_pct = st.number_input("Current Scrap Rate (%)", value=5.0, step=0.1, key="sub_scrap_pct") / 100
            else:
                primary_val = st.number_input("Annual Die Coating Costs ($)", value=5000.0, key="form_die")
                scrap_rate_pct = st.number_input("Current Scrap Rate (%)", value=3.0, step=0.1, key="form_scrap_pct") / 100
        
        with col2:
            st.subheader("Maintenance & Fluid Costs")
            # NEW: Sump Fill terminology
            fill_label = "Cost per Sump Fill ($)" if calc_mode == 'Subtractive' else "Cost per Press Fill ($)"
            fill_cost = st.number_input(fill_label, value=1200.0, key="fill_cost_in")
            fill_frequency = st.number_input("Sump Fills Per Year", value=4, key="fill_freq_in")
            
            # NEW: Monthly Additives (Converted to annual)
            monthly_additives = st.number_input("Average Monthly Tankside Additives Cost ($)", value=150.0, key="adds_in")
            annual_additives = monthly_additives * 12
            
            disposal_annual = st.number_input("Total Annual Disposal Fees ($)", value=1500.0, key="disp_in")

    # --- CALCULATION LOGIC ---
    current_fills_total = fill_cost * fill_frequency
    
    # Base costs before scrap impact
    if calc_mode == 'Subtractive':
        base_annual_cost = primary_val + (tool_changes * cost_per_change) + current_fills_total + annual_additives + disposal_annual
    else:
        base_annual_cost = primary_val + current_fills_total + annual_additives + disposal_annual

    # NEW: Apply Scrap Rate to the total cost of ownership
    # This represents the financial burden of the scrap relative to the process spend
    scrap_burden = base_annual_cost * scrap_rate_pct
    current_annual_burden = base_annual_cost + scrap_burden

    # Consultant Lubricants Savings Logic
    if calc_mode == 'Subtractive':
        s_tooling = primary_val * 0.25      # 25% Tool Life
        s_tool_labor = (tool_changes * cost_per_change) * 0.25 
        s_fills = current_fills_total * 0.50  # 50% fewer fills (longer life)
        s_additives = annual_additives * 0.80 # 80% reduction in "band-aid" additives
        s_scrap = scrap_burden * 0.30        # 30% reduction in scrap
        
        total_savings = s_tooling + s_tool_labor + s_fills + s_additives + s_scrap
    else:
        s_fills = current_fills_total * 0.40 
        s_additives = annual_additives * 0.70
        s_scrap = scrap_burden * 0.20
        total_savings = (primary_val * 0.30) + s_fills + s_additives + s_scrap

    # --- DASHBOARD OUTPUT ---
    st.markdown("---")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"""
            <div style="background: rgba(0, 181, 173, 0.1); padding: 25px; border-radius: 12px; border: 2px solid #00b5ad; text-align: center;">
                <p style="color: #ffffff !important; margin: 0; font-weight: bold;">Total Estimated Annual Savings</p>
                <h1 style="color: #00b5ad; margin: 10px 0;">${total_savings:,.2f}</h1>
            </div>
        """, unsafe_allow_html=True)
    
    with d2:
        # ROI calculated against the "Fluid & Additive" spend
        fluid_investment = current_fills_total + annual_additives
        roi = (total_savings / (fluid_investment if fluid_investment > 0 else 1) * 100)
        st.markdown(f"""
            <div style="background: rgba(142, 68, 173, 0.1); padding: 25px; border-radius: 12px; border: 2px solid #8e44ad; text-align: center;">
                <p style="color: #ffffff !important; margin: 0; font-weight: bold;">Projected ROI</p>
                <h1 style="color: #8e44ad; margin: 10px 0;">{roi:.1f}%</h1>
            </div>
        """, unsafe_allow_html=True)

    # --- THE GRAPH SECTION ---
    st.markdown("### Cumulative 12-Month Cost Comparison")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    projected_annual_burden = current_annual_burden - total_savings

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=[(current_annual_burden/12)*i for i in range(1,13)], 
                             name="Current Process (incl. Scrap)", line=dict(color='#8e44ad', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=months, y=[(projected_annual_burden/12)*i for i in range(1,13)], 
                             name="Consultant Lubricants", line=dict(color='#00b5ad', width=5), 
                             fill='tonexty', fillcolor='rgba(0, 181, 173, 0.1)'))
    
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=450, margin=dict(l=20, r=20, t=50, b=20), font=dict(color="#ffffff"),
        yaxis=dict(tickfont=dict(color="#ffffff"), title="Cumulative Spend ($)", showgrid=True, gridcolor="#30363d"),
        xaxis=dict(tickfont=dict(color="#ffffff"), showgrid=False),
        legend=dict(font=dict(color="#ffffff"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 7. FOOTER ---
st.markdown("---")
st.caption("Consultant Lubricants, Inc. | 9 Research Park Dr, St. Peters, MO 63376 | 636-926-9903")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("PROPRIETARY & CONFIDENTIAL: © 2026 Consultant Lubricants, Inc.")
