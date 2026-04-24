import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# -------------------- CLASSES --------------------

class VenturiMeter:
    def __init__(self, d1, d2):
        self.d1 = d1
        self.d2 = d2

    def radius(self, x):
        """Smooth venturi shape using cosine transition"""
        if x < 3:
            return self.d1 / 2
        elif 3 <= x <= 7:
            return (self.d2/2) + (self.d1/2 - self.d2/2) * (1 + np.cos(np.pi*(x-3)/4)) / 2
        else:
            return self.d1 / 2


class Fluid:
    def __init__(self, rho):
        self.rho = rho


class FlowSimulator:
    def __init__(self, venturi, fluid, dp):
        self.venturi = venturi
        self.fluid = fluid
        self.dp = dp

    def area(self, r):
        return np.pi * r**2

    def velocity(self, x):
        """Velocity varies with area (continuity + Bernoulli)"""
        r = self.venturi.radius(x)
        A = self.area(r)

        r_throat = self.venturi.d2 / 2
        A2 = self.area(r_throat)

        v2 = np.sqrt((2*self.dp)/(self.fluid.rho*((self.area(self.venturi.d1/2)/A2)**2 - 1)))
        v = v2 * (A2 / A)

        return v


# -------------------- ANIMATION --------------------

def animate():
    venturi = VenturiMeter(d1, d2)
    fluid = Fluid(rho)
    flow = FlowSimulator(venturi, fluid, dp)

    placeholder = st.empty()

    # particles
    num_particles = 80
    particles_x = np.random.uniform(0, 10, num_particles)
    particles_y = np.random.uniform(-d1/2, d1/2, num_particles)

    for _ in range(200):
        fig, ax = plt.subplots(figsize=(16,5))

        x_vals = np.linspace(0, 10, 400)
        y_top = [venturi.radius(x) for x in x_vals]
        y_bottom = [-y for y in y_top]

        # draw venturi walls
        ax.plot(x_vals, y_top, color="black", linewidth=2)
        ax.plot(x_vals, y_bottom, color="black", linewidth=2)

        new_x = []
        new_y = []

        for i in range(num_particles):
            x = particles_x[i]
            y = particles_y[i]

            r = venturi.radius(x)

            # keep particle inside pipe
            if abs(y) > r:
                y = np.random.uniform(-r, r)

            v = flow.velocity(x)

            # smooth movement
            x_new = x + v * 0.03

            if x_new > 10:
                x_new = 0

            new_x.append(x_new)
            new_y.append(y)

        particles_x[:] = new_x
        particles_y[:] = new_y

        # velocity color
        velocities = [flow.velocity(x) for x in particles_x]

        sc = ax.scatter(
            particles_x,
            particles_y,
            c=velocities,
            cmap="plasma",
            s=25
        )

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1/2 - 0.2, d1/2 + 0.2)
        ax.set_title("Realistic Venturi Flow (Velocity-Based Animation)")
        ax.axis("off")

        placeholder.pyplot(fig)
        plt.close(fig)

        time.sleep(0.03)


# -------------------- UI --------------------

st.title("Venturi Meter Flow Simulation (Realistic)")

d1 = st.sidebar.slider("Inlet Diameter", 1.0, 5.0, 3.0)
d2 = st.sidebar.slider("Throat Diameter", 0.5, 3.0, 1.5)
dp = st.sidebar.slider("Pressure Difference", 1000, 10000, 5000)
rho = st.sidebar.slider("Fluid Density", 500, 1500, 1000)

if st.button("Start Simulation"):
    animate()
