import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="4D Digital Twin", layout="wide")

# --- 1. SESSION STATE FOR TIME ---
if 'timer' not in st.session_state:
    st.session_state.timer = 0
if 'run' not in st.session_state:
    st.session_state.run = False

# --- 2. ADVANCED SIDEBAR ---
st.sidebar.header("🕹️ 4D Temporal Controls")
if st.sidebar.button("▶️ Play / ⏸️ Pause"):
    st.session_state.run = not st.session_state.run

playback_speed = st.sidebar.select_slider("Playback Speed", options=[1, 2, 5, 10, 20], value=5)
trail_size = st.sidebar.slider("Comet Trail Length", 100, 1000, 600)

# --- 3. 4D DATA ENGINE ---
warehouse = [77.23, 28.61]

@st.cache_data
def generate_4d_trips(num_agents=6):
    trips = []
    for a in range(num_agents):
        path = [warehouse]
        timestamps = [0]
        # Generate 15 waypoints per agent for smoother 4D motion
        target = [77.1 + np.random.rand()*0.3, 28.4 + np.random.rand()*0.4]
        
        for step in range(1, 16):
            f = step / 15
            # Add some "noise" to the path to make it look like real city driving
            noise = (np.random.rand() - 0.5) * 0.02
            lng = warehouse[0] + (target[0] - warehouse[0]) * f + noise
            lat = warehouse[1] + (target[1] - warehouse[1]) * f + noise
            path.append([lng, lat])
            timestamps.append(step * 100) # Time in 100ms chunks
            
        trips.append({
            "agent": f"Van {a+1}",
            "path": path,
            "timestamps": timestamps,
            "color": [0, 255, 255] if a % 2 == 0 else [255, 100, 0]
        })
    return trips

trips = generate_4d_trips()

# --- 4. THE 4D TRIP LAYER ---
trip_layer = pdk.Layer(
    "TripsLayer",
    trips,
    get_path="path",
    get_timestamps="timestamps",
    get_color="color",
    opacity=1,
    width_min_pixels=6,
    rounded=True,
    trail_length=trail_size,
    current_time=st.session_state.timer,
)

# --- 5. RENDER LOOP ---
st.title("🚚 4D Fleet Digital Twin: Real-Time Execution")
st.write(f"**Current Simulation Time:** `{st.session_state.timer}ms` | **Status:** {'🟢 ACTIVE' if st.session_state.run else '🔴 PAUSED'}")

map_placeholder = st.empty()

with map_placeholder:
    st.pydeck_chart(pdk.Deck(
        layers=[trip_layer],
        initial_view_state=pdk.ViewState(latitude=28.61, longitude=77.23, zoom=10, pitch=45),
        map_style=None,
    ))

# This handles the "Animation" feel
if st.session_state.run:
    st.session_state.timer += (playback_speed * 2)
    if st.session_state.timer > 1500: # Reset when trip ends
        st.session_state.timer = 0
    time.sleep(0.01)
    st.rerun()
