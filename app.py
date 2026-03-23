import streamlit as st
import random
import matplotlib.pyplot as plt
import numpy as np
from ortools.constraint_solver import pywrapcp

st.title("🚀 Nexus-Route: Logistics Optimizer")

# -----------------------------
# STEP 1: Generate Packages
# -----------------------------
def generate_packages(n=50):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

packages = generate_packages()

# -----------------------------
# STEP 2: Create Distance Matrix
# -----------------------------
def create_distance_matrix(locations):
    size = len(locations)
    matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            matrix[i][j] = ((locations[i][0] - locations[j][0]) ** 2 +
                            (locations[i][1] - locations[j][1]) ** 2) ** 0.5
    return matrix

distance_matrix = create_distance_matrix(packages)

# -----------------------------
# STEP 3: Solve TSP
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

route = solve_tsp(distance_matrix)

# -----------------------------
# STEP 4: Plot
# -----------------------------
fig, ax = plt.subplots()

# Plot points
x = [p[0] for p in packages]
y = [p[1] for p in packages]

ax.scatter(x, y)

# Label points
for i, (x_coord, y_coord) in enumerate(packages):
    ax.text(x_coord, y_coord, str(i), fontsize=8)

# Draw route
route_x = [packages[i][0] for i in route]
route_y = [packages[i][1] for i in route]

ax.plot(route_x, route_y)

# Show in Streamlit
st.pyplot(fig)
