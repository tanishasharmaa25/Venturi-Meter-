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
# SIMULATION CLASS
# =========================
class Simulation:
    def __init__(self, venturi, flow):
        self.venturi = venturi
        self.flow = flow

    def animate(self, v1, v2):
        x, y = self.venturi.shape()
        pressure = self.flow.pressure(x, v1, v2)

        placeholder = st.empty()

        n = 1500
        px = np.random.uniform(0, 10, n)
        py = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2, n)

        for _ in range(150):
            fig, ax = plt.subplots(figsize=(18,6))

            ax.plot(x, y, color='black')
            ax.plot(x, -y, color='black')

            norm = (pressure - pressure.min())/(pressure.max()-pressure.min())

            for i in range(len(x)-1):
                ax.fill_between([x[i], x[i+1]],
                                y[i], -y[i],
                                color=plt.cm.coolwarm(norm[i]),
                                alpha=0.25)

            for i in range(n):
                xi = px[i]
                yi = py[i]

                r = np.interp(xi, x, y)
                if abs(yi) > r:
                    py[i] = np.random.uniform(-r, r)

                vx = v1 if (xi < 3 or xi > 7) else v2

                px[i] += vx * 0.04

                if px[i] > 10:
                    px[i] = 0
                    py[i] = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2)

            ax.scatter(px, py, s=1, color='white', alpha=0.6)

            ax.set_xlim(0, 10)
            ax.set_ylim(-self.venturi.d1, self.venturi.d1)
            ax.axis('off')

            ax.set_title("Flowing Water Through Venturi")

            placeholder.pyplot(fig)
            time.sleep(0.01)

    def velocity_graph(self, v1):
        x, y = self.venturi.shape()

        A1 = self.venturi.area(self.venturi.d1)

        velocity = []
        for i in range(len(x)):
            radius = y[i]
            A = np.pi * radius**2
            v = (A1 * v1) / A
            velocity.append(v)

        velocity = np.array(velocity)

        fig, ax = plt.subplots(figsize=(12,5))

        ax.plot(x, velocity, linewidth=3)

        ax.axvline(3, linestyle='--')
        ax.axvline(7, linestyle='--')

        ax.text(1.5, max(velocity)*0.9, "Inlet", ha='center')
        ax.text(5, max(velocity)*0.95, "Throat", ha='center')
        ax.text(8.5, max(velocity)*0.9, "Outlet", ha='center')

        ax.set_title("Physics-Based Velocity Distribution")
        ax.set_xlabel("Length")
        ax.set_ylabel("Velocity")
        ax.grid(True)

        return fig


# =========================
# UI
# =========================
menu = st.sidebar.selectbox("Select Section", ["Simulation"])

if menu == "Simulation":
    st.title("Venturi Meter Simulation")

    col1, col2 = st.columns([1,2])

    with col1:
        d1 = st.slider("Inlet Diameter", 0.3, 1.0, 0.6)
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
        dp = st.slider("Pressure Difference", 100, 5000, 1000)
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
        st.pyplot(sim.velocity_graph(v1))
