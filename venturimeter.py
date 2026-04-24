import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# -------------------------
# CORE PHYSICS FUNCTIONS
# -------------------------

def area(d):
    return np.pi * (d / 2) ** 2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2 * dp) / (rho * ((A1 / A2) ** 2 - 1)))
    v1 = (A2 / A1) * v2

    return v1, v2


# -------------------------
# VENTURI GEOMETRY
# -------------------------

def venturishape(d1, d2):
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


# -------------------------
# REALISTIC ANIMATION
# -------------------------

def animate_real(d1, d2, dp, rho):
    x, y = venturishape(d1, d2)

    A1 = area(d1)

    placeholder = st.empty()

    num_particles = 250
    particles_x = np.random.uniform(0, 10, num_particles)
    particles_y = np.random.uniform(-d1 / 2, d1 / 2, num_particles)

    for frame in range(150):
        fig, ax = plt.subplots(figsize=(20, 8))

        # Pipe walls
        ax.plot(x, y, color="black", linewidth=2)
        ax.plot(x, -y, color="black", linewidth=2)

        # Velocity field
        A_x = np.pi * (2 * y) ** 2 / 4
        v_x = A1 / A_x

        v_norm = (v_x - np.min(v_x)) / (np.max(v_x) - np.min(v_x))

        # Color field
        for i in range(len(x) - 1):
            ax.fill_between(
                [x[i], x[i + 1]],
                y[i],
                -y[i],
                color=plt.cm.jet(v_norm[i]),
                alpha=0.3,
            )

        # Particle motion
        for i in range(num_particles):
            px = particles_x[i]
            py = particles_y[i]

            idx = np.argmin(np.abs(x - px))

            local_area = np.pi * (2 * y[idx]) ** 2 / 4
            v_local = A1 / local_area

            px += v_local * 0.08

            if px > 10:
                px = 0

            if abs(py) > y[idx]:
                py = np.sign(py) * y[idx] * 0.9

            particles_x[i] = px
            particles_y[i] = py

            ax.scatter(px, py, color=plt.cm.jet(v_norm[idx]), s=10)

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1, d1)
        ax.set_title("Venturi Meter Flow (Realistic Simulation)", fontsize=18)
        ax.axis("off")

        placeholder.pyplot(fig, use_container_width=True)
        time.sleep(0.03)


# -------------------------
# REAL VELOCITY GRAPH
# -------------------------

def plot_velocity_real(d1, d2):
    x, y = venturishape(d1, d2)

    A1 = area(d1)
    A_x = np.pi * (2 * y) ** 2 / 4
    v_x = A1 / A_x

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(x, v_x, linewidth=3)

    ax.set_title("Velocity Variation Along Venturi")
    ax.set_xlabel("Pipe Length")
    ax.set_ylabel("Velocity")

    return fig


# -------------------------
# UI
# -------------------------

menu = st.sidebar.selectbox("Select Section", ["Simulation", "Notes", "Quiz"])

# -------------------------
# SIMULATION
# -------------------------

if menu == "Simulation":
    st.title("Venturi Meter Flow Simulation")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Controls")

        d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
        dp = st.slider("Pressure Difference", 100, 5000, 1000)
        rho = st.slider("Fluid Density", 500, 1500, 1000)

        v1, v2 = velocity(d1, d2, dp, rho)

        st.metric("Inlet Velocity", f"{v1:.2f} m/s")
        st.metric("Throat Velocity", f"{v2:.2f} m/s")

        if st.button("Start Simulation"):
            animate_real(d1, d2, dp, rho)

    with col2:
        st.subheader("Velocity Graph")
        fig = plot_velocity_real(d1, d2)
        st.pyplot(fig)


# -------------------------
# NOTES
# -------------------------

elif menu == "Notes":
    st.header("Venturi Meter Notes")

    tab1, tab2 = st.tabs(["Concept", "Derivation"])

    with tab1:
        st.subheader("What is Venturi Meter?")

        st.markdown("""
Venturi meter is used to measure flow rate in a pipe.

It works on **Bernoulli's Principle**:
- Velocity increases → Pressure decreases
        """)

        st.image("https://upload.wikimedia.org/wikipedia/commons/3/3d/Venturi_tube_diagram.svg")

    with tab2:
        st.subheader("Derivation")

        st.latex(r"A_1 v_1 = A_2 v_2")
        st.latex(r"P_1 + \frac{1}{2}\rho v_1^2 = P_2 + \frac{1}{2}\rho v_2^2")
        st.latex(r"v_2 = \sqrt{\frac{2\Delta P}{\rho\left(\left(\frac{A_1}{A_2}\right)^2 - 1\right)}}")


# -------------------------
# QUIZ
# -------------------------

elif menu == "Quiz":
    st.header("Quiz")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempted" not in st.session_state:
        st.session_state.attempted = 0
    if "weak_topics" not in st.session_state:
        st.session_state.weak_topics = []

    quiz_data = [
        ("Velocity is maximum at?", ["Inlet", "Throat", "Outlet"], "Throat"),
        ("Pressure is lowest at?", ["Inlet", "Throat", "Outlet"], "Throat"),
        ("Which equation ensures conservation?", ["Bernoulli", "Continuity", "Newton"], "Continuity"),
    ]

    for i, (q, options, ans) in enumerate(quiz_data):
        st.subheader(q)
        choice = st.radio("Select", options, key=i)

        if st.button("Submit", key=f"btn{i}"):
            st.session_state.attempted += 1
            if choice == ans:
                st.success("Correct")
                st.session_state.score += 1
            else:
                st.error(f"Wrong. Correct: {ans}")

    st.subheader("Score Board")
    st.metric("Score", st.session_state.score)
    st.metric("Attempted", st.session_state.attempted)

    if st.button("Reset"):
        st.session_state.score = 0
        st.session_state.attempted = 0
        st.rerun()
