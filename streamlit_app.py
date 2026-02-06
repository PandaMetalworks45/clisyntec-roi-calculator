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
    
    .menu-btn-container .stButton>button {
        height: 200px !important;
        width: 100% !important;
        max-width: 800px !important; /* Prevents it from stretching too far on wide screens */
        margin: 10px auto !important; /* Centers and adds spacing between them */
        display: block !important;
        font-size: 28px !important;
        border: 2px solid #00b5ad !important;
        transition: all 0.3s ease !important;
        white-space: pre-wrap !important;
    }
    .menu-btn-container .stButton>button:hover {
        border: 2px solid #8e44ad !important;
        transform: scale(1.02);
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
    
    # Title and Subtitle (Keep these centered)
    st.markdown("<h1 style='text-align: center;'>Consultant Lubricant's TCO Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Select a process to start the financial comparison.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # --- THIS IS WHERE THE STACKED BUTTONS GO ---
    st.markdown('<div class="menu-btn-container">', unsafe_allow_html=True)
    
    # First Big Button
    if st.button("🏗️\n\nFORMING CALCULATOR", use_container_width=True):
        st.session_state.page = 'calculator'
        st.session_state.calc_type = 'Forming'
        st.rerun()
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Second Big Button
    if st.button("⚙️\n\nSUBTRACTIVE CALCULATOR", use_container_width=True):
        st.session_state.page = 'calculator'
        st.session_state.calc_type = 'Subtractive'
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
    # --- END OF STACKED BUTTONS ---

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")

    # The Slider/Carousel section usually follows right after this...

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
                avg_tool_cost = st.number_input("Average Tool Replacement Cost ($)", value=300.0, key="sub_tool_avg")
                tool_changes = st.number_input("Annual Tool Changes (#)", value=150, key="sub_t_changes")
                primary_val = avg_tool_cost * tool_changes
                st.caption(f"Calculated Annual Tool Spend: **${primary_val:,.2f}**")
                
                scrap_rate_pct = st.number_input("Current Scrap Rate (%)", value=5.0, step=0.1, key="sub_scrap_pct") / 100
                
                # Hidden variables for math consistency
                die_change_total = 0
            
            else: # FORMING CALCULATOR (WITH NEW DIE CHANGE FIELDS)
                primary_val = st.number_input("Annual Die Coating/Polishing Costs ($)", value=5000.0, key="form_die_costs")
                
                # NEW FIELDS FOR FORMING
                annual_die_changes = st.number_input("Annual Die Changes (#)", value=24, key="form_die_changes")
                cost_per_die_change = st.number_input("Cost Per Die Change (Labor/Downtime) ($)", value=200, key="form_cost_per_die")
                
                die_change_total = annual_die_changes * cost_per_die_change
                st.caption(f"Calculated Annual Changeover Cost: **${die_change_total:,.2f}**")
                
                scrap_rate_pct = st.number_input("Current Scrap Rate (%)", value=3.0, step=0.1, key="form_scrap_pct") / 100
                
                # Hidden variables for math consistency
                tool_changes = 0
        
        with col2:
            st.subheader("Maintenance & Fluid Costs")
            fill_label = "Cost per Sump Fill ($)" if calc_mode == 'Subtractive' else "Cost per Sump Fill ($)"
            
            fill_cost = st.number_input(fill_label, value=1000, key=f"{calc_mode}_fill_val")
            fill_frequency = st.number_input("Fills Per Year", value=6, key=f"{calc_mode}_freq_val")
            
            monthly_adds = st.number_input("Monthly Additives Cost ($)", value=300, key=f"{calc_mode}_adds_val")
            annual_additives = monthly_adds * 12
            disposal_annual = st.number_input("Annual Disposal Fees ($)", value=1500.0, key=f"{calc_mode}_disp_val")

    # --- CALCULATION LOGIC ---
    current_fills_total = fill_cost * fill_frequency
    
    if calc_mode == 'Subtractive':
        base_annual_cost = primary_val + (tool_changes) + current_fills_total + annual_additives + disposal_annual
        scrap_burden = base_annual_cost * scrap_rate_pct
        
        s_tooling = primary_val * 0.25      
        s_labor = (tool_changes) * 0.25 
        s_fills = current_fills_total * 0.50 
        s_adds = annual_additives * 0.80    
        s_scrap = scrap_burden * 0.30       
        total_savings = s_tooling + s_labor + s_fills + s_adds + s_scrap
        
    else: # FORMING (UPDATED MATH)
        # Adding the Die Change Total to the Base Cost
        base_annual_cost = primary_val + die_change_total + current_fills_total + annual_additives + disposal_annual
        scrap_burden = base_annual_cost * scrap_rate_pct
        
        # Savings Estimates
        s_die_life = primary_val * 0.30     
        s_die_change = die_change_total * 0.30  # Assuming 30% fewer changeovers due to better lubrication
        s_fills = current_fills_total * 0.40 
        s_adds = annual_additives * 0.70    
        s_scrap = scrap_burden * 0.20       
        
        total_savings = s_die_life + s_die_change + s_fills + s_adds + s_scrap

    current_annual_burden = base_annual_cost + scrap_burden
    projected_annual_burden = current_annual_burden - total_savings

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
