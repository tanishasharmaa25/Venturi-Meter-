import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# ---------------------------
# CORE LOGIC
# ---------------------------
def area(d):
    return np.pi * (d/2)**2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2*dp)/(rho*((A1/A2)**2 - 1)))
    v1 = (A2/A1)*v2

    return v1, v2


# ---------------------------
# DRAW VENTURI
# ---------------------------
def venturi_shape(d1, d2):
    x = np.linspace(0, 10, 200)

    y = np.piecewise(
        x,
        [x < 3, (x>=3)&(x<=7), x>7],
        [lambda x: d1/2,
         lambda x: d1/2 - (d1-d2)/2*((x-3)/4),
         lambda x: d1/2]
    )
    return x, y


# ---------------------------
# ANIMATION
# ---------------------------
def animate(d1, d2, v2):
    x, y = venturi_shape(d1, d2)

    fig, ax = plt.subplots()
    placeholder = st.empty()

    particles = np.linspace(0, 10, 25)

    for frame in range(60):
        ax.clear()

        # pipe
        ax.plot(x, y, color="black")
        ax.plot(x, -y, color="black")
        ax.fill_between(x, y, -y, alpha=0.1)

        # particles
        for i in range(len(particles)):
            pos = (particles[i] + frame*0.1*v2) % 10

            # faster in throat
            speed = 2 if 3 <= pos <= 7 else 1
            ax.plot(pos, 0, "o")

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1, d1)
        ax.set_title("Flow Through Venturi Meter")

        placeholder.pyplot(fig)
        time.sleep(0.05)


# ---------------------------
# UI
# ---------------------------
st.title("Venturi Meter Interactive Simulation")

col1, col2 = st.columns([1, 2])

# LEFT: CONTROLS
with col1:
    st.subheader("Controls")

    d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
    d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
    dp = st.slider("Pressure Difference", 100, 5000, 1000)
    rho = st.slider("Density", 500, 1500, 1000)

    v1, v2 = velocity(d1, d2, dp, rho)

    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

# RIGHT: SIMULATION
with col2:
    st.subheader("Simulation")

    animate(d1, d2, v2)
