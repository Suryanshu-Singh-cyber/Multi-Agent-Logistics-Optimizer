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



st.set_page_config(page_title="Logistics Digital Twin", layout="wide", page_icon="🚚")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #3e4255;
    }
    .feature-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #00f2ff;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HERO SECTION ---
st.title("🛰️ Multi-Agent Logistics: The 4D Digital Twin")
st.subheader("Solving the 'Last-Mile' Problem with AI and Spatio-Temporal Intelligence")

st.image("https://images.unsplash.com/photo-1586769852044-692d6e3703f0?auto=format&fit=crop&q=80&w=2000", 
         caption="Next-Gen Autonomous Routing Simulation")

st.divider()

# --- THE PROBLEM STORY ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>🚨 The Problem: Static Logistics is Failing</h3>
        <p>In cities like <b>New Delhi</b>, traffic and weather aren't just inconveniences—they are variables that break standard routing algorithms. 
        Traditional maps only show <b>Where</b> things are. They ignore <b>When</b> things happen.</p>
        <ul>
            <li><b>Inefficiency:</b> Vans getting stuck in predictable peak-hour traffic.</li>
            <li><b>Safety:</b> Drones running out of battery because of unexpected headwinds.</li>
            <li><b>Waste:</b> High CO2 emissions due to non-optimized idling.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.lottie = "https://assets5.lottiefiles.com/packages/lf20_kz9pjc9x.json" # Placeholder for animation logic
    st.info("💡 **Did you know?** Last-mile delivery accounts for 53% of total shipping costs. Optimization isn't just cool—it's profitable.")

# --- THE 4D SOLUTION ---
st.header("🛠️ Our Solution: The 4D Approach")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 📍 Phase 1: Optimizer")
    st.write("Using **Google OR-Tools**, we calculate the mathematically perfect route for multiple agents simultaneously.")

with c2:
    st.markdown("### ⛈️ Phase 2: Stress-Testing")
    st.write("We inject **Real-World Physics** (Rain, Wind, Battery Drain) into the simulation to see how the plan survives chaos.")

with c3:
    st.markdown("### 📊 Phase 3: 4D Twin")
    st.write("A high-fidelity **Digital Twin** visualizes the fleet's execution across space and time in a 3D environment.")

# --- TECH STACK RADAR ---
st.divider()
st.header("🧬 The Tech Stack")
tech_col1, tech_col2, tech_col3, tech_col4 = st.columns(4)

tech_col1.metric("Language", "Python 3.10")
tech_col2.metric("Intelligence", "OR-Tools / ML")
tech_col3.metric("Visualization", "PyDeck / 4D")
tech_col4.metric("Interface", "Streamlit Cloud")

# --- NAVIGATION CALL TO ACTION ---
st.divider()
st.success("👈 **Ready to explore? Use the Sidebar to navigate through the Optimizer and the 4D Simulator.**")

st.markdown("""
    ---
    **Built for the South Asian University Research Sprint** *Developer: Suryanshu Singh* *Focus: Multi-Agent Systems & Robotics*
""")
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
