import streamlit as st
import random
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Fun Fishing Frenzy", page_icon="🎣")

# --- DATA: SMART HABITAT ENGINE ---
# State-specific species categorized by habitat
state_habitat_data = {
    "Missouri": {
        "Lake": ["Largemouth Bass", "White Crappie", "Walleye", "Bluegill", "Channel Catfish"],
        "Pond": ["Largemouth Bass", "Bluegill", "Hybrid Sunfish", "Channel Catfish"],
        "River": ["Smallmouth Bass", "Flathead Catfish", "Paddlefish", "Blue Catfish", "Sauger"],
        "Anywhere": ["Channel Catfish", "Bluegill", "Carp"]
    },
    "Florida": {
        "Lake": ["Florida Largemouth Bass", "Bluegill", "Black Crappie", "Sunshine Bass"],
        "Pond": ["Largemouth Bass", "Bluegill", "Warmouth", "Catfish"],
        "River": ["Suwannee Bass", "Red Drum (Escaped)", "Striped Bass", "Gar"],
        "Bay": ["Snook", "Red Drum", "Spotted Seatrout", "Mangrove Snapper"],
        "Open Ocean": ["Sailfish", "Gag Grouper", "Mahi Mahi", "King Mackerel", "Tarpon"]
    },
    "Texas": {
        "Lake": ["Largemouth Bass", "White Bass", "Striped Bass", "Crappie"],
        "Pond": ["Bass", "Bluegill", "Catfish"],
        "River": ["Guadalupe Bass", "Alligator Gar", "Flathead Catfish", "River Carp"],
        "Bay": ["Red Drum", "Speckled Trout", "Flounder"],
        "Open Ocean": ["Red Snapper", "Cobias", "Yellowfin Tuna", "King Mackerel"]
    }
}

# Generic fallback for other states
fallback_data = {
    "Freshwater": ["Largemouth Bass", "Bluegill", "Catfish", "Yellow Perch"],
    "Saltwater": ["Sea Trout", "Snapper", "Mackerel", "Flounder"]
}

baits = ["Nightcrawlers", "Spinnerbaits", "Plastic Worms", "Crankbaits", "Live Shrimp", "Spoons", "Corn", "Jigs"]

templates = [
    "Catch a {species} using {bait}",
    "Catch 3 different fish within 60 minutes",
    "Catch a {species} larger than {size} inches",
    "Catch any fish using a topwater lure",
    "Land a {species} without using a net",
    "Catch a fish using a lure that has the color 'Red' on it"
]

# --- INITIALIZE SESSION STATE ---
if "challenge" not in st.session_state:
    st.session_state.challenge = None
if "trophies" not in st.session_state:
    st.session_state.trophies = []

def get_challenge(state, habitat):
    # Retrieve species based on state and habitat
    state_info = state_habitat_data.get(state, {})
    species_list = state_info.get(habitat, fallback_data["Saltwater"] if habitat in ["Bay", "Open Ocean"] else fallback_data["Freshwater"])
    
    template = random.choice(templates)
    species = random.choice(species_list)
    bait = random.choice(baits)
    size = random.randint(10, 25)
    return template.format(species=species, bait=bait, size=size)

# --- SIDEBAR: GATEKEEPER ---
st.sidebar.title("🎣 Setup Your Trip")

# Force State Selection first
state = st.sidebar.selectbox("1. Choose Your State", ["-- Select --", "Missouri", "Florida", "Texas"])

# --- MAIN INTERFACE ---
st.title("Fun Fishing Frenzy")

if state == "-- Select --":
    st.warning("Please select a state in the sidebar to begin your fishing trip!")
    st.stop() # Prevents the rest of the app from loading until state is picked

# Once State is picked, show Environment options
mode = st.sidebar.radio("2. Choose Environment", ["Freshwater", "Saltwater"])

if mode == "Freshwater":
    habitat = st.sidebar.selectbox("3. Body of Water", ["Lake", "Pond", "River", "Anywhere"])
else:
    habitat = st.sidebar.selectbox("3. Body of Water", ["Bay", "Open Ocean"])

st.write(f"Currently fishing in: **{habitat}** ({state})")

# Challenge Logic
if st.session_state.challenge is None:
    if st.button("Generate First Challenge"):
        st.session_state.challenge = get_challenge(state, habitat)
        st.rerun()
else:
    st.info(f"### {st.session_state.challenge}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ I Did It!"):
            st.session_state.trophies.append(f"{state} {habitat}: {st.session_state.challenge}")
            st.session_state.challenge = get_challenge(state, habitat)
            st.success("Big checkmark! Challenge Complete!")
            st.balloons()
            time.sleep(1)
            st.rerun()
    with col2:
        if st.button("⏭️ Skip"):
            st.session_state.challenge = get_challenge(state, habitat)
            st.rerun()

# --- TROPHY ROOM ---
st.divider()
st.subheader("🏆 Your Trophy Room")
for t in reversed(st.session_state.trophies):
    st.write(f"- {t}")
