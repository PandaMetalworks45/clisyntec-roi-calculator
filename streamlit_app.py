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
    
    # Safety check for calc_type
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
                primary_val = st.number_input("Annual Tooling / Insert Spend ($)", value=15000.0, key="sub_tool")
                lub_volume_annually = st.number_input("Annual Coolant Concentrate Spend ($)", value=8000.0, key="sub_lub")
                scrap_rate_cost = st.number_input("Annual Part Rejection/Rework Cost ($)", value=5000.0, key="sub_scrap")
            else:
                primary_val = st.number_input("Annual Die Coating Costs ($)", value=5000.0, key="form_die")
                lub_volume_annually = st.number_input("Annual Lubricant Spend ($)", value=10000.0, key="form_lub")
                scrap_rate_cost = st.number_input("Annual Scrap/Defect Cost ($)", value=8000.0, key="form_scrap")
        
        with col2:
            st.subheader("Maintenance & Labor")
            maint_label = "Cost per Sump Clean-out ($)" if calc_mode == 'Subtractive' else "Cost per Press Clean-out ($)"
            maint_event_cost = st.number_input(maint_label, value=2500.0, key="maint_cost_in")
            maint_frequency = st.number_input("Clean-outs Per Year", value=4, key="maint_freq_in")
            labor_annual = st.number_input("Total Annual Fluid Labor ($)", value=5000.0, key="labor_in")
            disposal_annual = st.number_input("Total Annual Disposal Fees ($)", value=1500.0, key="disp_in")

    # --- CALCULATION LOGIC ---
    current_maint = maint_event_cost * maint_frequency
    
    if calc_mode == 'Subtractive':
        s_primary = primary_val * 0.25  
        s_vol = lub_volume_annually * 0.20 
        s_maint = current_maint * 0.50     
    else:
        s_primary = primary_val * 0.30  
        s_vol = lub_volume_annually * 0.50 
        s_maint = current_maint * 0.30     

    total_savings = s_primary + s_vol + (scrap_rate_cost * 0.30) + (labor_annual * 0.30) + s_maint

    # --- DASHBOARD OUTPUT (SAVINGS & ROI) ---
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
        roi = (total_savings / (lub_volume_annually if lub_volume_annually > 0 else 1) * 100)
        st.markdown(f"""
            <div style="background: rgba(142, 68, 173, 0.1); padding: 25px; border-radius: 12px; border: 2px solid #8e44ad; text-align: center;">
                <p style="color: #ffffff !important; margin: 0; font-weight: bold;">Projected ROI</p>
                <h1 style="color: #8e44ad; margin: 10px 0;">{roi:.1f}%</h1>
            </div>
        """, unsafe_allow_html=True)

    # --- THE GRAPH SECTION ---
    st.markdown("### Cumulative 12-Month Cost Comparison")
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    current_annual_burden = (current_maint + primary_val + lub_volume_annually + labor_annual + disposal_annual)
    projected_annual_burden = current_annual_burden - total_savings

    # Build the data points
    current_trend = [(current_annual_burden/12)*i for i in range(1,13)]
    projected_trend = [(projected_annual_burden/12)*i for i in range(1,13)]

    fig = go.Figure()
    
    # Current Cost Line
    fig.add_trace(go.Scatter(
        x=months, y=current_trend, 
        name="Current Process", 
        line=dict(color='#8e44ad', width=4, dash='dot')
    ))
    
    # Consultant Lubricants Line
    fig.add_trace(go.Scatter(
        x=months, y=projected_trend, 
        name="Consultant Lubricants", 
        line=dict(color='#00b5ad', width=5), 
        fill='tonexty', 
        fillcolor='rgba(0, 181, 173, 0.1)'
    ))
    
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(color="#ffffff"),
        xaxis=dict(tickfont=dict(color="#ffffff"), showgrid=False),
        yaxis=dict(tickfont=dict(color="#ffffff"), title="Cumulative Spend ($)", showgrid=True, gridcolor="#30363d"),
        legend=dict(font=dict(color="#ffffff"), orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    # Force the render
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- 7. FOOTER ---
st.markdown("---")
st.caption("Consultant Lubricants, Inc. | 9 Research Park Dr, St. Peters, MO 63376 | 636-926-9903")

# --- 7. FOOTER ---
st.markdown("---")
st.caption("PROPRIETARY & CONFIDENTIAL: © 2026 Consultant Lubricants, Inc.")
