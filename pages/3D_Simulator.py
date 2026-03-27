import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="3D Logistics Command", layout="wide")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🚦 Environment Settings")
traffic_density = st.sidebar.slider("Traffic Density (Congestion)", 0, 100, 30)
num_agents = st.sidebar.select_slider("Active Agents", options=[1, 3, 5, 8], value=3)

# Logic: Higher traffic = Redder colors
def get_traffic_color(density):
    # RGB: Low = Cyan [0, 255, 200], High = Red [255, 50, 50]
    r = int((density / 100) * 255)
    g = int(255 - (density / 100) * 200)
    b = int(200 - (density / 100) * 150)
    return [r, g, b, 200]

current_color = get_traffic_color(traffic_density)

# --- MAIN UI ---
st.title("🚚 3D Logistics Command Center")

if traffic_density > 70:
    st.warning(f"High Traffic Alert: Efficiency reduced by {traffic_density - 50}%")
else:
    st.success("Traffic Flow: Optimal")

# --- DATA GENERATION ---
warehouse = [77.23, 28.61] 

@st.cache_data
def get_static_targets(n=50):
    return [[77.1 + np.random.rand()*0.25, 28.5 + np.random.rand()*0.25] for _ in range(n)]

targets = get_static_targets(num_agents * 10)
data = []
for i, t in enumerate(targets):
    data.append({
        "from": warehouse,
        "to": t,
        "agent": f"Agent {i % num_agents + 1}",
        "color": current_color
    })

df = pd.DataFrame(data)

# --- PYDECK CONFIGURATION ---

# 1. Define View State FIRST so it exists for the map
view_state = pdk.ViewState(
    longitude=77.23, 
    latitude=28.61, 
    zoom=10, 
    pitch=45, 
    bearing=0
)

# 2. Build the Warehouse Glow Layer
warehouse_layer = pdk.Layer(
    "ScatterplotLayer",
    pd.DataFrame([{"pos": warehouse}]),
    get_position="pos",
    get_color=[255, 255, 255, 255],
    get_radius=600,
)

# 3. Build the Neon Arc Layer
arc_layer = pdk.Layer(
    "ArcLayer",
    df,
    get_source_position="from",
    get_target_position="to",
    get_source_color="color",
    get_target_color=[255, 255, 255, 80],
    get_width="2 + (traffic_density / 20)", # Arcs get thicker as traffic increases
    pickable=True,
    auto_highlight=True,
)

# 4. Draw a SINGLE consolidated Map
st.pydeck_chart(pdk.Deck(
    layers=[warehouse_layer, arc_layer],
    initial_view_state=view_state,
    map_style=None, # Set to "mapbox://styles/mapbox/dark-v10" if you have a token
    tooltip={
        "html": "<b>Agent:</b> {agent}<br/><b>Status:</b> Moving through traffic",
        "style": {"color": "white"}
    }
))

# --- LIVE METRICS ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Deliveries", len(targets))
with col2:
    avg_speed = max(10, 60 - (traffic_density * 0.5))
    st.metric("Avg. Speed", f"{avg_speed:.1f} km/h", f"-{traffic_density/2}%" if traffic_density > 20 else None)
with col3:
    fuel_multiplier = 1.0 + (traffic_density * 0.01)
    st.metric("Fuel Consumption", f"{fuel_multiplier:.2f}x", delta_color="inverse")
