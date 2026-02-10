import streamlit as st
import random
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Fun Fishing Frenzy", page_icon="🎣")

# --- INITIALIZE SESSION STATE ---
if "challenge" not in st.session_state:
    st.session_state.challenge = None
if "trophies" not in st.session_state:
    st.session_state.trophies = []
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# --- STATE-SPECIFIC FISH DATA ---
# This dictionary maps states to their 10 most common/popular catches
state_fish_map = {
    "Missouri": ["Largemouth Bass", "Smallmouth Bass", "Bluegill", "Channel Catfish", "White Crappie", "Black Crappie", "Walleye", "Rainbow Trout", "Paddlefish", "Flathead Catfish"],
    "Florida": ["Largemouth Bass", "Snook", "Red Drum (Redfish)", "Spotted Seatrout", "Tarpon", "Mangrove Snapper", "Gag Grouper", "Sailfish", "Spanish Mackerel", "Bluegill"],
    "Texas": ["Largemouth Bass", "Red Drum", "Alligator Gar", "Channel Catfish", "White Bass", "Speckled Trout", "Crappie", "Flounder", "Striped Bass", "BlueCatfish"],
    "California": ["Rainbow Trout", "California Golden Trout", "Largemouth Bass", "Chinook Salmon", "Striped Bass", "Calico Bass", "Lingcod", "Halibut", "Sturgeon", "Bluegill"],
    "Michigan": ["Walleye", "Yellow Perch", "Smallmouth Bass", "Brook Trout", "Lake Trout", "Northern Pike", "Muskellunge", "Chinook Salmon", "Steelhead", "Bluegill"],
    "Wisconsin": ["Walleye", "Muskellunge", "Northern Pike", "Yellow Perch", "Smallmouth Bass", "Largemouth Bass", "Crappie", "Bluegill", "Lake Trout", "Channel Catfish"],
    "Minnesota": ["Walleye", "Northern Pike", "Largemouth Bass", "Smallmouth Bass", "Crappie", "Bluegill", "Yellow Perch", "Lake Trout", "Muskellunge", "Sauger"],
    "New York": ["Striped Bass", "Largemouth Bass", "Smallmouth Bass", "Walleye", "Lake Trout", "Atlantic Salmon", "Yellow Perch", "Bluefish", "Summer Flounder", "Black Sea Bass"],
    "North Carolina": ["Red Drum", "Largemouth Bass", "Bluefish", "Speckled Trout", "Striped Bass", "Flounder", "Channel Catfish", "Yellow Perch", "Crappie", "Spanish Mackerel"],
    "Alabama": ["Largemouth Bass", "Spotted Bass", "Crappie", "Bluegill", "Channel Catfish", "Red Drum", "Speckled Trout", "Cobia", "King Mackerel", "Red Snapper"],
    "General US": ["Largemouth Bass", "Bluegill", "Channel Catfish", "Crappie", "Rainbow Trout", "Yellow Perch", "Smallmouth Bass", "Common Carp", "Striped Bass", "Bullhead"]
}

baits = ["Nightcrawlers", "Spinnerbaits", "Plastic Worms", "Crankbaits", "Live Shrimp", "Spoons", "Corn", "Topwater Plugs", "Jigs"]

# REMOVED: "Catch on your first cast" challenges
templates = [
    "Catch a {species} using {bait}",
    "Catch 3 different fish within 60 minutes",
    "Catch a {species} larger than {size} inches",
    "Catch any fish using a topwater lure",
    "Land a fish without using a net",
    "Catch a {species} while standing on one leg for the last 10 seconds of the fight",
    "Catch a fish using a lure that has the color 'Red' on it",
    "Successfully release a {species} after taking a quick 'Trophy Photo'"
]

def get_new_challenge(state_name):
    template = random.choice(templates)
    # Fallback to General US if state isn't in our top 10 list
    species_list = state_fish_map.get(state_name, state_fish_map["General US"])
    species = random.choice(species_list)
    bait = random.choice(baits)
    size = random.randint(10, 25)
    return template.format(species=species, bait=bait, size=size)

# --- SIDEBAR: SETTINGS ---
st.sidebar.title("🎣 Master Settings")

# 1. State Selection
selected_state = st.sidebar.selectbox("Select your State", sorted(list(state_fish_map.keys())))

# 2. Environment Selection
mode = st.sidebar.radio("Environment", ["Freshwater", "Saltwater"])

if mode == "Freshwater":
    location = st.sidebar.selectbox("Specific Setting", ["Lake", "Pond", "River", "Anywhere"])
else:
    location = st.sidebar.selectbox("Specific Setting", ["Bay", "Open Ocean"])

if st.sidebar.button("Reset All Progress"):
    st.session_state.challenge = None
    st.session_state.trophies = []
    st.rerun()

# --- MAIN APP INTERFACE ---
st.title("Fun Fishing Frenzy")
st.write(f"Location: **{location}** in **{selected_state}**")

# Success Celebration
if st.session_state.show_success:
    st.success("CHALLENGE COMPLETE!", icon="✅")
    st.balloons()
    st.session_state.show_success = False

# Challenge Logic
if st.session_state.challenge is None:
    if st.button("Generate My First Challenge"):
        st.session_state.challenge = get_new_challenge(selected_state)
        st.rerun()
else:
    st.info(f"### {st.session_state.challenge}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ I Did It!"):
            st.session_state.trophies.append(f"{selected_state} ({location}): {st.session_state.challenge}")
            st.session_state.challenge = get_new_challenge(selected_state)
            st.session_state.show_success = True
            st.rerun()
            
    with col2:
        if st.button("⏭️ Skip Challenge"):
            st.session_state.challenge = get_new_challenge(selected_state)
            st.rerun()

# --- TROPHY ROOM ---
st.divider()
st.subheader("🏆 Your Trophy Room")
if st.session_state.trophies:
    for t in reversed(st.session_state.trophies):
        st.write(f"- {t}")
else:
    st.write("Your trophy wall is empty. Go catch something!")
