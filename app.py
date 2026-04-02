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
        min-height: 200px;
    }
    .feature-card:hover { 
        transform: translateY(-8px); 
        border-top: 4px solid #ff00ff; 
        box-shadow: 0px 10px 30px rgba(0, 242, 255, 0.2);
    }
    .pipeline-step {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #3e4255;
    }
    .hero-text { font-size: 3.5rem; font-weight: 800; color: white; margin-bottom: 5px; line-height: 1.1; }
    .highlight { color: #00f2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
col_hero1, col_hero2 = st.columns([1, 1])

with col_hero1:
    st.markdown('<p class="hero-text">The 4D Fleet <span style="color:#00f2ff;">Digital Twin</span></p>', unsafe_allow_html=True)
    st.markdown("""
        ### **Bridging Mathematical Optimization and Real-World Chaos.**
        This dashboard isn't a map; it's a **Cyber-Physical Simulation**. It transforms static route plans into a dynamic, 
        physics-aware environment, solving the complex 'Last-Mile' puzzle for autonomous networks in New Delhi.
    """)
    st.divider()
    st.success("👈 **Explore the System:** Select '4D Simulator' or 'QA Tester' in the sidebar.")

with col_hero2:
    st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=1600&auto=format&fit=crop", 
             caption="Real-time Multi-Agent Fleet Synchronization Engine", use_container_width=True)

st.divider()

# --- NEW: PROJECT PIPELINE SECTION ---
st.header("🛠️ Project Pipeline & Data Workflow")
p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    st.markdown("""<div class="pipeline-step"><h3>📥</h3><b>Data Ingestion</b><br><small>Raw CSV/Excel Upload</small></div>""", unsafe_allow_html=True)
with p2:
    st.markdown("""<div class="pipeline-step"><h3>⚙️</h3><b>Optimization</b><br><small>OR-Tools Heuristics</small></div>""", unsafe_allow_html=True)
with p3:
    st.markdown("""<div class="pipeline-step"><h3>⛈️</h3><b>Physics Injector</b><br><small>Environment Stress-Test</small></div>""", unsafe_allow_html=True)
with p4:
    st.markdown("""<div class="pipeline-step"><h3>🛰️</h3><b>4D Mapping</b><br><small>Temporal Visualization</small></div>""", unsafe_allow_html=True)
with p5:
    st.markdown("""<div class="pipeline-step"><h3>📄</h3><b>Reporting</b><br><small>Automated PDF Manifest</small></div>""", unsafe_allow_html=True)

st.divider()

# --- THE THREE PILLARS ---
st.header("🚀 System Intelligence & Digital Twin Architecture")

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
        <p>High-fidelity <b>4D Visualization</b> with PyDeck GL. Watch 'comet-trail' telemetry predict fleet positions with sub-second accuracy.</p>
        <p class="highlight">WebGL Visualization</p>
    </div>
    """, unsafe_allow_html=True)

# --- TECH STACK ---
st.divider()
st.header("🧬 Engineering Core")
t1, t2, t3, t4 = st.columns(4)
t1.metric("Logic", "Python 3.10")
t2.metric("Intelligence", "OR-Tools")
t3.metric("Visualization", "PyDeck GL")
t4.metric("UX Framework", "Streamlit")

# --- FOOTER ---
st.divider()
st.markdown(f"""
    <div style="text-align: center; color: gray; padding: 20px;">
        Developed by <b>Suryanshu Singh</b> | South Asian University<br>
        <i>Specialization: Spiking Neural Networks, Robotics, & Event-Based Vision</i>
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
