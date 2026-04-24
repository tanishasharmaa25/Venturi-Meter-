import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# =========================
# VENTURI CLASS
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
# FLUID CLASS
# =========================
class Fluid:
    def __init__(self, rho):
        self.rho = rho


# =========================
# FLOW CALCULATOR
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

    def pressure(self, x, v1, v2):
        p = []
        for xi in x:
            if xi < 3 or xi > 7:
                v = v1
            else:
                v = v2
            p.append(0.5 * self.fluid.rho * (v1**2 - v**2))
        return np.array(p)


# =========================
# SIMULATION
# =========================
class Simulation:
    def __init__(self, venturi, flow):
        self.venturi = venturi
        self.flow = flow

    def animate(self, v1, v2):
        x, y = self.venturi.shape()
        pressure = self.flow.pressure(x, v1, v2)

        placeholder = st.empty()

        # 🔥 DENSE PARTICLES = FLUID BODY
        n = 2000
        px = np.random.uniform(0, 10, n)
        py = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2, n)

        for frame in range(200):
            fig, ax = plt.subplots(figsize=(18,6))

            # Pipe
            ax.plot(x, y, color='black', linewidth=2)
            ax.plot(x, -y, color='black', linewidth=2)

            # Pressure gradient
            norm = (pressure - pressure.min())/(pressure.max()-pressure.min())

            for i in range(len(x)-1):
                ax.fill_between([x[i], x[i+1]],
                                y[i], -y[i],
                                color=plt.cm.coolwarm(norm[i]),
                                alpha=0.25)

            # 🔥 MOVE FLUID
            for i in range(n):
                xi = px[i]
                yi = py[i]

                # stay inside pipe
                r = np.interp(xi, x, y)
                if abs(yi) > r:
                    py[i] = np.random.uniform(-r, r)

                # velocity variation
                if xi < 3 or xi > 7:
                    vx = v1
                else:
                    vx = v2

                # move
                px[i] += vx * 0.04

                # wrap
                if px[i] > 10:
                    px[i] = 0
                    py[i] = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2)

            # 🔥 DRAW FLUID MASS (this is key)
            ax.scatter(px, py, s=1, color='white', alpha=0.6)

            ax.set_xlim(0, 10)
            ax.set_ylim(-self.venturi.d1, self.venturi.d1)
            ax.axis('off')

            ax.set_title("Flowing Water Through Venturi", fontsize=18)

            plt.tight_layout()
            placeholder.pyplot(fig)
            time.sleep(0.01)

    def graph(self, v1, v2):
        x = np.linspace(0, 10, 200)
        vel = [v1 if (xi < 3 or xi > 7) else v2 for xi in x]

        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(x, vel, linewidth=3)

        ax.set_title("Velocity Along Pipe")
        ax.set_xlabel("Length")
        ax.set_ylabel("Velocity")
        ax.grid(True)

        return fig


# =========================
# UI
# =========================
st.title("Venturi Meter Flow (Best Possible Streamlit Simulation)")

col1, col2 = st.columns([1,2])

with col1:
    d1 = st.slider("Inlet Diameter", 0.3, 1.0, 0.6)
    d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.3)
    dp = st.slider("Pressure Difference", 100, 5000, 1500)
    rho = st.slider("Density", 500, 1500, 1000)

    venturi = VenturiMeter(d1, d2)
    fluid = Fluid(rho)
    flow = FlowCalculator(venturi, fluid, dp)
    sim = Simulation(venturi, flow)

    v1, v2 = flow.velocity()

    st.metric("Inlet Velocity", f"{v1:.2f}")
    st.metric("Throat Velocity", f"{v2:.2f}")

    if st.button("Start Flow"):
        sim.animate(v1, v2)

with col2:
    st.pyplot(sim.graph(v1, v2))
