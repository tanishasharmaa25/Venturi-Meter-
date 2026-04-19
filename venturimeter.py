import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

#Core Function
def area(d):
    return np.pi * (d / 2) ** 2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2 * dp) / (rho * ((A1 / A2) ** 2 - 1)))
    v1 = (A2 / A1) * v2

    return v1, v2

# Venturi shape

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

#Pressure colour Function

def pressure_colour(x):
    # High pressure : blue, low pressure : red
    if 3 <= x <= 7:
        return "red"   #low pressure
    else:
        return "blue"  #high pressure

#Animation

def animate(d1, d2, v1, v2):
    x, y = venturi_shape(d1, d2)

    fig, ax = plt.subplots()
    placeholder = st.empty()

    particles = np.linspace(0, 10, 30)

    for frame in range(80):
        ax.clear()

        #Pipe walls
        ax.plot(x, y, color="black")
        ax.plot(x, -y, color="black")

        #Pressure shading
        for i in range(len(x)-1):
            color = "lightblue" if x[i] < 3 or x[i] > 7 else "lightcoral"
            ax.fill_between([x[i], x[i+1]], y[i], -y[i], color=color, alpha=0.2)

        #Particle motion
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

            ax.plot(pos, 0, "o", color=pressure_colour(pos))

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1, d1)
        ax.set_title("Venturi Flow Simulation")

        placeholder.pyplot(fig)
        time.sleep(0.05)
        
#Velocity Graph

def plot_velocity_graph(d1, d2, v1, v2):
    x = np.linspace(0, 10, 200)

    v = np.piecewise(
        x,
        [x < 3, (x >= 3) & (x <= 7), x > 7],
        [
            lambda x: v1,
            lambda x: v2,
            lambda x: v1,
        ],
    )

    fig, ax = plt.subplots()
    ax.plot(x, v)
    ax.set_title("Velocity Variation Along Venturi")
    ax.set_xlabel("Position")
    ax.set_ylabel("Velocity (m/s)")

    return fig

#UI
st.title("Venturi Meter Interactive Simulation")

col1, col2 = st.columns([1, 2])

#Controls
with col1:
    st.subheader("Controls")

    d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
    d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
    dp = st.slider("Pressure Difference", 100, 5000, 1000)
    rho = st.slider("Fluid Density", 500, 1500, 1000)

    v1, v2 = velocity(d1, d2, dp, rho)

    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

    st.markdown("### 🔵 High Pressure
    | 🔴 Low Pressure")

#Simulation
with col2:
    st.subheader("Simulation")

    animate(d1, d2, v1, v2)

     st.subheader("Velocity Graph")
    fig = plot_velocity_graph(d1,d2,v1,v2)
    st.pyplot(fig)
