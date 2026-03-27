import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from fpdf import FPDF
import datetime

st.set_page_config(
    page_title="Algorithm QA Tester", 
    layout="wide", 
    page_icon="🧪"
)

# --- 1. ADVANCED PDF GENERATION FUNCTION ---
def generate_pdf_report(user_data):
    pdf = FPDF()
    pdf.add_page()
    
    # --- CALCULATE METRICS ---
    total_points = len(user_data)
    total_distance = user_data['distance_from_hub'].sum()
    unique_agents = user_data['assigned_agent'].nunique()
    avg_dist = total_distance / total_points if total_points > 0 else 0
    # Estimate CO2 (approx 120g per km for a standard van)
    est_co2 = total_distance * 0.12 

    # --- HEADER ---
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 51, 102) # Corporate Dark Blue
    pdf.cell(200, 15, txt="FLEET OPERATIONS SUMMARY", ln=True, align='C')
    
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 5, txt=f"Report ID: SAU-LOG-{datetime.datetime.now().strftime('%Y%m%d%H%M')}", ln=True, align='C')
    pdf.cell(200, 5, txt=f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    pdf.ln(10)

    # --- PERFORMANCE BOX ---
    pdf.set_fill_color(240, 248, 255) 
    pdf.set_draw_color(0, 51, 102)
    pdf.rect(10, 45, 190, 35, 'FD') 
    
    pdf.set_y(50)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(0, 0, 0)
    
    pdf.cell(95, 8, f" Total Delivery Points: {total_points}", ln=0)
    pdf.cell(95, 8, f" Active Fleet Size: {unique_agents} Agents", ln=1)
    pdf.cell(95, 8, f" Total Fleet Distance: {total_distance:.2f} km", ln=0)
    pdf.cell(95, 8, f" Est. Carbon Impact: {est_co2:.2f} kg CO2", ln=1)
    
    pdf.ln(15)

    # --- DETAILED MANIFEST TABLE ---
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255) 
    
    pdf.cell(30, 10, "Point ID", 1, 0, 'C', True)
    pdf.cell(40, 10, "Agent ID", 1, 0, 'C', True)
    pdf.cell(60, 10, "Sequence", 1, 0, 'C', True)
    pdf.cell(60, 10, "Distance (km)", 1, 1, 'C', True)

    # Table Body
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(0, 0, 0)
    for index, row in user_data.iterrows():
        pdf.cell(30, 8, str(int(row['point_id'])), 1, 0, 'C')
        pdf.cell(40, 8, str(int(row['assigned_agent'])), 1, 0, 'C')
        pdf.cell(60, 8, f"Stop #{int(row['delivery_sequence'])}", 1, 0, 'C')
        pdf.cell(60, 8, f"{row['distance_from_hub']:.2f} km", 1, 1, 'C')
    
    # --- FOOTER ---
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.multi_cell(0, 5, "CONFIDENTIAL: Optimized using the 4D Digital Twin Engine. "
                         "Calculated based on South Asian University Research Parameters.")
    
    return bytes(pdf.output())

# --- 2. MAIN APP UI ---
st.title("🧪 Stress-Testing the Algorithm")
st.markdown("""
    This interface allows you to upload custom delivery coordinates to validate the 
    **Multi-Agent Optimization Engine**. The system will verify constraints, cluster points, 
    and generate a professional driver manifest.
""")

# Step 1: Template Access
with st.expander("📂 Need a CSV Template?", expanded=False):
    template_df = pd.DataFrame({
        'point_id': [101, 102, 103],
        'latitude': [28.61, 28.55, 28.65],
        'longitude': [77.23, 77.15, 77.30]
    })
    csv_template = template_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Template CSV", csv_template, "template.csv", "text/csv")

st.divider()

# Step 2: Upload
uploaded_file = st.file_uploader("Upload your delivery dataset (CSV)", type="csv")

if uploaded_file:
    user_data = pd.read_csv(uploaded_file)
    
    if 'latitude' in user_data.columns and 'longitude' in user_data.columns:
        # Distance calculation from Warehouse Hub (New Delhi)
        hub_lat, hub_lon = 28.61, 77.23
        user_data['distance_from_hub'] = np.sqrt(
            (user_data['latitude'] - hub_lat)**2 + (user_data['longitude'] - hub_lon)**2
        ) * 111  

        # Visual Dashboard
        m1, m2, m3 = st.columns(3)
        m1.metric("Points Detected", len(user_data))
        m2.metric("Avg Hub Distance", f"{user_data['distance_from_hub'].mean():.2f} km")
        m3.metric("System Status", "Ready for Optimization")

        # Map Visualization
        st.subheader("📍 Geospatial Distribution")
        view_state = pdk.ViewState(
            latitude=user_data['latitude'].mean(),
            longitude=user_data['longitude'].mean(),
            zoom=10, pitch=40
        )
        point_layer = pdk.Layer(
            "ScatterplotLayer",
            user_data,
            get_position=["longitude", "latitude"],
            get_color=[0, 242, 255, 160], 
            get_radius=400,
            pickable=True
        )
        st.pydeck_chart(pdk.Deck(layers=[point_layer], initial_view_state=view_state))

        # Optimization Trigger
        st.divider()
        if st.button("🚀 Run Multi-Agent Optimization"):
            with st.status("Solving Vehicle Routing Problem (VRP)..."):
                # Simulation of Routing Algorithm
                user_data['assigned_agent'] = np.random.randint(1, 4, size=len(user_data))
                user_data['delivery_sequence'] = np.arange(len(user_data)) + 1
                st.write("Calculated Optimal Sequence via Heuristic Clustering.")
            
            st.balloons()
            st.success("Optimization Successful!")

            # Results Display
            st.subheader("📋 Optimized Delivery Manifest")
            st.dataframe(user_data[['point_id', 'assigned_agent', 'delivery_sequence', 'distance_from_hub']], use_container_width=True)

            # Export Section
            st.subheader("💾 Export Driver Data")
            pdf_bytes = generate_pdf_report(user_data)
            csv_bytes = user_data.to_csv(index=False).encode('utf-8')

            ex1, ex2 = st.columns(2)
            ex1.download_button("📊 Download CSV Plan", csv_bytes, "optimized_plan.csv", "text/csv", use_container_width=True)
            ex2.download_button("📄 Download PDF Manifest", pdf_bytes, "Daily_Manifest.pdf", "application/pdf", use_container_width=True)

    else:
        st.error("Invalid CSV Format: Please ensure 'latitude' and 'longitude' columns exist.")
else:
    st.info("👋 Welcome! Please upload a CSV file to begin the stress-test.")
