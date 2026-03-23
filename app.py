import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from ortools.constraint_solver import pywrapcp

st.title("🚀 Nexus-Route: Multi-Agent Logistics Optimizer")

# -----------------------------
# STEP 1: Generate Packages
# -----------------------------
def generate_packages(n=50):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

packages = generate_packages()
points = np.array(packages)

# -----------------------------
# STEP 2: Clustering (5 Vans)
# -----------------------------
kmeans = KMeans(n_clusters=5, random_state=0)
labels = kmeans.fit_predict(points)

# -----------------------------
# STEP 3: Distance Matrix
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
# STEP 4: Solve TSP
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
# STEP 5: Plot Multi-Agent Routes
# -----------------------------
fig, ax = plt.subplots()

colors = ['red', 'blue', 'green', 'purple', 'orange']

for cluster_id in range(5):
    cluster_points = points[labels == cluster_id]

    # Skip if too small
    if len(cluster_points) < 2:
        continue

    distance_matrix = create_distance_matrix(cluster_points)
    route = solve_tsp(distance_matrix)

    route_points = cluster_points[route]

    # Plot points
    ax.scatter(cluster_points[:, 0], cluster_points[:, 1],
               color=colors[cluster_id], label=f"Van {cluster_id+1}")

    # Label points
    for i, (x_coord, y_coord) in enumerate(cluster_points):
        ax.text(x_coord, y_coord, str(i), fontsize=7)

    # Plot route
    ax.plot(route_points[:, 0], route_points[:, 1],
            color=colors[cluster_id])

ax.legend()
st.pyplot(fig)
