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
 #00f2ff; font-weight: bold; }

import streamlit as st

st.set_page_config(
    page_title="Logistics Digital Twin | 4D Fleet", 
    layout="wide", 
    page_icon="🛰️"
)

# --- CUSTOM CSS FOR PROFESSIONAL UI ---
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
        min-height: 220px;
    }
    .feature-card:hover { 
        transform: translateY(-10px); 
        border-top: 4px solid #ff00ff; 
        box-shadow: 0px 10px 20px rgba(0, 242, 255, 0.2);
    }
    .hero-text { font-size: 3rem; font-weight: 800; color: white; margin-bottom: 10px; line-height: 1.1; }
    .highlight { color: #00f2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
col_hero1, col_hero2 = st.columns([1.2, 1])

with col_hero1:
    st.markdown('<p class="hero-text">Predicting the Future of <span style="color:#00f2ff;">Autonomous Logistics</span></p>', unsafe_allow_html=True)
    st.markdown("""
        ### **A 4D Multi-Agent Digital Twin**
        This system transforms static route data into a living, breathing **Cyber-Physical Simulation**. 
        By modeling **Space, Time, and Environment**, we solve the 'Last-Mile' puzzle for the modern world.
    """)
    st.info("👈 **Get Started:** Select **4D Simulator** in the sidebar to watch the fleet in action.")

with col_hero2:
    # Reliable high-speed delivery/network image from Unsplash Source
    st.image("https://images.unsplash.com/photo-1580674684081-7617fbf3d745?q=80&w=1000&auto=format&fit=crop", 
             caption="Real-Time Fleet Execution Engine", use_container_width=True)

st.divider()

# --- THE THREE PILLARS ---
st.header("🛠️ Core System Architecture")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <h3>📍 01. Mathematical Optimization</h3>
        <p>Powered by <b>Google OR-Tools</b>. We find the global minimum for delivery time across multiple agents and complex drop-points.</p>
        <p class="highlight">Intelligence Engine</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <h3>⛈️ 02. Environmental Stress</h3>
        <p>Simulation of New Delhi's physics: <b>Rain, Wind, and Battery Decay</b>. Our 4D engine 'stretches' time based on real-world drag.</p>
        <p class="highlight">Physics-Aware</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <h3>🛸 03. Digital Twin Execution</h3>
        <p>High-fidelity <b>4D Visualization</b> with PyDeck. Watch 'comet-trail' telemetry predict fleet positions with sub-second accuracy.</p>
        <p class="highlight">WebGL Visualization</p>
    </div>
    """, unsafe_allow_html=True)

# --- TECH STACK ---
st.divider()
st.header("🧬 Tech Stack")
t1, t2, t3, t4 = st.columns(4)
t1.metric("Logic", "Python 3.10")
t2.metric("Intelligence", "OR-Tools")
t3.metric("Visualization", "PyDeck GL")
t4.metric("Interface", "Streamlit")

# --- FOOTER ---
st.divider()
st.markdown(f"""
    <div style="text-align: center; color: gray; padding: 20px;">
        Developed by <b>Suryanshu Singh</b> | South Asian University Research Sprint 2026<br>
        <i>Specialization: Spiking Neural Networks & Autonomous Systems</i>
    </div>
    """, unsafe_allow_html=True)
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
