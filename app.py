import streamlit as st
import random
import matplotlib.pyplot as plt

st.title("🚀 Nexus-Route: Logistics Optimizer")

# Generate random package locations
def generate_packages(n=50):
    return [(random.randint(0, 100), random.randint(0, 100)) for _ in range(n)]

packages = generate_packages()

# Separate X and Y
x = [p[0] for p in packages]
y = [p[1] for p in packages]

# Plot
fig, ax = plt.subplots()
ax.scatter(x, y)

# Label points
for i, (x_coord, y_coord) in enumerate(packages):
    ax.text(x_coord, y_coord, str(i), fontsize=8)

st.pyplot(fig)
