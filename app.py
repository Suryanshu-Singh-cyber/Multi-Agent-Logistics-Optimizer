import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from ortools.constraint_solver import pywrapcp

st.set_page_config(layout="wide")
st.title("🚀 Nexus-Route: Intelligent Multi-Agent Logistics System")

# -----------------------------
# UI CONTROLS
# -----------------------------
num_packages = st.sidebar.slider("📦 Number of Packages", 20, 100, 50)
num_agents = st.sidebar.slider("🚚 Number of Vans", 2, 8, 5)

simulate_traffic = st.sidebar.button("🚧 Simulate Traffic Jam")

# -----------------------------
# STEP 1: Generate Packages
# -----------------------------
def generate_packages(n=50):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

packages = generate_packages(num_packages)
points = np.array(packages)

# -----------------------------
# STEP 2: Clustering
# -----------------------------
kmeans = KMeans(n_clusters=num_agents, random_state=0)
labels = kmeans.fit_predict(points)

# -----------------------------
# STEP 3: Agent State
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
# STEP 4: AI NEGOTIATOR
# -----------------------------
def ai_negotiator(low_agent, agents):
    best_agent = None
    best_score = -1

    for agent in agents:
        if agent["status"] == "Active":
            score = agent["battery"] - len(agent["packages"]) * 2
            if score > best_score:
                best_score = score
                best_agent = agent

    return best_agent

# -----------------------------
# STEP 5: REALLOCATION (AI-based)
# -----------------------------
for agent in agents:
    if agent["status"] == "Low Battery ⚠️":
        for pkg in agent["packages"]:
            best_agent = ai_negotiator(agent, agents)
            if best_agent:
                best_agent["packages"].append(pkg)
        agent["packages"] = []

# -----------------------------
# STEP 6: Distance Matrix
# -----------------------------
def create_distance_matrix(locations):
    size = len(locations)
    matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            dist = ((locations[i][0] - locations[j][0]) ** 2 +
                    (locations[i][1] - locations[j][1]) ** 2) ** 0.5

            if simulate_traffic:
                dist *= random.uniform(1.2, 2.0)  # traffic increases cost

            matrix[i][j] = dist

    return matrix

# -----------------------------
# STEP 7: Solve TSP
# -----------------------------
def solve_tsp(distance_matrix):
    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return int(distance_matrix[
            manager.IndexToNode(from_index)][
            manager.IndexToNode(to_index)
        ])

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    solution = routing.SolveWithParameters(
        pywrapcp.DefaultRoutingSearchParameters()
    )

    route = []
    index = routing.Start(0)

    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))

    return route

# -----------------------------
# STEP 8: Visualization
# -----------------------------
fig, ax = plt.subplots()

colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan']

total_distance = 0

for agent in agents:
    cluster_points = np.array(agent["packages"])

    if len(cluster_points) < 2:
        continue

    if agent["status"] == "Low Battery ⚠️":
        ax.scatter(cluster_points[:, 0], cluster_points[:, 1],
                   color='black', label=f"Van {agent['id']} (Failed)")
        continue

    distance_matrix = create_distance_matrix(cluster_points)
    route = solve_tsp(distance_matrix)

    route_points = cluster_points[route]

    # distance calculation
    for i in range(len(route_points) - 1):
        total_distance += np.linalg.norm(route_points[i] - route_points[i+1])

    ax.scatter(cluster_points[:, 0], cluster_points[:, 1],
               color=colors[agent["id"]], label=f"Van {agent['id']}")

    ax.plot(route_points[:, 0], route_points[:, 1],
            color=colors[agent["id"]])

ax.legend()
st.pyplot(fig)

# -----------------------------
# STEP 9: METRICS DASHBOARD
# -----------------------------
active_vans = sum(1 for a in agents if a["status"] == "Active")

st.sidebar.header("📊 System Metrics")
st.sidebar.metric("Total Packages", num_packages)
st.sidebar.metric("Active Vans", active_vans)
st.sidebar.metric("Total Distance", round(total_distance, 2))

# -----------------------------
# STEP 10: AGENT STATUS
# -----------------------------
st.sidebar.header("🚚 Agent Status")

for agent in agents:
    st.sidebar.write(
        f"Van {agent['id']} | 🔋 {agent['battery']}% | 📦 {len(agent['packages'])} | {agent['status']}"
    )
