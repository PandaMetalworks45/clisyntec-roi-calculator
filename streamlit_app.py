import streamlit as st
import random
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Fun Fishing Frenzy", page_icon="🎣")

# --- INITIALIZE SESSION STATE ---
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "selected_habitat" not in st.session_state:
    st.session_state.selected_habitat = None
if "challenge" not in st.session_state:
    st.session_state.challenge = None
if "trophies" not in st.session_state:
    st.session_state.trophies = []

# --- DATA: SMART HABITAT ENGINE ---
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
        "River": ["Suwannee Bass", "Red Drum", "Striped Bass", "Gar"],
        "Bay": ["Snook", "Red Drum", "Spotted Seatrout", "Mangrove Snapper"],
        "Open Ocean": ["Sailfish", "Gag Grouper", "Mahi Mahi", "King Mackerel", "Tarpon"]
    },
    "Texas": {
        "Lake": ["Largemouth Bass", "White Bass", "Striped Bass", "Crappie"],
        "Pond": ["Bass", "Bluegill", "Catfish"],
        "River": ["Guadalupe Bass", "Alligator Gar", "Flathead Catfish", "River Carp"],
        "Bay": ["Red Drum", "Speckled Trout", "Flounder"],
        "Open Ocean": ["Red Snapper", "Cobia", "Yellowfin Tuna", "King Mackerel"]
    }
}

fallback_data = {
    "Freshwater": ["Largemouth Bass", "Bluegill", "Catfish", "Yellow Perch"],
    "Saltwater": ["Sea Trout", "Snapper", "Mackerel", "Flounder"]
