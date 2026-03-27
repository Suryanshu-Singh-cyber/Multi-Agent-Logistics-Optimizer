import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="4D Digital Twin", layout="wide")

# --- 1. EXPLANATORY HEADER (For others to understand) ---
st.title("🛰️ 4D Fleet Digital Twin: Predictive Execution")
with st.expander("📖 What am I looking at? (Project Documentation)"):
    st.write("""
    **This is not a static map.** This is a 4D Digital Twin of a logistics network in New Delhi.
    - **3D (Space):** The (x, y) coordinates of the vans and the height of the arcs.
    - **4D (Time):** The temporal element. Use the slider below to 'scrub' through time.
    
    **How it works:** The system predicts the position of every vehicle at a specific minute. For example, if a van leaves the warehouse at 12:00 PM, 
    the 4D engine calculates exactly where it will be at 12:05 PM vs 12:10 PM based on its assigned route and current traffic.
    """)

# --- 2. TIME-OF-DAY LOGIC ---
st.sidebar.header("🕒 Master Clock")
# We start the "Logistics Day" at 12:00 PM
start_time = datetime.strptime("12:00", "%H:%M")

# Time Slider (Simulating 0 to 30 minutes of travel)
minutes_passed = st.sidebar.slider("Minutes after Noon", 0, 30, 0)
current_clock = (start_time + timedelta(minutes=minutes_passed)).strftime("%I:%M %p")

st.sidebar.metric("Simulated Time", current_clock)

# --- 3. 4D DATA ENGINE ---
warehouse = [77.23, 28.61]

@st.cache_data
def generate_predictive_trips(num_agents=6):
    trips = []
    for a in range(num_agents):
        path = [warehouse]
        timestamps = [0]
        # Target location
        target = [77.1 + np.random.rand()*0.3, 28.4 + np.random.rand()*0.4]
        
        # Create 30 "Minute" markers for the 4D path
        for m in range(1, 31):
            f = m / 30
            lng = warehouse[0] + (target[0] - warehouse[0]) * f
            lat = warehouse[1] + (target[1] - warehouse[1]) * f
            path.append([lng, lat])
            timestamps.append(m) # Each step represents 1 minute
            
        trips.append({
            "agent": f"Van {a+1}",
            "path": path,
            "timestamps": timestamps,
            "color": [0, 255, 255] if a % 2 == 0 else [255, 165, 0]
        })
    return trips

trips = generate_predictive_trips()

# --- 4. THE 4D TRIP LAYER ---
trip_layer = pdk.Layer(
    "TripsLayer",
    trips,
    get_path="path",
    get_timestamps="timestamps",
    get_color="color",
    opacity=1,
    width_min_pixels=8,
    rounded=True,
    trail_length=5, # Short trail so we can see the exact "Point" in time
    current_time=minutes_passed,
)

# --- 5. VISUALIZATION ---
st.subheader(f"📍 Fleet Status at {current_clock}")

# Add a text insight for the user
if minutes_passed == 5:
    st.info("Vans are currently clearing the main city intersections.")
elif minutes_passed == 25:
    st.success("Vans are approaching final delivery destinations.")

st.pydeck_chart(pdk.Deck(
    layers=[trip_layer],
    initial_view_state=pdk.ViewState(latitude=28.61, longitude=77.23, zoom=11, pitch=45),
    map_style=None,
    tooltip={"text": "{agent} | Position at " + current_clock}
))

# --- LIVE PREDICTION TABLE ---
st.divider()
st.subheader("📊 Real-Time Coordinate Prediction")
prediction_data = []
for t in trips:
    # Find the coordinate at the current minute
    pos = t['path'][minutes_passed]
    prediction_data.append({
        "Vehicle": t['agent'],
        "Time": current_clock,
        "Latitude": f"{pos[1]:.4f}",
        "Longitude": f"{pos[0]:.4f}",
        "Status": "In Transit" if minutes_passed < 30 else "Arrived"
    })

st.table(pd.DataFrame(prediction_data))
