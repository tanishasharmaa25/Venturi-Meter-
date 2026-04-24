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

        A1 = self.area(self.venturi.d1 / 2)
        A2 = self.area(self.venturi.d2 / 2)

        v2 = np.sqrt((2*self.dp)/(self.rho*((A1/A2)**2 - 1)))
        return v2 * (A2 / A)


# ------------------ ANIMATION ------------------

def animate():
    venturi = VenturiMeter(d1, d2)
    flow = FlowSimulator(venturi, rho, dp)

    placeholder = st.empty()

    x = np.linspace(0, 10, 300)
    y_lines = np.linspace(-d1/2, d1/2, 20)

    phase = 0

    for _ in range(150):
        fig, ax = plt.subplots(figsize=(16,5))

        # Venturi shape
        y_top = np.array([venturi.radius(xi) for xi in x])
        y_bottom = -y_top

        ax.plot(x, y_top, color="black", linewidth=2)
        ax.plot(x, y_bottom, color="black", linewidth=2)

        # STREAMLINES
        for y0 in y_lines:
            x_stream = []
            y_stream = []
            colors = []

            for xi in x:
                r = venturi.radius(xi)

                if abs(y0) <= r:  # only inside pipe
                    v = flow.velocity(xi)

                    x_stream.append(xi)
                    y_stream.append(y0)
                    colors.append(v)

            if len(x_stream) > 1:  # avoid crash
                ax.plot(
                    x_stream,
                    y_stream,
                    color=plt.cm.plasma(np.mean(colors)/max(colors)),
                    linewidth=1.5,
                    alpha=0.8
                )

        # fake motion effect using shifting overlay
        for shift in np.linspace(0, 0.3, 5):
            for y0 in y_lines[::2]:
                xs = x + (phase * 0.02 + shift)
                ys = np.full_like(xs, y0)

                mask = np.abs(ys) <= np.array([venturi.radius(xi) for xi in xs])

                ax.plot(xs[mask], ys[mask], color="cyan", alpha=0.05)

        phase += 1

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1/2 - 0.2, d1/2 + 0.2)
        ax.set_title("Venturi Flow (Continuous Visible Streamlines)")
        ax.axis("off")

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0.03)


# ------------------ UI ------------------

st.title("Venturi Meter Flow Simulation")

d1 = st.sidebar.slider("Inlet Diameter", 1.0, 5.0, 3.0)
d2 = st.sidebar.slider("Throat Diameter", 0.5, 3.0, 1.5)
dp = st.sidebar.slider("Pressure Difference", 1000, 10000, 5000)
rho = st.sidebar.slider("Density", 500, 1500, 1000)

if st.button("Start Simulation"):
    animate()
