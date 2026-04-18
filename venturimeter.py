import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Venturi Flow Simulation")

# ---------------------------
# FUNCTIONS
# ---------------------------
def area(d):
    return np.pi * (d / 2) ** 2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2 * dp) / (rho * ((A1 / A2) ** 2 - 1)))
    v1 = (A2 / A1) * v2

    return v1, v2

def venturi_shape(d1, d2):
    x = np.linspace(0, 10, 100)

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
# PARTICLE SIMULATION
# ---------------------------
def simulate(d1, d2, v1, v2):

    x, y = venturi_shape(d1, d2)

    # persist particles
    if "particles" not in st.session_state:
        st.session_state.particles = np.linspace(0, 10, 20)

    particles = st.session_state.particles

    fig, ax = plt.subplots()
    placeholder = st.empty()

    for _ in range(60):
        ax.clear()

        # draw pipe
        ax.plot(x, y, color="black")
        ax.plot(x, -y, color="black")
        ax.fill_between(x, y, -y, alpha=0.1)

        # move particles
        for i in range(len(particles)):
            pos = particles[i]

            if pos < 3:
                pos += v1 * 0.02
            elif 3 <= pos <= 7:
                pos += v2 * 0.02
            else:
                pos += v1 * 0.02

            if pos > 10:
                pos = 0

            particles[i] = pos

            ax.plot(pos, 0, "bo")

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1, d1)
        ax.set_title("Venturi Flow")

        placeholder.pyplot(fig, clear_figure=True)
        time.sleep(0.03)

    st.session_state.particles = particles

# ---------------------------
# UI INPUTS
# ---------------------------
d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.4)
d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
dp = st.slider("Pressure Difference", 100, 5000, 1000)
rho = st.slider("Density", 500, 1500, 1000)

v1, v2 = velocity(d1, d2, dp, rho)

st.write(f"Inlet Velocity: {v1:.2f} m/s")
st.write(f"Throat Velocity: {v2:.2f} m/s")

# ---------------------------
# RUN SIMULATION
# ---------------------------
if st.button("Start Simulation"):
    simulate(d1, d2, v1, v2)
