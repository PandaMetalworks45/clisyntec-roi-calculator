import streamlit as st
import random
import time

# --- 1. FORCE HIDE SIDEBAR & SETTINGS ---
st.set_page_config(
    page_title="Fishing Frenzy", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# This tiny CSS block ensures the sidebar toggle button is completely gone
st.markdown("<style>[data-testid='collapsedControl'] {display: none;}</style>", unsafe_allow_html=True)

# --- 2. INITIALIZE GAME TRACKING ---
if "step" not in st.session_state:
    st.session_state.step = "start_screen"
if "state" not in st.session_state:
    st.session_state.state = None
if "habitat" not in st.session_state:
    st.session_state.habitat = None
if "challenge" not in st.session_state:
    st.session_state.challenge = None
if "trophies" not in st.session_state:
    st.session_state.trophies = []

# --- 3. DATA ENGINE ---
state_habitat_data = {
    "Missouri": {
        "Lake": ["Largemouth Bass", "White Crappie", "Walleye"],
        "Pond": ["Largemouth Bass", "Bluegill", "Channel Catfish"],
        "River": ["Smallmouth Bass", "Flathead Catfish", "Paddlefish"]
    },
    "Florida": {
        "Lake": ["Florida Bass", "Bluegill", "Sunshine Bass"],
        "Pond": ["Largemouth Bass", "Warmouth"],
        "River": ["Suwannee Bass", "Gar"],
        "Ocean": ["Sailfish", "Gag Grouper", "Mahi Mahi", "Tarpon"]
    }
}

templates = [
    "Catch a {species} using {bait}",
    "Catch 3 different fish within 60 minutes",
    "Catch a {species} larger than {size} inches",
    "Catch any fish using a topwater lure",
    "Land a {species} without using a net"
]

def get_challenge(state, habitat):
    # Fallback species if habitat isn't explicitly defined
    species_list = state_habitat_data.get(state, {}).get(habitat, ["Bass", "Catfish", "Perch"])
    template = random.choice(templates)
    species = random.choice(species_list)
    bait = random.choice(["Nightcrawlers", "Plastic Worms", "Spoons", "Jigs"])
    size = random.randint(10, 25)
    return template.format(species=species, bait=bait, size=size)

# --- 4. THE LINEAR GAME FLOW ---

st.title("Fishing Frenzy")

# STEP 1: START SCREEN
if st.session_state.step == "start_screen":
    st.write("Welcome to the challenge.")
    if st.button("Start Game", use_container_width=True):
        st.session_state.step = "choose_state"
        st.rerun()

# STEP 2: CHOOSE STATE
elif st.session_state.step == "choose_state":
    st.subheader("Choose State")
    state_selection = st.selectbox("Where are you?", ["Missouri", "Florida"])
    if st.button("Next", use_container_width=True):
        st.session_state.state = state_selection
        st.session_state.step = "choose_water"
        st.rerun()

# STEP 3: CHOOSE WATER TYPE
elif st.session_state.step == "choose_water":
    st.subheader("Choose Water Type")
    # Dynamically offer water types based on state
    water_options = list(state_habitat_data[st.session_state.state].keys())
    habitat_selection = st.selectbox("What are you fishing?", water_options)
    if st.button("Generate Challenges", use_container_width=True):
        st.session_state.habitat = habitat_selection
        st.session_state.challenge = get_challenge(st.session_state.state, habitat_selection)
        st.session_state.step = "play_game"
        st.rerun()

# STEP 4: PLAY GAME
elif st.session_state.step == "play_game":
    st.write(f"**{st.session_state.state}** | **{st.session_state.habitat}**")
    st.info(f"### {st.session_state.challenge}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ I Did It!", use_container_width=True):
            st.session_state.trophies.append(st.session_state.challenge)
            st.session_state.challenge = get_challenge(st.session_state.state, st.session_state.habitat)
            st.balloons()
            st.rerun()
    with col2:
        if st.button("⏭️ Skip", use_container_width=True):
            st.session_state.challenge = get_challenge(st.session_state.state, st.session_state.habitat)
            st.rerun()

    if st.button("Quit / Reset", type="secondary"):
        st.session_state.step = "start_screen"
        st.session_state.state = None
        st.session_state.habitat = None
        st.rerun()

    # Trophy List
    if st.session_state.trophies:
        st.divider()
        st.subheader("🏆 Trophies")
        for t in reversed(st.session_state.trophies):
            st.write(f"- {t}")
