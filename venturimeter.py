import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# CLASS 1:Venturi Meter

class VenturiMeter:
    def __init__(self, inlet, throat):
        self.inlet = inlet
        self.throat = throat

    def area(self, d):
        return np.pi * (d / 2) ** 2

    def get_area(self):
        return self.area(self.inlet), self.area(self.throat)
        
# CLASS 2:Fluid

class Fluid:
    def __init__(self, density):
        self.density = density



# CLASS 3:Flow Calculator

class FlowCalculator:
    def __init__(self, venturi, fluid, delta_p):
        self.venturi = venturi
        self.fluid = fluid
        self.delta_p = delta_p

    def calculate_velocity(self):
        A1, A2 = self.venturi.get_area()
        rho = self.fluid.density

        v2 = np.sqrt((2 * self.delta_p) / (rho * ((A1 / A2) ** 2 - 1)))
        v1 = (A2 / A1) * v2

        return v1, v2

    def calculate_flow_rate(self):
        A1, _ = self.venturi.get_area()
        v1, _ = self.calculate_velocity()
        return A1 * v1

# CLASS 4:Visualizer

class Visualizer:

    def plot_velocity(self, v1, v2):
        fig, ax = plt.subplots()
        ax.bar(['Inlet', 'Throat'], [v1, v2])
        ax.set_ylabel("Velocity (m/s)")
        ax.set_title("Velocity Comparison")
        return fig

    def plot_venturi_shape(self, d1, d2):
        x = np.linspace(0, 10, 100)

        y_upper = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x <= 7), x > 7],
            [
                lambda x: d1 / 2,
                lambda x: d1 / 2 - (d1 - d2) / 2 * ((x - 3) / 4),
                lambda x: d1 / 2,
            ],
        )

        y_lower = -y_upper

        fig, ax = plt.subplots()
        ax.plot(x, y_upper)
        ax.plot(x, y_lower)
        ax.fill_between(x, y_upper, y_lower, alpha=0.3)
        ax.set_title("Venturi Shape")
        return fig

    def simulate_real_flow(self, d1, d2):
        x = np.linspace(0, 10, 100)

        y_upper = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x <= 7), x > 7],
            [
                lambda x: d1 / 2,
                lambda x: d1 / 2 - (d1 - d2) / 2 * ((x - 3) / 4),
                lambda x: d1 / 2,
            ],
        )

        y_lower = -y_upper

        fig, ax = plt.subplots()
        placeholder = st.empty()

        particles = np.linspace(0, 10, 15)

        for frame in range(40):
            ax.clear()

            ax.plot(x, y_upper)
            ax.plot(x, y_lower)
            ax.fill_between(x, y_upper, y_lower, alpha=0.2)

            for i in range(len(particles)):
                pos = (particles[i] + frame * 0.2) % 10

                if 3 <= pos <= 7:
                    speed = 1.5
                else:
                    speed = 1.0

                ax.plot(pos, 0, "bo")

            ax.set_xlim(0, 10)
            ax.set_ylim(-d1, d1)
            ax.set_title("Flow Simulation")

            placeholder.pyplot(fig)
            time.sleep(0.1)

#Streamlit

st.title("🚰 Venturi Meter Flow Simulator")

menu = st.sidebar.selectbox("Select", ["Simulation", "Notes", "Quiz"])

#Simulation

if menu == "Simulation":
    st.header("Simulation")

    d1 = st.sidebar.number_input("Inlet Diameter", 0.1, 1.0, 0.2)
    d2 = st.sidebar.number_input("Throat Diameter", 0.05, 0.5, 0.1)
    dp = st.sidebar.number_input("Pressure Difference", 100, 5000, 1000)
    rho = st.sidebar.number_input("Density", 500, 2000, 1000)

    venturi = VenturiMeter(d1, d2)
    fluid = Fluid(rho)
    calc = FlowCalculator(venturi, fluid, dp)
    viz = Visualizer()

    v1, v2 = calc.calculate_velocity()
    Q = calc.calculate_flow_rate()

    st.write(f"Inlet Velocity: {v1:.2f}")
    st.write(f"Throat Velocity: {v2:.2f}")
    st.write(f"Flow Rate: {Q:.4f}")

    st.pyplot(viz.plot_velocity(v1, v2))

    st.subheader("🔬 Flow Simulation")
    if st.button("Start Simulation"):
        viz.simulate_real_flow(d1, d2)

#Notes

elif menu == "Notes":
    st.header("Interactive Notes")

    viz = Visualizer()

    term = st.selectbox("Learn Concept",
                        ["Select", "Bernoulli", "Continuity", "Flow Rate"])

    if term == "Bernoulli":
        st.info("Energy conservation in fluid flow")
    elif term == "Continuity":
        st.info("A1V1 = A2V2")
    elif term == "Flow Rate":
        st.info("Q = A × V")

    with st.expander("Visual"):
        d1 = st.slider("Inlet Diameter", 0.1, 1.0, 0.2)
        d2 = st.slider("Throat Diameter", 0.05, 0.5, 0.1)

        st.pyplot(viz.plot_venturi_shape(d1, d2))

        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/6/6f/Venturi_effect.svg",
            use_container_width=True
        )

        if st.button("Animate Flow"):
            viz.simulate_real_flow(d1, d2)
#Quiz

elif menu == "Quiz":
    st.header("Quiz")

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.level = "Easy"

    st.write(f"Score: {st.session_state.score}")
    st.write(f"Level: {st.session_state.level}")

    if st.session_state.level == "Easy":
        q = st.radio("Velocity when diameter decreases?",
                     ["Increase", "Decrease"])

        if st.button("Submit"):
            if q == "Increase":
                st.session_state.score += 1
                st.session_state.level = "Medium"

    elif st.session_state.level == "Medium":
        q = st.radio("Pressure at throat?",
                     ["Increase", "Decrease"])

        if st.button("Submit"):
            if q == "Decrease":
                st.session_state.score += 1
                st.session_state.level = "Hard"

    elif st.session_state.level == "Hard":
        q = st.radio("Principle used?",
                     ["Bernoulli", "Newton"])

        if st.button("Submit"):
            if q == "Bernoulli":
                st.session_state.score += 1
                st.success(f"Final Score: {st.session_state.score}/3")
                st.balloons()
