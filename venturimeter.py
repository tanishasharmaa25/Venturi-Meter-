import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# ------------------ CLASSES ------------------

class VenturiMeter:
    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

    def radius(self, x):
        if x < 3:
            return self.d1 / 2
        elif 3 <= x <= 7:
            return (self.d2/2) + (self.d1/2 - self.d2/2) * (1 + np.cos(np.pi*(x-3)/4)) / 2
        else:
            return self.d1 / 2


class FlowSimulator:
    def __init__(self, venturi, rho, dp):
        self.venturi = venturi
        self.rho = rho
        self.dp = dp

    def area(self, r):
        return np.pi * r**2

    def velocity(self, x):
        r = self.venturi.radius(x)
        A = self.area(r)

        r2 = self.venturi.d2 / 2
        A2 = self.area(r2)
        A1 = self.area(self.venturi.d1 / 2)

        v2 = np.sqrt((2*self.dp)/(self.rho*((A1/A2)**2 - 1)))
        return v2 * (A2 / A)


# ------------------ ANIMATION ------------------

def animate():
    venturi = VenturiMeter(d1, d2)
    flow = FlowSimulator(venturi, rho, dp)

    placeholder = st.empty()

    x = np.linspace(0, 10, 400)
    y_lines = np.linspace(-d1/2, d1/2, 25)

    phase = 0

    for _ in range(200):
        fig, ax = plt.subplots(figsize=(16,5))

        y_top = [venturi.radius(xi) for xi in x]
        y_bottom = [-y for y in y_top]

        # Draw pipe
        ax.plot(x, y_top, color="black", linewidth=2)
        ax.plot(x, y_bottom, color="black", linewidth=2)

        # STREAMLINES (REAL FLOW LOOK)
        for y0 in y_lines:
            y_stream = []
            x_stream = []

            for xi in x:
                r = venturi.radius(xi)
                if abs(y0) < r:
                    v = flow.velocity(xi)

                    # phase shift creates motion illusion
                    xi_shift = xi + (phase * v * 0.02)

                    x_stream.append(xi_shift % 10)
                    y_stream.append(y0)

            velocities = [flow.velocity(xi) for xi in x_stream]

            ax.plot(
                x_stream,
                y_stream,
                color=plt.cm.plasma(np.mean(velocities)/max(velocities)),
                linewidth=1.5,
                alpha=0.8
            )

        phase += 1

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1/2 - 0.2, d1/2 + 0.2)
        ax.set_title("Venturi Meter – Visible Fluid Flow")
        ax.axis("off")

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0.03)


# ------------------ UI ------------------

st.title("Venturi Meter (Real Flow Visualization)")

d1 = st.sidebar.slider("Inlet Diameter", 1.0, 5.0, 3.0)
d2 = st.sidebar.slider("Throat Diameter", 0.5, 3.0, 1.5)
dp = st.sidebar.slider("Pressure Difference", 1000, 10000, 5000)
rho = st.sidebar.slider("Density", 500, 1500, 1000)

if st.button("Start Simulation"):
    animate()
