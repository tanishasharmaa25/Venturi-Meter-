import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

    def calculate_velocity(self):
        A1, A2 = self.venturi.get_areas()
        rho = self.fluid.density

        v2 = np.sqrt((2 * self.dp) / (rho * ((A1 / A2) ** 2 - 1)))
        v1 = (A2 / A1) * v2

        return v1, v2

    def velocity_field(self):
        x, y = self.venturi.shape()
        A1, _ = self.venturi.get_areas()

        A_x = np.pi * (2 * y) ** 2 / 4
        v_x = A1 / A_x

        return x, y, v_x

    # ✅ FINAL STREAMLINE VISUALIZATION
    def draw_streamlines(self):
        x, y, v_x = self.velocity_field()

        # Grid
        Y_vals = np.linspace(-self.venturi.d1/2, self.venturi.d1/2, 100)
        X, Y = np.meshgrid(x, Y_vals)

        U = np.zeros_like(X)
        V = np.zeros_like(X)

        for i in range(len(x)):
            for j in range(len(Y_vals)):
                if abs(Y[j, i]) <= y[i]:

                    # Laminar profile
                    if y[i] != 0:
                        profile = 1 - (Y[j, i] / y[i])**2
                    else:
                        profile = 1

                    U[j, i] = v_x[i] * profile
                    V[j, i] = 0
                else:
                    U[j, i] = 0
                    V[j, i] = 0

        fig, ax = plt.subplots(figsize=(20, 8))

        # Pipe walls
        ax.plot(x, y, color="black", linewidth=2)
        ax.plot(x, -y, color="black", linewidth=2)

        # Speed for coloring
        speed = np.sqrt(U**2 + V**2)
        norm = speed / np.max(speed)

        # Streamlines
        ax.streamplot(
            X, Y, U, V,
            color=norm,
            cmap='plasma',
            density=2,
            linewidth=1.5
        )

        ax.set_xlim(0, 10)
        ax.set_ylim(-self.venturi.d1/2, self.venturi.d1/2)
        ax.set_title("Venturi Flow (Streamline Visualization)", fontsize=18)
        ax.axis("off")

        return fig

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
    st.title("Venturi Meter Flow Simulation (OOP + Streamlines)")

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

        if st.button("Show Flow"):
            st.pyplot(sim.draw_streamlines(), use_container_width=True)

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

Fluid accelerates at throat and pressure decreases.
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
