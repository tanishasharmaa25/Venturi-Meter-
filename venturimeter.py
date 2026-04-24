import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# =========================
# CLASS 1: VENTURI METER
# =========================
class VenturiMeter:
    
    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

    def area(self, d):
        return np.pi * (d/2)**2

    def get_areas(self):
        return self.area(self.d1), self.area(self.d2)

    def shape(self):
        x = np.linspace(0, 10, 400)

        y = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x <= 7), x > 7],
            [
                lambda x: self.d1/2,
                lambda x: self.d2/2 + (self.d1 - self.d2)/2 * (1 + np.cos(np.pi*(x-3)/4))/2,
                lambda x: self.d1/2
            ]
        )
        return x, y


# =========================
# CLASS 2: FLUID
# =========================
class Fluid:
    
    def __init__(self, density):
        self.rho = density


# =========================
# CLASS 3: FLOW CALCULATOR
# =========================
class FlowCalculator:
    
    def __init__(self, venturi, fluid, dp):
        self.venturi = venturi
        self.fluid = fluid
        self.dp = dp

    def velocity(self):
        A1, A2 = self.venturi.get_areas()
        rho = self.fluid.rho

        v2 = np.sqrt((2*self.dp) / (rho*((A1/A2)**2 - 1)))
        v1 = (A2/A1) * v2

        return v1, v2

    def pressure_distribution(self, x, v1, v2):
        pressure = []

        for xi in x:
            if xi < 3 or xi > 7:
                v = v1
            else:
                v = v2

            P = 0.5 * self.fluid.rho * (v1**2 - v**2)
            pressure.append(P)

        return np.array(pressure)


# =========================
# CLASS 4: SIMULATION
# =========================
class Simulation:
    
    def __init__(self, venturi, flow_calc):
        self.venturi = venturi
        self.flow_calc = flow_calc

    def animate(self, v1, v2):
        x, y = self.venturi.shape()
        pressure = self.flow_calc.pressure_distribution(x, v1, v2)

        placeholder = st.empty()

        # 🔥 WATER LAYERS (continuous flow)
        layers_y = np.linspace(-self.venturi.d1/2, self.venturi.d1/2, 20)
        offsets = np.zeros(len(layers_y))

        for frame in range(150):
            fig, ax = plt.subplots(figsize=(18,6))

            # Pipe walls
            ax.plot(x, y, color='black', linewidth=2)
            ax.plot(x, -y, color='black', linewidth=2)

            # Pressure gradient
            norm = (pressure - pressure.min()) / (pressure.max() - pressure.min())

            for i in range(len(x)-1):
                ax.fill_between(
                    [x[i], x[i+1]],
                    y[i],
                    -y[i],
                    color=plt.cm.coolwarm(norm[i]),
                    alpha=0.4
                )

            # 🔥 FLOWING WATER (REAL VISUAL)
            for i, y_layer in enumerate(layers_y):

                offsets[i] += 0.05

                wave = 0.02 * np.sin(5 * x + offsets[i])

                velocity_profile = np.where((x < 3) | (x > 7), v1, v2)

                flow_x = x + velocity_profile * offsets[i]

                ax.plot(flow_x, y_layer + wave,
                        color='white',
                        linewidth=1.2,
                        alpha=0.7)

            ax.set_xlim(0, 10)
            ax.set_ylim(-self.venturi.d1, self.venturi.d1)

            ax.axis('off')
            ax.set_title("Water Flow Through Venturi Meter", fontsize=18)

            plt.tight_layout()
            placeholder.pyplot(fig, use_container_width=True)
            time.sleep(0.03)

    def velocity_graph(self, v1, v2):
        x = np.linspace(0, 10, 200)
        velocity = []

        for xi in x:
            if xi < 3 or xi > 7:
                velocity.append(v1)
            else:
                velocity.append(v2)

        fig, ax = plt.subplots(figsize=(12,5))

        ax.plot(x, velocity, linewidth=3)

        ax.set_title("Velocity Distribution Along Venturi Meter")
        ax.set_xlabel("Length of Pipe")
        ax.set_ylabel("Velocity (m/s)")
        ax.grid(True, linestyle='--', alpha=0.5)

        return fig


# =========================
# UI
# =========================
st.title("Venturi Meter Flow Simulation (OOP)")

col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Controls")

    d1 = st.slider("Inlet Diameter", 0.3, 1.0, 0.6)
    d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.3)
    dp = st.slider("Pressure Difference", 100, 5000, 1500)
    rho = st.slider("Fluid Density", 500, 1500, 1000)

    venturi = VenturiMeter(d1, d2)
    fluid = Fluid(rho)
    flow = FlowCalculator(venturi, fluid, dp)
    sim = Simulation(venturi, flow)

    v1, v2 = flow.velocity()

    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

    st.markdown("### 🔵 High Pressure | 🔴 Low Pressure")

    if st.button("Start Simulation"):
        sim.animate(v1, v2)

with col2:
    st.subheader("Velocity Graph")
    fig = sim.velocity_graph(v1, v2)
    st.pyplot(fig)
    flow = FlowCalculator(venturi, fluid, dp)
    sim = Simulation(venturi, flow)

    v1, v2 = flow.velocity()

    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

    st.markdown("### 🔵 High Pressure | 🔴 Low Pressure")

    if st.button("Start Simulation"):
        sim.animate(v1, v2)

with col2:
    st.subheader("Velocity Graph")
    fig = sim.velocity_graph(v1, v2)
    st.pyplot(fig)
