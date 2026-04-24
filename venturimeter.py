import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# -------------------------
# CLASS 1: Venturi Meter
# -------------------------

class VenturiMeter:
    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

    def area(self, d):
        return np.pi * (d / 2) ** 2

    def get_areas(self):
        return self.area(self.d1), self.area(self.d2)

    def shape(self):
        x = np.linspace(0, 10, 300)

        y = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x <= 7), x > 7],
            [
                lambda x: self.d1 / 2,
                lambda x: self.d1 / 2 - (self.d1 - self.d2) / 2 * ((x - 3) / 4),
                lambda x: self.d1 / 2,
            ],
        )
        return x, y


# -------------------------
# CLASS 2: Fluid
# -------------------------

class Fluid:
    def __init__(self, density):
        self.density = density


# -------------------------
# CLASS 3: Flow Simulator
# -------------------------

class FlowSimulator:
    def __init__(self, venturi, fluid, dp):
        self.venturi = venturi
        self.fluid = fluid
        self.dp = dp

    # Bernoulli + Continuity
    def calculate_velocity(self):
        A1, A2 = self.venturi.get_areas()
        rho = self.fluid.density

        v2 = np.sqrt((2 * self.dp) / (rho * ((A1 / A2) ** 2 - 1)))
        v1 = (A2 / A1) * v2

        return v1, v2

    # Velocity field along pipe
    def velocity_field(self):
        x, y = self.venturi.shape()
        A1, _ = self.venturi.get_areas()

        A_x = np.pi * (2 * y) ** 2 / 4
        v_x = A1 / A_x

        return x, y, v_x

    # FINAL REALISTIC ANIMATION
    def animate(self):
        x, y, v_x = self.velocity_field()

        placeholder = st.empty()

        num_particles = 600
        px = np.random.uniform(0, 10, num_particles)
        py = np.random.uniform(-self.venturi.d1 / 2, self.venturi.d1 / 2, num_particles)

        dt = 0.02

        fig, ax = plt.subplots(figsize=(20, 8))

        # Pipe walls
        ax.plot(x, y, color="black", linewidth=2)
        ax.plot(x, -y, color="black", linewidth=2)

        scatter = ax.scatter(px, py, s=5)

        ax.set_xlim(0, 10)
        ax.set_ylim(-self.venturi.d1, self.venturi.d1)
        ax.set_title("Realistic Venturi Flow", fontsize=18)
        ax.axis("off")

        for frame in range(250):

            colors = []

            for i in range(num_particles):
                idx = np.searchsorted(x, px[i])
                idx = np.clip(idx, 1, len(x)-1)

                # interpolate velocity
                x1, x2 = x[idx-1], x[idx]
                v1, v2 = v_x[idx-1], v_x[idx]
                v_local = v1 + (v2 - v1) * ((px[i] - x1) / (x2 - x1))

                # amplify for visibility
                v_local *= 2.5

                # laminar profile
                radius = y[idx]
                if radius != 0:
                    profile = (1 - (py[i]/radius)**2)
                else:
                    profile = 1

                v_local *= profile

                # move particle
                px[i] += v_local * dt

                if px[i] > 10:
                    px[i] = 0
                    py[i] = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2)

                # stay inside pipe
                y_limit = np.interp(px[i], x, y)
                if abs(py[i]) > y_limit:
                    py[i] = np.sign(py[i]) * y_limit * 0.95

                # color based on velocity
                norm = (v_local - np.min(v_x)) / (np.max(v_x) - np.min(v_x))
                colors.append(plt.cm.plasma(norm))

            scatter.set_offsets(np.c_[px, py])
            scatter.set_color(colors)

            placeholder.pyplot(fig, use_container_width=True)
            time.sleep(0.01)

    # Velocity graph
    def plot_graph(self):
        x, y, v_x = self.velocity_field()

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(x, v_x, linewidth=3)

        ax.set_title("Velocity Distribution Along Venturi")
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
    st.title("Venturi Meter Flow Simulation (OOP)")

    col1, col2 = st.columns([1, 2])

    with col1:
        d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
        dp = st.slider("Pressure Difference", 100, 5000, 1000)
        rho = st.slider("Fluid Density", 500, 1500, 1000)

        venturi = VenturiMeter(d1, d2)
        fluid = Fluid(rho)
        sim = FlowSimulator(venturi, fluid, dp)

        v1, v2 = sim.calculate_velocity()

        st.metric("Inlet Velocity", f"{v1:.2f} m/s")
        st.metric("Throat Velocity", f"{v2:.2f} m/s")

        if st.button("Start Simulation"):
            sim.animate()

    with col2:
        st.subheader("Velocity Graph")
        st.pyplot(sim.plot_graph())


# -------------------------
# NOTES
# -------------------------

elif menu == "Notes":
    st.header("Venturi Meter Notes")

    st.markdown("""
Venturi meter works on:
- Bernoulli’s Principle
- Continuity Equation

Velocity increases at throat → pressure decreases.
""")


# -------------------------
# QUIZ
# -------------------------

elif menu == "Quiz":
    st.header("Quiz")

    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempted" not in st.session_state:
        st.session_state.attempted = 0

    questions = [
        ("Velocity is maximum at?", ["Inlet", "Throat", "Outlet"], "Throat"),
        ("Pressure is lowest at?", ["Inlet", "Throat", "Outlet"], "Throat"),
        ("Which equation ensures conservation?", ["Bernoulli", "Continuity", "Newton"], "Continuity"),
    ]

    for i, (q, options, ans) in enumerate(questions):
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
