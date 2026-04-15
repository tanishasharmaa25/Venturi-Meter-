{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 39,
   "id": "0604aee7-5a9c-40e0-a884-cb4822050d22",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "#Class 1: Venturi Meter\n",
    "\n",
    "class VenturiMeter:\n",
    "    \n",
    "    def __init__(self, inlet, throat):\n",
    "        self.inlet = inlet #Inlet Diameter\n",
    "        self.throat = throat #Throat Diameter\n",
    "\n",
    "    def area(self, d):\n",
    "        return np.pi * (d / 2) ** 2 #cross-sectional area of pipe\n",
    "\n",
    "    def get_area(self):\n",
    "        return self.area(self.inlet), self.area(self.throat)\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "6e041617-890f-486b-a42a-7510fe4e932e",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Class 2: Fluid\n",
    "class Fluid:\n",
    "\n",
    "    def __init__(self, density):\n",
    "        self.density = density #Stores Density"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "799307b8-3010-4076-aefe-db59e3864f48",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Class 3: Flow Calculator\n",
    "class FlowCalculator:\n",
    "    def __init__(self, Venturi, fluid, delta_p):\n",
    "        self.venturi = venturi\n",
    "        self.fluid = fluid\n",
    "        self.delta_p = delta_p #Pressure Diffence\n",
    "    \n",
    "    def calculate_velocity(self):\n",
    "        A1, A2 = self.venturi.get_area()\n",
    "        rho = self.fluid.density\n",
    "\n",
    "        v2 = np.sqrt((2 * self.delta_p) / (rho * ((A1 / A2) ** 2 - 1)))\n",
    "        v1 = (A2 / A1) * v2\n",
    "\n",
    "        return v1, v2\n",
    "\n",
    "    def calculate_flow_rate(self):\n",
    "        A1, _ = self.venturi.get_area()\n",
    "        v1, _ = self.calculate_velocity()\n",
    "        return A1 * v1\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "9e3f10ba-ac69-444f-82ec-e768f9cfbc2b",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Class 4: Visualizer\n",
    "\n",
    "class Visualizer:\n",
    "    def plot_velocity(self, v1, v2):\n",
    "        labels = ['Inlet Velocity', 'Throat Velocity']\n",
    "        values = [v1, v2]\n",
    "\n",
    "        fig, ax = plt.subplots()\n",
    "        ax.bar(labels, values)\n",
    "        ax.set_ylabel(\"Velocity(m/s)\")\n",
    "        ax.set_title(\"Velocity Comparison\")\n",
    "\n",
    "        return fig"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "c6f32326-345d-4467-8e6d-388126940f26",
   "metadata": {
    "scrolled": true
   },
   "outputs": [
    {
     "ename": "SyntaxError",
     "evalue": "invalid syntax (2835567654.py, line 73)",
     "output_type": "error",
     "traceback": [
      "\u001b[1;36m  Cell \u001b[1;32mIn[45], line 73\u001b[1;36m\u001b[0m\n\u001b[1;33m    streamlit run venturi_meter.ipynb\u001b[0m\n\u001b[1;37m              ^\u001b[0m\n\u001b[1;31mSyntaxError\u001b[0m\u001b[1;31m:\u001b[0m invalid syntax\n"
     ]
    }
   ],
   "source": [
    "#Streamlit App\n",
    "\n",
    "st.title(\"Venturi Meter Flow Simulator\")\n",
    "\n",
    "#Sidebar Menu\n",
    "menu = st.sidebar.selectbox(\"Select Option:\", [\"Simulation\", \"Notes\", \"Quiz\"])\n",
    "\n",
    "#Simulation\n",
    "\n",
    "if menu == \"Simulation\":\n",
    "    st.header(\"Simulation\")\n",
    "\n",
    "    d1 = st.sidebar.number_input(\"Inlet Diameter(m)\", value=0.2)\n",
    "    d2 = st.sidebar.number_input(\"Throat Diameter(m)\", value=0.1)\n",
    "    delta_p = st.sidebar.number_input(\"Pressure Difference(Pa)\", value=1000)\n",
    "    density = st.sidebar.number_input(\"Fluid Density(kg/m³)\", value=1000)\n",
    "\n",
    "    venturi = VenturiMeter(d1, d2)\n",
    "    fluid = Fluid(density)\n",
    "    calculator = FlowCalculator(venturi, fluid, delta_p)\n",
    "    visualizer = Visualizer()\n",
    "\n",
    "    v1, v2 = calculator.calculate_velocity()\n",
    "    flow_rate = calculator.calculate_flow_rate()\n",
    "\n",
    "    st.subheader(\"Results\")\n",
    "    st.write(f\"Inlet Velocity: {v1:.2f} m/s\")\n",
    "    st.write(f\"Throat Velocity: {v2:.2f} m/s\")\n",
    "    st.write(f\"Flow Rate: {flow_rate:.4f} m³/s\")\n",
    "\n",
    "    fig = visualizer.plot_velocity(v1, v2)\n",
    "    st.pyplot(fig)\n",
    "\n",
    "#Notes section\n",
    "elif menu == \"Notes\":\n",
    "    st.header(\"Venturi Meter Notes\")\n",
    "\n",
    "    st.subheader(\"What is a Venturi Meter?\")\n",
    "    st.write(\"A Venturi meter is a device used to measure the flow rate of fluid in a pipe.\")\n",
    "\n",
    "    st.subheader(\"Working Principle\")\n",
    "    st.write(\"When fluid flows through a narrow section, velocity increases and pressure decreases.\")\n",
    "\n",
    "    st.subheader(\"Key Equations\")\n",
    "    st.write(\"Continuity Equation: A1V1 = A2V2\")\n",
    "    st.write(\"Bernoulli Equation: P1 + ½ρV1² = P2 + ½ρV2²\")\n",
    "\n",
    "    st.subheader(\"Concept Insight\")\n",
    "    st.write(\"As the pipe narrows, fluid speeds up and pressure drops.\")\n",
    "\n",
    "#Quiz\n",
    "\n",
    "elif menu == \"Quiz\":\n",
    "    st.header(\"Quiz\")\n",
    "\n",
    "    q1 = st.radio(\"1. What happens to velocity when diameter decreases?\",\n",
    "                 [\"Decreases\", \"Increases\"])\n",
    "\n",
    "    if st.button(\"Check Answer 1\"):\n",
    "        if q1 == \"Increases\":\n",
    "            st.success(\"Correct!\")\n",
    "        else:\n",
    "            st.error(\"Wrong! Velocity increases.\")\n",
    "\n",
    "    q2 = st.radio(\"2. Which principle is used in Venturi meter?\",\n",
    "                 [\"Newton’s Law\", \"Bernoulli’s Principle\"])\n",
    "\n",
    "    if st.button(\"Check Answer 2\"):\n",
    "        if q2 == \"Bernoulli’s Principle\":\n",
    "            st.success(\"Correct!\")\n",
    "        else:\n",
    "            st.error(\"Wrong answer.\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c83bd9d9-a2a8-4ca5-81a9-ee9a671f298a",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
