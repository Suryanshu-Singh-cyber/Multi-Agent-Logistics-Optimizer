import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from ortools.constraint_solver import pywrapcp

st.title("🚀 Nexus-Route: Cooperative Multi-Agent System")

# -----------------------------
# STEP 1: Generate Packages
# -----------------------------
def generate_packages(n=50):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

packages = generate_packages()
points = np.array(packages)

# -----------------------------
# STEP 2: Clustering
# -----------------------------
kmeans = KMeans(n_clusters=5, random_state=0)
labels = kmeans.fit_predict(points)

# -----------------------------
# STEP 3: Agent State
# -----------------------------
agents = []

for i in range(5):
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
# STEP 4: Distance Function
# -----------------------------
def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# -----------------------------
# STEP 5: REALLOCATION LOGIC 🔥
# -----------------------------
for agent in agents:
    if agent["status"] == "Low Battery ⚠️":
        for pkg in agent["packages"]:
            best_agent = None
            best_dist = float("inf")

            for other in agents:
                if other["status"] == "Active":
                    # Compare with center of cluster
                    center = np.mean(other["packages"], axis=0) if len(other["packages"]) > 0 else [0,0]
                    d = distance(pkg, center)

                    if d < best_dist:
                        best_dist = d
                        best_agent = other

            if best_agent:
                best_agent["packages"].append(pkg)

        # Clear packages from failed agent
        agent["packages"] = []

# -----------------------------
# STEP 6: Distance Matrix
# -----------------------------
def create_distance_matrix(locations):
    size = len(locations)
    matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            matrix[i][j] = ((locations[i][0] - locations[j][0]) ** 2 +
                            (locations[i][1] - locations[j][1]) ** 2) ** 0.5
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
# STEP 8: Plot
# -----------------------------
fig, ax = plt.subplots()
colors = ['red', 'blue', 'green', 'purple', 'orange']

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

    ax.scatter(cluster_points[:, 0], cluster_points[:, 1],
               color=colors[agent["id"]], label=f"Van {agent['id']}")

    ax.plot(route_points[:, 0], route_points[:, 1],
            color=colors[agent["id"]])

# -----------------------------
# STEP 9: Sidebar Info
# -----------------------------
st.sidebar.header("🚚 Agent Status")

for agent in agents:
    st.sidebar.write(
        f"Van {agent['id']} | Battery: {agent['battery']}% | Packages: {len(agent['packages'])} | Status: {agent['status']}"
    )

ax.legend()
st.pyplot(fig)
