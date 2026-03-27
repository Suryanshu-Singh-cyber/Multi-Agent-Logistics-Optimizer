import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

st.set_page_config(page_title="Ultra 4D Digital Twin", layout="wide")

# --- 1. SESSION STATE ---
if 'timer' not in st.session_state:
    st.session_state.timer = 0
if 'run' not in st.session_state:
    st.session_state.run = False

# --- 2. EXPLANATORY HEADER (For UX) ---
st.title("🛰️ Ultra 4D Digital Twin: Environmental Stress-Test")
with st.expander("📖 System Architecture & Logic"):
    st.write("""
    ### **What is a 4D Digital Twin?**
    This page simulates a **Cyber-Physical System**. Unlike a standard map, this model accounts for **Time (4D)** and **Environmental Physics**.
    
    **Key Features Explained:**
    * **Elastic Time:** When you select 'Heavy Rain', the simulation time slows down. This mimics real-world drag and reduced velocity for drones and vans.
    * **Autonomous Rerouting:** Drones are programmed with a 'Safety Threshold'. If battery drops below 20%, they are visually flagged for immediate landing/recharge.
    * **Predictive Telemetry:** The table below predicts the exact coordinate and battery health of every unit at any given second.
    """)

# --- 3. ADVANCED ENVIRONMENT CONTROLS ---
st.sidebar.header("⛈️ Environmental Constraints")
weather_condition = st.sidebar.selectbox("Current Weather", ["Clear Skies", "Heavy Rain", "High Winds"])
battery_mode = st.sidebar.toggle("Show Battery Health", value=True)

# Logic: Weather affects speed (The 4th Dimension is elastic!)
weather_multiplier = 1.0
battery_drain_rate = 0.8
if weather_condition == "Heavy Rain":
    weather_multiplier = 0.6  
    battery_drain_rate = 1.5 # Battery dies faster in rain
elif weather_condition == "High Winds":
    weather_multiplier = 0.8  
    battery_drain_rate = 1.2

# --- 4. THE 4D CLOCK ---
st.sidebar.header("🕒 Master Control")
if st.sidebar.button("▶️ Start/Stop Simulation"):
    st.session_state.run = not st.session_state.run

sim_speed = st.sidebar.slider("Simulation Speed", 1, 10, 3)
start_time = datetime.strptime("12:00", "%H:%M")
current_clock = (start_time + timedelta(minutes=st.session_state.timer / 10)).strftime("%I:%M %p")

# --- 5. DATA ENGINE (With Autonomous Logic) ---
warehouse = [77.23, 28.61]
recharge_station = [77.15, 28.55] # Static recharge hub

@st.cache_data
def generate_advanced_trips(num_agents=6):
    trips = []
    for a in range(num_agents):
        path = [warehouse]
        timestamps = [0]
        target = [77.1 + np.random.rand()*0.3, 28.4 + np.random.rand()*0.4]
        
        for m in range(1, 101): 
            f = m / 100
            lng = warehouse[0] + (target[0] - warehouse[0]) * f
            lat = warehouse[1] + (target[1] - warehouse[1]) * f
            path.append([lng, lat])
            timestamps.append(m)
            
        trips.append({
            "agent": f"Drone-{a+101}" if a < 3 else f"Van-{a+1}",
            "path": path,
            "timestamps": timestamps,
            "color": [0, 255, 255] if a < 3 else [255, 165, 0],
            "type": "EV-Drone" if a < 3 else "Diesel-Van"
        })
    return trips

trips = generate_advanced_trips()

# --- 6. VISUALIZATION LAYERS ---
# Layer 1: The Recharge Hub
recharge_layer = pdk.Layer(
    "ScatterplotLayer",
    pd.DataFrame([{"pos": recharge_station}]),
    get_position="pos",
    get_color=[255, 0, 0, 200],
    get_radius=800,
    pickable=True,
)

# Layer 2: The Moving Fleet
trip_layer = pdk.Layer(
    "TripsLayer",
    trips,
    get_path="path",
    get_timestamps="timestamps",
    get_color="color",
    opacity=1,
    width_min_pixels=8,
    trail_length=20,
    current_time=st.session_state.timer,
)

# Render Status Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Simulated Time", current_clock)
m2.metric("Efficiency", f"{int(weather_multiplier*100)}%", delta=f"{int((weather_multiplier-1)*100)}%")
m3.metric("Fleet Status", "In Transit")

st.pydeck_chart(pdk.Deck(
    layers=[recharge_layer, trip_layer],
    initial_view_state=pdk.ViewState(latitude=28.61, longitude=77.23, zoom=11, pitch=45),
    map_style=None,
    tooltip={"text": "{agent} ({type})\nStatus: Tracking..."}
))

# --- 7. REAL-TIME TELEMETRY & ALERT SYSTEM ---
st.divider()
st.subheader("🔋 Real-Time Fleet Telemetry")

telemetry = []
current_idx = int(min(st.session_state.timer, 100))

for t in trips:
    # Battery logic: Drain rate is multiplied by weather severity
    battery = max(0, 100 - (current_idx * battery_drain_rate))
    pos = t['path'][current_idx]
    
    # Autonomous Alert Logic
    status = "✅ OPTIMAL"
    color_ui = "normal"
    if battery < 20:
        status = "🚨 EMERGENCY: RECHARGE REQ"
        color_ui = "inverse"
    elif battery < 50:
        status = "⚠️ CAUTION: LOW POWER"

    telemetry.append({
        "Unit": t['agent'],
        "Type": t['type'],
        "Battery/Fuel": f"{battery:.1f}%",
        "Position": f"{pos[1]:.3f}, {pos[0]:.3f}",
        "Safety Status": status
    })

st.table(pd.DataFrame(telemetry))

# --- 8. ANIMATION ENGINE ---
if st.session_state.run:
    st.session_state.timer += (sim_speed * weather_multiplier)
    if st.session_state.timer > 100:
        st.session_state.timer = 0
    time.sleep(0.05)
    st.rerun()
