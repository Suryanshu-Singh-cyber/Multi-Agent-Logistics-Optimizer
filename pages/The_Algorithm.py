import streamlit as st

st.set_page_config(page_title="The Brain: Optimization Logic", layout="centered")

st.title("🤖 The Optimization Brain")
st.write("How do multiple agents decide who goes where?")

# --- SECTION 1: THE MATH ---
st.header("1. The Mathematical Objective")
st.write("We model this as a **Vehicle Routing Problem (VRP)**. Our goal is to minimize the total cost $C$:")

st.latex(r'''
C = \sum_{i,j \in A} d_{ij} \cdot x_{ij}
''')

st.info("""
**Where:**
* $d_{ij}$ is the distance between point $i$ and point $j$.
* $x_{ij}$ is a binary variable (1 if the van travels that path, 0 if not).
* We also add constraints to ensure each package is picked up exactly once!
""")

# --- SECTION 2: MULTI-AGENT NEGOTIATION ---
st.header("2. Multi-Agent Logic Flow")

col1, col2 = st.columns(2)

with col1:
    st.subheader("The 'Central' Manager")
    st.write("""
    - Receives all 100+ package coordinates.
    - Clusters them using **K-Means** or **Distance Matrices**.
    - Assigns 'zones' to each agent to prevent overlapping.
    """)

with col2:
    st.subheader("The 'Mobile' Agents")
    st.write("""
    - Calculate the local 'Shortest Path' in their zone.
    - Report back if a route is blocked (Traffic Simulation).
    - Can 'hand off' a package if another agent is closer.
    """)

# --- SECTION 3: INTERACTIVE EXPLANATION ---
st.header("3. Why Google OR-Tools?")
st.write("Instead of checking every path (which would take years), we use **Heuristics**.")

tab1, tab2 = st.tabs(["First Solution Strategy", "Local Search"])

with tab1:
    st.write("**Path Cheapest Arc:** We start by always picking the closest unvisited neighbor.")
    st.code("search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)")

with tab2:
    st.write("**Guided Local Search:** Once we have a route, we 'wiggle' the lines to see if we can save another 5% of fuel.")
    st.code("search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)")

st.success("Check out the 3D Simulator in the sidebar to see these algorithms in action!")
