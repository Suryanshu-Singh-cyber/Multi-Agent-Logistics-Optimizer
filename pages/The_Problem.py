import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(page_title="The Logistics Nightmare", layout="wide")

st.title("📊 The Problem: Why Optimization Matters")

st.write("""
Imagine you have **3 Agents** and **30 Deliveries** across New Delhi. 
Without an optimizer, agents often "criss-cross" the city, visiting the same neighborhoods at different times.
""")

# --- 1. GENERATE DATA ---
warehouse = [77.23, 28.61]
np.random.seed(42) # Keep it consistent for the comparison
targets = [[77.1 + np.random.rand()*0.25, 28.5 + np.random.rand()*0.25] for _ in range(30)]

# Chaos Data (Randomly assigned)
chaos_data = []
for i, t in enumerate(targets):
    chaos_data.append({"from": warehouse, "to": t, "agent": f"Agent {i % 3}"})

# Optimized Data (Grouped by Longitude to simulate basic clustering)
targets_sorted = sorted(targets, key=lambda x: x[0])
opt_data = []
for i, t in enumerate(targets_sorted):
    agent_id = 0 if i < 10 else (1 if i < 20 else 2)
    opt_data.append({"from": warehouse, "to": t, "agent": f"Agent {agent_id}"})

# --- 2. THE COMPARISON UI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ Unoptimized (The Chaos)")
    st.error("Agents cross paths, doubling fuel costs.")
    
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=28.61, longitude=77.23, zoom=9.5, pitch=40),
        layers=[pdk.Layer("ArcLayer", chaos_data, get_source_position="from", get_target_position="to", 
                          get_source_color=[255, 0, 0, 150], get_target_color=[255, 200, 200, 80], get_width=2)]
    ))

with col2:
    st.subheader("✅ Optimized (The Solution)")
    st.success("Agents stay in zones, reducing distance by ~40%.")
    
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(latitude=28.61, longitude=77.23, zoom=9.5, pitch=40),
        layers=[pdk.Layer("ArcLayer", opt_data, get_source_position="from", get_target_position="to", 
                          get_source_color=[0, 255, 150, 150], get_target_color=[200, 255, 200, 80], get_width=2)]
    ))
    # Add this logic to 1_📊_The_Problem.py
st.sidebar.subheader("Fleet Parameters")
fuel_price = st.sidebar.number_input("Fuel Price (per liter)", 90, 110, 96)
avg_mileage = st.sidebar.slider("Vehicle Mileage (km/l)", 5, 20, 12)

# Calculate real-world savings
dist_saved = 45.2 # Simulated value
money_saved = (dist_saved / avg_mileage) * fuel_price
co2_saved = dist_saved * 0.12 # 120g per km

col1, col2, col3 = st.columns(3)
col1.metric("Fuel Savings", f"₹{money_saved:,.0f}", "+15%")
col2.metric("CO2 Reduced", f"{co2_saved:.1f} kg", "-22%")
col3.metric("Fleet Utilization", "98%", "+12%")

# --- 3. THE "WHY" METRICS ---
st.divider()
st.header("The Hidden Costs of Bad Logistics")

m1, m2, m3 = st.columns(3)
m1.metric("Carbon Footprint", "+42%", "Excessive Travel", delta_color="inverse")
m2.metric("Delivery Delay", "2.5 Hours", "Traffic Overlap", delta_color="inverse")
m3.metric("Fleet Wear", "High", "Tire & Fuel Waste", delta_color="inverse")

st.info("💡 Move to the next page to see the **Algorithm** that fixes this chaos!")
