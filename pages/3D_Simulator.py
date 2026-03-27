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
    return [r, g, b, 160]

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
    # We cache these so the dots don't jump every time you move the slider
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

# --- PYDECK 3D VISUALIZATION ---
# Layer 1: The Arcs (Routes)
arc_layer = pdk.Layer(
    "ArcLayer",
    df,
    get_source_position="from",
    get_target_position="to",
    get_source_color="color",
    get_target_color=[255, 255, 255, 50],
    get_width=3,
    pickable=True,
)

# Layer 2: The Warehouse Glow
warehouse_layer = pdk.Layer(
    "ScatterplotLayer",
    pd.DataFrame([{"pos": warehouse}]),
    get_position="pos",
    get_color=[255, 255, 255, 200],
    get_radius=500,
)

view_state = pdk.ViewState(
    longitude=77.23, latitude=28.61, zoom=10, pitch=45, bearing=0
)

st.pydeck_chart(pdk.Deck(
    layers=[arc_layer, warehouse_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={"text": "{agent} | Status: Moving through traffic"}
))

# --- LIVE METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Deliveries", len(targets))
with col2:
    avg_speed = max(10, 60 - (traffic_density * 0.5))
    st.metric("Avg. Speed", f"{avg_speed:.1f} km/h", f"-{traffic_density/2}%" if traffic_density > 20 else None)
with col3:
    st.metric("Fuel Consumption", f"{1.2 + (traffic_density * 0.01):.2f}x", delta_color="inverse")
