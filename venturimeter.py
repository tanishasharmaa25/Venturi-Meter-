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

    def area(self, d):
        return np.pi * (d/2)**2

    def A1(self):
        return self.area(self.d1)

    def A2(self):
        return self.area(self.d2)

    def shape(self):
        x = np.linspace(0, 10, 200)
        y = np.piecewise(
            x,
            [x < 3, (x >= 3) & (x <= 7), x > 7],
            [
                lambda x: self.d1/2,
                lambda x: self.d1/2 - (self.d1-self.d2)/2 * ((x-3)/4),
                lambda x: self.d1/2
            ]
        )
        return x, y


class Fluid:
    def __init__(self, density):
        self.density = density


class FlowCalculator:
    def __init__(self, venturi, fluid, dp):
        self.v = venturi
        self.f = fluid
        self.dp = dp

    def velocity(self):
        A1 = self.v.A1()
        A2 = self.v.A2()
        rho = self.f.density

        v2 = np.sqrt((2*self.dp)/(rho*((A1/A2)**2 - 1)))
        v1 = (A2/A1)*v2
        return v1, v2

    def velocity_profile(self, x):
        A1 = self.v.A1()
        v1, _ = self.velocity()
        area = np.pi * (self.v.d1/2)**2
        return (A1*v1)/area


# ------------------ SIMULATION ------------------

class Simulation:
    def __init__(self, venturi, flow):
        self.v = venturi
        self.f = flow

    def pipe(self):
        x, y = self.v.shape()
        fig, ax = plt.subplots(figsize=(10,4))
        ax.plot(x, y, color="black")
        ax.plot(x, -y, color="black")
        ax.set_title("Venturi Shape")
        st.pyplot(fig)

    def velocity_graph(self):
        x = np.linspace(0,10,100)
        v1, v2 = self.f.velocity()
        v = np.piecewise(x, [x<3, (x>=3)&(x<=7), x>7], [v1, v2, v1])

        fig, ax = plt.subplots()
        ax.plot(x, v)
        ax.set_title("Velocity vs Position")
        st.pyplot(fig)

    def pressure_graph(self):
        x = np.linspace(0,10,100)
        v1, v2 = self.f.velocity()
        v = np.piecewise(x, [x<3, (x>=3)&(x<=7), x>7], [v1, v2, v1])
        P = 0.5*1000*(v1**2 - v**2)

        fig, ax = plt.subplots()
        ax.plot(x, P)
        ax.set_title("Pressure vs Position")
        st.pyplot(fig)

    def animate(self):
        x, y = self.v.shape()
        particles = np.linspace(0,10,30)
        placeholder = st.empty()

        v1, v2 = self.f.velocity()

        for _ in range(80):
            fig, ax = plt.subplots(figsize=(10,4))

            ax.plot(x, y, color='black')
            ax.plot(x, -y, color='black')

            new_particles = []

            for p in particles:
                if p < 3:
                    p += v1*0.05
                elif p <= 7:
                    p += v2*0.05
                else:
                    p += v1*0.05

                if p > 10:
                    p = 0

                new_particles.append(p)
                ax.scatter(p, 0, color='blue')

            particles = new_particles

            ax.set_xlim(0,10)
            ax.set_ylim(-self.v.d1, self.v.d1)

            placeholder.pyplot(fig)
            time.sleep(0.05)


# ------------------ NOTES ------------------

NOTES = """
Venturi Meter Notes:

1. Based on Bernoulli’s Principle
2. Velocity increases at throat
3. Pressure decreases at throat
4. Continuity Equation: A1V1 = A2V2
5. Used to measure flow rate
"""

# ------------------ QUIZ ------------------

QUIZ = [
    ("Where is velocity maximum?", ["Inlet","Throat","Outlet"], "Throat"),
    ("Where is pressure minimum?", ["Inlet","Throat","Outlet"], "Throat"),
    ("Venturi meter measures?", ["Temp","Flow","Density"], "Flow"),
]

# ------------------ UI ------------------

menu = st.sidebar.selectbox("Menu", ["Simulation","Notes","Quiz"])

# ------------------ SIMULATION ------------------

if menu == "Simulation":

    st.title("Venturi Meter Simulation")

    d1 = st.slider("Inlet Diameter", 0.1,1.0,0.5)
    d2 = st.slider("Throat Diameter", 0.05,0.5,0.2)
    dp = st.slider("Pressure Difference",100,1000,500)

    venturi = VenturiMeter(d1,d2)
    fluid = Fluid(1000)
    flow = FlowCalculator(venturi,fluid,dp)
    sim = Simulation(venturi,flow)

    v1, v2 = flow.velocity()

    st.write("Inlet Velocity:", round(v1,2))
    st.write("Throat Velocity:", round(v2,2))

    sim.pipe()
    sim.velocity_graph()
    sim.pressure_graph()

    if st.button("Start Animation"):
        sim.animate()

# ------------------ NOTES ------------------

elif menu == "Notes":
    st.title("Notes")
    st.write(NOTES)

# ------------------ QUIZ ------------------

elif menu == "Quiz":
    st.title("Quiz")

    score = 0
    weak = []

    for i,(q,options,ans) in enumerate(QUIZ):
        user = st.radio(q, options, key=i)
        if user == ans:
            score += 1
        else:
            weak.append(q)

    if st.button("Submit"):
        st.write("Score:", score)
        st.write("Weak Areas:", weak)
