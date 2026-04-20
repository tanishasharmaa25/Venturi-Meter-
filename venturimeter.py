import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# -----------------------------
# Core Functions
# -----------------------------
def area(d):
    return np.pi * (d/2)**2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2*dp) / (rho*((A1 / A2)**2 - 1)))
    v1 = (A2 / A1)*v2

    return v1, v2 

# -----------------------------
# Venturi Shape
# -----------------------------
def venturishape(d1, d2):
    x = np.linspace(0, 10, 400)

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

# -----------------------------
# Animation (FIXED BIG VERSION)
# -----------------------------
def animate(d1, d2, v1, v2):

    x, y = venturishape(d1, d2)

    placeholder = st.empty()
    particles = np.linspace(0, 10, 40)

    for frame in range(100):

        # 🔥 BIG FIGURE (MAIN FIX)
        fig, ax = plt.subplots(figsize=(18, 6))

        # Pipe walls
        ax.plot(x, y, color="black", linewidth=2)
        ax.plot(x, -y, color="black", linewidth=2)

        # Fill pipe (better visuals)
        ax.fill_between(x, y, -y, color="lightblue", alpha=0.2)

        # Pressure shading
        for i in range(len(x)-1):
            color = "lightblue" if x[i] < 3 or x[i] > 7 else "lightcoral"
            ax.fill_between([x[i], x[i+1]], y[i], -y[i], color=color, alpha=0.15)

        # Particle motion
        for i in range(len(particles)):
            pos = particles[i]

            if pos < 3:
                pos += v1 * 0.08
            elif 3 <= pos <= 7:
                pos += v2 * 0.08
            else:
                pos += v1 * 0.08

            if pos > 10:
                pos = 0

            particles[i] = pos

            color = "blue" if pos < 3 or pos > 7 else "red"
            ax.plot(pos, 0, "o", color=color, markersize=6)

        # 🔥 BIG VISUAL SETTINGS
        ax.set_xlim(0, 10)
        ax.set_ylim(-d1*2, d1*2)

        ax.axis('off')  # remove axes → cleaner look

        ax.set_title("Venturi Flow Simulation", fontsize=18)

        plt.tight_layout()

        # 🔥 FULL WIDTH DISPLAY
        placeholder.pyplot(fig, use_container_width=True)

        time.sleep(0.02)

# -----------------------------
# Velocity Graph (Improved)
# -----------------------------
def plot_velocity_graph(v1, v2):
    fig, ax = plt.subplots(figsize=(10, 5))

    labels = ['Inlet', 'Throat']
    values = [v1, v2]

    bars = ax.bar(labels, values)

    bars[0].set_color('blue')
    bars[1].set_color('red')

    for i, v in enumerate(values):
        ax.text(i, v + 0.05, f"{v:.2f}", ha='center', fontweight='bold')

    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Velocity Comparison")
    ax.set_ylim(0, max(values) * 1.3)

    return fig

# -----------------------------
# UI
# -----------------------------
menu = st.sidebar.selectbox("Select Section", ["Simulation", "Notes", "Quiz"])

# -----------------------------
# SIMULATION (FULL WIDTH FIXED)
# -----------------------------
if menu == "Simulation":

    st.title("Venturi Meter Flow Simulation")

    # 🔥 Controls on top (NOT side-by-side anymore)
    st.subheader("Controls")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)

    with col2:
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)

    with col3:
        dp = st.slider("Pressure Difference", 100, 5000, 1000)

    with col4:
        rho = st.slider("Fluid Density", 500, 1500, 1000)

    v1, v2 = velocity(d1, d2, dp, rho)

    st.markdown("### Velocity Values")
    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

    st.markdown("🔵 High Pressure | 🔴 Low Pressure")

    if st.button("Start Simulation"):
        animate(d1, d2, v1, v2)

    st.subheader("Velocity Graph")
    fig = plot_velocity_graph(v1, v2)
    st.pyplot(fig, use_container_width=True)

# -----------------------------
# NOTES
# -----------------------------
elif menu == "Notes":

    st.header("Venturi Meter Notes")

    st.markdown("""
A Venturi meter works on the principle of the **Venturi Effect**, where fluid velocity increases as the cross-section decreases, causing pressure to drop.
""")

    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3d/Venturi_tube_diagram.svg")

    st.markdown("""
### Key Points:
- Narrow section → High velocity → Low pressure  
- Wide section → Low velocity → High pressure  
- Based on Bernoulli + Continuity equation  
""")

# -----------------------------
# QUIZ
# -----------------------------
elif menu == "Quiz":

    st.header("Quiz")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempted" not in st.session_state:
        st.session_state.attempted = 0

    question = st.radio(
        "Where is velocity maximum?",
        ["Inlet", "Throat", "Outlet"]
    )

    if st.button("Submit"):
        st.session_state.attempted += 1

        if question == "Throat":
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error("Wrong!")

    st.subheader("Score Board")
    st.metric("Score", st.session_state.score)
    st.metric("Attempted", st.session_state.attempted)

    if st.button("Reset Quiz"):
        st.session_state.score = 0
        st.session_state.attempted = 0
        st.rerun()
