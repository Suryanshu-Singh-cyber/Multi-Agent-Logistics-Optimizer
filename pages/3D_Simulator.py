import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

st.set_page_config(page_title="3D Logistics Command", layout="wide")

st.title("🚚 3D Multi-Agent Command Center")

# Create sample data for 3D Arcs
# Let's assume the warehouse is in Central Delhi (28.61, 77.23)
warehouse = [77.23, 28.61] 

def generate_3d_data(n=20):
    data = []
    for i in range(n):
        target = [77.1 + np.random.rand()*0.2, 28.5 + np.random.rand()*0.2]
        data.append({
            "from": warehouse,
            "to": target,
            "agent": f"Agent {i%3 + 1}",
            "color": [255, 100, 0, 150] if i%3==0 else [0, 255, 200, 150]
        })
    return pd.DataFrame(data)

df = generate_3d_data()

# Pydeck 3D Layer
layer = pdk.Layer(
    "ArcLayer",
    df,
    get_source_position="from",
    get_target_position="to",
    get_source_color="color",
    get_target_color=[255, 255, 255, 80],
    get_width=5,
    pickable=True,
    auto_highlight=True,
)

# Set the 3D View
view_state = pdk.ViewState(
    longitude=77.23,
    latitude=28.61,
    zoom=10,
    pitch=45, # This gives the 3D tilt
    bearing=30
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10", # Sleek dark mode
    tooltip={"text": "{agent} delivering to destination"}
))

st.sidebar.header("Agent Statistics")
st.sidebar.metric("Active Vans", "3")
st.sidebar.metric("Efficiency Score", "94%", "+2%")
