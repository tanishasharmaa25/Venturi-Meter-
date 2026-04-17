import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#Class 1: Venturi Meter

class VenturiMeter:
    
    def __init__(self, inlet, throat):
        self.inlet = inlet #Inlet Diameter
        self.throat = throat #Throat Diameter

    def area(self, d):
        return np.pi * (d / 2) ** 2 #cross-sectional area of pipe

    def get_area(self):
        return self.area(self.inlet), self.area(self.throat)

#Class 2: Fluid
class Fluid:

    def __init__(self, density):
        self.density = density #Stores Density

#Class 3: Flow Calculator
class FlowCalculator:
    def __init__(self, Venturi, fluid, delta_p):
        self.venturi = venturi
        self.fluid = fluid
        self.delta_p = delta_p #Pressure Diffence
    
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
#Class 4: Visualizer

class Visualizer:
    def plot_velocity(self, v1, v2):
        labels = ['Inlet Velocity', 'Throat Velocity']
        values = [v1, v2]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylabel("Velocity(m/s)")
        ax.set_title("Velocity Comparison")

        return fig

#Streamlit App
import streamlit as st

st.title("Venturi Meter Flow Simulator")

#Sidebar Menu
menu = st.sidebar.selectbox("Select Option:", ["Simulation", "Notes", "Quiz"])

#Simulation

if menu == "Simulation":
    st.header("Simulation")

    d1 = st.sidebar.number_input("Inlet Diameter(m)", value=0.2)
    d2 = st.sidebar.number_input("Throat Diameter(m)", value=0.1)
    delta_p = st.sidebar.number_input("Pressure Difference(Pa)", value=1000)
    density = st.sidebar.number_input("Fluid Density(kg/m³)", value=1000)

    venturi = VenturiMeter(d1, d2)
    fluid = Fluid(density)
    calculator = FlowCalculator(venturi, fluid, delta_p)
    visualizer = Visualizer()

    v1, v2 = calculator.calculate_velocity()
    flow_rate = calculator.calculate_flow_rate()

    st.subheader("Results")
    st.write(f"Inlet Velocity: {v1:.2f} m/s")
    st.write(f"Throat Velocity: {v2:.2f} m/s")
    st.write(f"Flow Rate: {flow_rate:.4f} m³/s")

    fig = visualizer.plot_velocity(v1, v2)
    st.pyplot(fig)

#Notes section
elif menu == "Notes":
    st.header("Venturi Meter Notes")

    st.subheader("What is a Venturi Meter?")
    st.write("A Venturi meter is a device used to measure the flow rate of fluid in a pipe.")

    st.subheader("Working Principle")
    st.write("When fluid flows through a narrow section, velocity increases and pressure decreases.")

    st.subheader("Key Equations")
    st.write("Continuity Equation: A1V1 = A2V2")
    st.write("Bernoulli Equation: P1 + ½ρV1² = P2 + ½ρV2²")

    st.subheader("Concept Insight")
    st.write("As the pipe narrows, fluid speeds up and pressure drops.")

#Quiz

elif menu == "Quiz":
    st.header("Quiz")

    q1 = st.radio("1. What happens to velocity when diameter decreases?",
                 ["Decreases", "Increases"])

    if st.button("Check Answer 1"):
        if q1 == "Increases":
            st.success("Correct!")
        else:
            st.error("Wrong! Velocity increases.")

    q2 = st.radio("2. Which principle is used in Venturi meter?",
                 ["Newton’s Law", "Bernoulli’s Principle"])

    if st.button("Check Answer 2"):
        if q2 == "Bernoulli’s Principle":
            st.success("Correct!")
        else:
            st.error("Wrong answer.")
