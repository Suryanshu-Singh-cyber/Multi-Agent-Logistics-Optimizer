import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="3D Logistics Command", layout="wide")

# --- 1. ANIMATION STATE ---
if 'timer' not in st.session_state:
    st.session_state.timer = 0
if 'run' not in st.session_state:
    st.session_state.run = False

# --- 2. SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Animation Control")
if st.sidebar.button("▶️ Start/Stop Simulation"):
    st.session_state.run = not st.session_state.run

speed = st.sidebar.slider("Simulation Speed", 1, 10, 5)
traffic_density = st.sidebar.slider("Traffic Congestion", 0, 100, 30)

# --- 3. DATA GENERATION (Path-based for TripLayer) ---
warehouse = [77.23, 28.61]

@st.cache_data
def generate_trip_data(num_agents=5):
    trips = []
    for a in range(num_agents):
        # Create a path of 10 points for each agent
        path = [warehouse]
        target = [77.1 + np.random.rand()*0.25, 28.5 + np.random.rand()*0.25]
        
        # Simple linear interpolation for the "trip"
        for step in range(1, 11):
            fraction = step / 10
            lng = warehouse[0] + (target[0] - warehouse[0]) * fraction
            lat = warehouse[1] + (target[1] - warehouse[1]) * fraction
            path.append([lng, lat, step * 100]) # [lng, lat, timestamp]
            
        trips.append({
            "vendor": f"Agent {a+1}",
            "path": path,
            "color": [0, 255, 255] if a % 2 == 0 else [255, 0, 150]
        })
    return trips

trips = generate_trip_data()

# --- 4. THE TRIP LAYER ---
# This layer renders the "moving" trails based on the timestamp
trip_layer = pdk.Layer(
    "TripsLayer",
    trips,
    get_path="path",
    get_timestamps="path.map(p => p[2])",
    get_color="color",
    opacity=0.8,
    width_min_pixels=5,
    rounded=True,
    trail_length=150, # How long the "tail" is
    current_time=st.session_state.timer,
)

view_state = pdk.ViewState(latitude=28.61, longitude=77.23, zoom=10, pitch=45)

# --- 5. RENDER & ANIMATION LOOP ---
st.title("🚚 4D Fleet Digital Twin")

map_placeholder = st.empty()

# The Animation Loop
if st.session_state.run:
    # Increment timer
    st.session_state.timer += (speed * 2)
    if st.session_state.timer > 1200: # Reset loop
        st.session_state.timer = 0
    
    # Redraw map
    with map_placeholder:
        st.pydeck_chart(pdk.Deck(
            layers=[trip_layer],
            initial_view_state=view_state,
            map_style=None,
        ))
    time.sleep(0.05)
    st.rerun() # This triggers the next frame
else:
    with map_placeholder:
        st.pydeck_chart(pdk.Deck(
            layers=[trip_layer],
            initial_view_state=view_state,
            map_style=None,
        ))

# --- METRICS ---
st.divider()
st.info(f"Current Simulation Time: {st.session_state.timer} | Status: {'Running' if st.session_state.run else 'Paused'}")
