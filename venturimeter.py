import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(layout="wide")

# ---------------------------
# CORE FUNCTIONS
# ---------------------------
def area(d):
    return np.pi * (d / 2) ** 2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2 * dp) / (rho * ((A1 / A2) ** 2 - 1)))
    v1 = (A2 / A1) * v2

    return v1, v2

# ---------------------------
# VENTURI SHAPE
# ---------------------------
def venturi_shape(d1, d2):
    x = np.linspace(0, 10, 200)

    y = np.piecewise(
        x,
        [x < 3, (x >= 3) & (x <= 7), x > 7],
        [
            lambda x: d1 / 2,
            lambda x: d1 / 2 - (d1 - d2) / 2 * ((x - 3) / 4),
            lambda x: d1 / 2,
        ],
    )
    return x, y

# ---------------------------
# INIT PARTICLES
# ---------------------------
if "particles" not in st.session_state:
    st.session_state.particles = np.linspace(0, 10, 40)

# ---------------------------
# ANIMATION FUNCTION
# ---------------------------
def animate(d1, d2, v1, v2):
    x, y = venturi_shape(d1, d2)

    particles = st.session_state.particles

    fig = go.Figure()

    # pipe shape
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='black')))
    fig.add_trace(go.Scatter(x=x, y=-y, mode='lines', line=dict(color='black')))

    # update particles
    new_particles = []

    for pos in particles:

        if pos < 3:
            pos += v1 * 0.05
        elif 3 <= pos <= 7:
            pos += v2 * 0.05
        else:
            pos += v1 * 0.05

        if pos > 10:
            pos = 0

        new_particles.append(pos)

    st.session_state.particles = new_particles

    # particle colors (pressure)
    colors = ["red" if 3 <= p <= 7 else "blue" for p in new_particles]

    fig.add_trace(go.Scatter(
        x=new_particles,
        y=[0]*len(new_particles),
        mode='markers',
        marker=dict(size=8, color=colors)
    ))

    fig.update_layout(
        title="Venturi Flow Simulation",
        xaxis=dict(range=[0,10], showgrid=False, visible=False),
        yaxis=dict(range=[-d1, d1], showgrid=False, visible=False),
        height=400
    )

    return fig

# ---------------------------
# UI
# ---------------------------
st.title("🚰 Venturi Meter Interactive Simulation")

col1, col2 = st.columns([1, 2])

# CONTROLS
with col1:
    st.subheader("Controls")

    d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
    d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
    dp = st.slider("Pressure Difference", 100, 5000, 1000)
    rho = st.slider("Fluid Density", 500, 1500, 1000)

    v1, v2 = velocity(d1, d2, dp, rho)

    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

    st.markdown("### 🔵 High Pressure | 🔴 Low Pressure")

# SIMULATION
with col2:
    st.subheader("Simulation")

    chart = st.empty()

    # smooth animation loop
    for _ in range(200):
        fig = animate(d1, d2, v1, v2)
        chart.plotly_chart(fig, use_container_width=True)
        time.sleep(0.03)
