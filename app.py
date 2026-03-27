import streamlit as st
import random
import numpy as np
from sklearn.cluster import KMeans
from ortools.constraint_solver import pywrapcp
import folium
from streamlit_folium import st_folium
import time

# Optional Gemini (safe fallback)
USE_GEMINI = False
try:
    import google.generativeai as genai
    # genai.configure(api_key="YOUR_API_KEY")
    # model = genai.GenerativeModel("gemini-pro")
    # USE_GEMINI = True
except: 
    USE_GEMINI = False

# st.set_page_config(layout="wide")
# # st.title("🚀 Nexus-Route: Real-Time Logistics Simulation")
# st.title("📦 Project: Multi-Agent Logistics Optimizer")

# with st.chat_message("assistant"):
#     st.write("Hello! I am the Logistics AI. Shipping 10,000 packages across Delhi is a nightmare. Doing it randomly wastes fuel and time.")
#     st.write("In this project, I use **OR-Tools** and **Multi-Agent Systems** to find the perfect path.")

# st.info("👈 Use the sidebar to explore the math or launch the 3D Simulator!")

# # Add a nice visual or a YouTube video link of drones/vans here
# st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?auto=format&fit=crop&w=800", caption="Future of Logistics")

import streamlit as st

st.set_page_config(
    page_title="Logistics Digital Twin", 
    layout="wide", 
    page_icon="🛰️"
)

# --- CUSTOM CSS FOR MODERN UI ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4255; }
    .feature-card {
        background-color: #161b22;
        padding: 25px;
        border-radius: 15px;
        border-top: 4px solid #00f2ff;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .feature-card:hover { transform: translateY(-5px); border-top: 4px solid #ff00ff; }
    .highlight { color: #00f2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
# This high-quality image sets the stage for "4D Digital Twin"
st.image("http://googleusercontent.com/image_collection/image_retrieval/6266554220892605383_0", 
         use_container_width=True)

st.title("🛰️ Multi-Agent Logistics: The 4D Digital Twin")
st.markdown("""
    ### **Bridging the Gap between Optimization and Reality**
    Welcome to the next generation of fleet management. This project isn't just a map; it's a **Cyber-Physical Simulation** designed to solve the most complex challenge in modern robotics: **The Last-Mile Delivery.**
""")

st.divider()

# --- THE THREE PILLARS (Visual Guide) ---
st.header("🚀 How the Digital Twin Works")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h2>📍 01. Plan</h2>
        <p>Using <b>Google OR-Tools</b>, we solve the Vehicle Routing Problem (VRP). We calculate the shortest, most efficient paths for a fleet of multiple agents simultaneously.</p>
        <p class="highlight">→ High Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h2>⛈️ 02. Stress-Test</h2>
        <p>We apply real-world constraints: <b>Heavy Rain, High Winds, and Battery Decay</b>. We test if the plan survives the chaos of New Delhi's environment.</p>
        <p class="highlight">→ Physics-Aware</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h2>🛸 03. Execute</h2>
        <p>We visualize the result in <b>4D Space-Time</b>. Watch neon 'comet trails' move across the map, predicting every vehicle's position down to the second.</p>
        <p class="highlight">→ Real-Time 4D</p>
    </div>
    """, unsafe_allow_html=True)

# --- TECH STACK SECTION ---
st.divider()
st.header("🧬 Engineering Core")
t1, t2, t3, t4 = st.columns(4)

with t1:
    st.write("🐍 **Language**")
    st.info("Python 3.10")
with t2:
    st.write("🧠 **Optimization**")
    st.info("Google OR-Tools")
with t3:
    st.write("🛰️ **Visualization**")
    st.info("PyDeck (WebGL)")
with t4:
    st.write("☁️ **Deployment**")
    st.info("Streamlit Cloud")

# --- FOOTER & CONTACT ---
st.divider()
st.success("👈 **Explore the Fleet: Select '4D Simulator' or 'QA Tester' from the sidebar to begin.**")

# Professional Footer
f1, f2 = st.columns([3, 1])
with f1:
    st.markdown("""
        **Project for South Asian University Research Sprint** *Focus: Spiking Neural Networks, Robotics, and Event-Based Vision.*
    """)
with f2:
    st.markdown("[LinkedIn](https://www.linkedin.com/) | [GitHub](https://github.com/)")



# -----------------------------
# UI CONTROLS
# -----------------------------
num_packages = st.sidebar.slider("📦 Packages", 20, 100, 50)
num_agents = st.sidebar.slider("🚚 Vans", 2, 8, 5)

simulate_traffic = st.sidebar.toggle("🚧 Traffic")
run_simulation = st.sidebar.button("▶️ Start Simulation")
reset = st.sidebar.button("🔄 Reset")

if reset:
    st.rerun()

# -----------------------------
# STEP 1: Generate Real Locations
# -----------------------------
# -----------------------------
# STEP 1: Generate Real Locations (CACHED)
# -----------------------------
@st.cache_data
def generate_packages(n):
    return [(28.5 + random.random()*0.2, 77.1 + random.random()*0.2) for _ in range(n)]

# If the user clicks reset, clear the memory!
if reset:
    generate_packages.clear()
    st.rerun()

packages = generate_packages(num_packages)
points = np.array(packages)

# -----------------------------
# STEP 2: Clustering
# -----------------------------
kmeans = KMeans(n_clusters=num_agents, random_state=0, n_init=10)
labels = kmeans.fit_predict(points)

# -----------------------------
# STEP 3: Agents
# -----------------------------
agents = []
for i in range(num_agents):
    agent = {
        "id": i,
        "battery": random.randint(20, 100),
        "status": "Active",
        "packages": list(points[labels == i])
    }
    if agent["battery"] < 30:
        agent["status"] = "Low Battery ⚠️"
    agents.append(agent)

# -----------------------------
# STEP 4: AI Negotiator
# -----------------------------
def ai_negotiator(low_agent, agents):
    active_agents = [a for a in agents if a["status"] == "Active"]

    if not active_agents:
        return None

    if USE_GEMINI:
        try:
            prompt = f"Choose best van ID for package transfer:\n"
            for a in agents:
                prompt += f"Van {a['id']} Battery {a['battery']} Load {len(a['packages'])}\n"

            response = model.generate_content(prompt)
            chosen_id = int(response.text.strip())
            return next(a for a in agents if a["id"] == chosen_id)
        except:
            pass

    # fallback logic
    return max(active_agents, key=lambda a: a["battery"] - len(a["packages"])*2)

# -----------------------------
# STEP 5: Reallocation
# -----------------------------
for agent in agents:
    if agent["status"] == "Low Battery ⚠️":
        for pkg in agent["packages"]:
            best = ai_negotiator(agent, agents)
            if best:
                best["packages"].append(pkg)
        agent["packages"] = []

# -----------------------------
# STEP 6: Distance Matrix
# -----------------------------
def create_distance_matrix(locations):
    size = len(locations)
    matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            dist = np.linalg.norm(locations[i] - locations[j])
            if simulate_traffic:
                dist *= random.uniform(1.2, 1.8)
            matrix[i][j] = dist
    return matrix

# -----------------------------
# STEP 7: Solve Route
# -----------------------------
def solve_tsp(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def callback(i, j):
        return int(distance_matrix[manager.IndexToNode(i)][manager.IndexToNode(j)])

    idx = routing.RegisterTransitCallback(callback)
    routing.SetArcCostEvaluatorOfAllVehicles(idx)

    solution = routing.SolveWithParameters(pywrapcp.DefaultRoutingSearchParameters())

    route = []
    index = routing.Start(0)
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))

    return route

# -----------------------------
# STEP 8: Prepare Routes
# -----------------------------
routes = {}

for agent in agents:
    pts = np.array(agent["packages"])
    if len(pts) < 2:
        continue

    matrix = create_distance_matrix(pts)
    route_idx = solve_tsp(matrix)
    routes[agent["id"]] = pts[route_idx]

# -----------------------------
# STEP 9: Metrics
# -----------------------------
active_vans = sum(1 for a in agents if a["status"] == "Active")

st.sidebar.header("📊 Metrics")
st.sidebar.metric("Packages", num_packages)
st.sidebar.metric("Active Vans", active_vans)

# -----------------------------
# STEP 10: Agent Status
# -----------------------------
st.sidebar.header("🚚 Agents")
for a in agents:
    st.sidebar.write(f"Van {a['id']} | 🔋 {a['battery']}% | 📦 {len(a['packages'])} | {a['status']}")

# -----------------------------
# STEP 11: MAP SIMULATION
# -----------------------------
# -----------------------------
# STEP 11: MAP SIMULATION
# -----------------------------
colors = ["red","blue","green","purple","orange","black","pink","cyan"]

if run_simulation:
    map_placeholder = st.empty() # Creates a single fixed box for the animation
    
    for step in range(20):
        m = folium.Map(location=[28.6, 77.2], zoom_start=11)

        # Draw packages
        for p in packages:
            folium.CircleMarker(location=p, radius=3, color="gray").add_to(m)

        for agent_id, route in routes.items():
            if len(route) < 2:
                continue

            # Draw route line
            folium.PolyLine(route, color=colors[agent_id]).add_to(m)

            # Draw moving van
            pos = route[min(step, len(route)-1)]
            folium.Marker(
                location=pos,
                icon=folium.Icon(color=colors[agent_id], icon="car")
            ).add_to(m)

        # Draw to the placeholder, and stop it from triggering re-runs!
        with map_placeholder:
            st_folium(m, width=900, height=500, returned_objects=[], key=f"anim_{step}")
        
        time.sleep(0.3)


else:
    # static preview
    m = folium.Map(location=[28.6, 77.2], zoom_start=11)

    for p in packages:
        folium.CircleMarker(location=p, radius=3).add_to(m)

    for agent_id, route in routes.items():
        if len(route) < 2:
            continue
        folium.PolyLine(route, color=colors[agent_id]).add_to(m)

    st_folium(m, width=900, height=500)

st.divider()
st.subheader("🚀 Project Roadmap")
st.checkbox("Phase 1: 2D Basic Routing", value=True)
st.checkbox("Phase 2: 3D Pydeck Visualization", value=True)
st.checkbox("Phase 3: Multi-Page Storytelling", value=True)
st.checkbox("Phase 4: Real-time Traffic API Integration", value=False)
st.checkbox("Phase 5: Drone-Specific Physics (Battery/Wind)", value=False)
