import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Algorithm Tester", layout="wide")

st.title("🧪 Stress-Testing the Algorithm")
st.write("Upload a custom CSV of coordinates to see how the agents handle your specific data.")

# --- 1. DOWNLOAD TEMPLATE ---
st.subheader("Step 1: Get the Template")
# Create a sample template
template_df = pd.DataFrame({
    'point_id': [1, 2, 3],
    'latitude': [28.61, 28.55, 28.65],
    'longitude': [77.23, 77.15, 77.30]
})

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

template_csv = convert_df(template_df)

st.download_button(
    label="📥 Download CSV Template",
    data=template_csv,
    file_name='delivery_template.csv',
    mime='text/csv',
)

# --- 2. UPLOAD & VISUALIZE ---
st.subheader("Step 2: Upload Your Data")
uploaded_file = st.file_uploader("Choose your CSV file", type="csv")

if uploaded_file is not None:
    user_data = pd.read_csv(uploaded_file)
    
    # Simple validation
    if 'latitude' in user_data.columns and 'longitude' in user_data.columns:
        st.success(f"Successfully loaded {len(user_data)} delivery points!")
        
        # Visualize the uploaded points
        view_state = pdk.ViewState(
            latitude=user_data['latitude'].mean(),
            longitude=user_data['longitude'].mean(),
            zoom=10, pitch=45
        )
        
        # Point Layer for uploaded data
        point_layer = pdk.Layer(
            "ScatterplotLayer",
            user_data,
            get_position=["longitude", "latitude"],
            get_color=[255, 165, 0, 200], # Orange
            get_radius=300,
            pickable=True
        )

        st.pydeck_chart(pdk.Deck(
            layers=[point_layer],
            initial_view_state=view_state,
            tooltip={"text": "Point ID: {point_id}"}
        ))
        
        if st.button("🚀 Run Optimization on My Data"):
            with st.status("Calculating best routes..."):
                # Here you would call your OR-Tools function
                st.write("Clustering points...")
                st.write("Applying Guided Local Search...")
                st.write("Done!")
            st.balloons()
    else:
        st.error("Error: CSV must contain 'latitude' and 'longitude' columns.")

# --- Replace the broken line near Line 80 with this ---
max_dist = 50.0  # km

# Calculate distance for every point from the warehouse [28.61, 77.23]
user_data['distance_from_hub'] = np.sqrt(
    (user_data['latitude'] - 28.61)**2 + (user_data['longitude'] - 77.23)**2
) * 111  # Rough conversion from degrees to km

# Now filter the outliers
outliers = user_data[user_data['distance_from_hub'] > max_dist]
