{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "d09de54d-9303-455b-9f99-2397791b8494",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "class VenturiMeter:\n",
    "    def __init__(self, d1, d2):\n",
    "        self.d1 = d1  # inlet diameter\n",
    "        self.d2 = d2  # throat diameter\n",
    "\n",
    "    def area(self, d):\n",
    "        return np.pi * (d/2)**2\n",
    "\n",
    "    def get_areas(self):\n",
    "        return self.area(self.d1), self.area(self.d2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "f6502564-94c8-404d-8682-9452df5e2353",
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "class Fluid:\n",
    "    def __init__(self, density):\n",
    "        self.density = density\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "faabadf7-a694-498b-880f-c2fa297ccf90",
   "metadata": {},
   "outputs": [],
   "source": [
    "class FlowCalculator:\n",
    "    def __init__(self, venturi, fluid, delta_p):\n",
    "        self.venturi = venturi\n",
    "        self.fluid = fluid\n",
    "        self.delta_p = delta_p\n",
    "   \n",
    "    def calculate_velocity(self):\n",
    "        A1, A2 = self.venturi.get_areas()\n",
    "        rho = self.fluid.density\n",
    "\n",
    "        v2 = np.sqrt((2 * self.delta_p) / (rho * ((A1/A2)**2 - 1)))\n",
    "        v1 = (A2 / A1) * v2\n",
    "\n",
    "        return v1, v2\n",
    "\n",
    "    def calculate_flow_rate(self):\n",
    "        A1, _ = self.venturi.get_areas()\n",
    "        v1, _ = self.calculate_velocity()\n",
    "        return A1 * v1\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "8f59cc1e-97ab-4c5f-8855-e371f1a8d764",
   "metadata": {},
   "outputs": [],
   "source": [
    "class Visualizer:\n",
    "    def plot(self, v1, v2):\n",
    "        labels = ['Inlet Velocity', 'Throat Velocity']\n",
    "        values = [v1, v2]\n",
    "\n",
    "        fig, ax = plt.subplots()\n",
    "        ax.bar(labels, values)\n",
    "        ax.set_ylabel(\"Velocity (m/s)\")\n",
    "        ax.set_title(\"Velocity Comparison\")\n",
    "\n",
    "        return fig\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "b03a55e4-73c6-4c35-88ab-cf1a26ea11f0",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-04-04 08:48:19.883 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.300 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\admin\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2026-04-04 08:48:20.301 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.303 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.304 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.305 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.305 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.306 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.307 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.307 Session state does not function when running a script without `streamlit run`\n",
      "2026-04-04 08:48:20.308 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.309 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.309 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.310 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.310 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.311 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.312 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.312 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.313 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.314 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.315 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.316 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.317 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.318 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.319 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.320 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.321 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.322 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.323 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 08:48:20.323 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    }
   ],
   "source": [
    "#streamlit UI\n",
    "st.title(\"Venturi Meter Flow Simulator\")\n",
    "\n",
    "st.sidebar.header(\"Input Parameters\")\n",
    "\n",
    "d1 = st.sidebar.number_input(\"Inlet Diameter (m)\", value=0.2)\n",
    "d2 = st.sidebar.number_input(\"Throat Diameter (m)\", value=0.1)\n",
    "delta_p = st.sidebar.number_input(\"Pressure Difference (Pa)\", value=1000)\n",
    "density = st.sidebar.number_input(\"Fluid Density (kg/m³)\", value=1000)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "1f3aea1d-3aa8-4e3d-b625-139d128c9e7d",
   "metadata": {},
   "outputs": [],
   "source": [
    "venturi = VenturiMeter(d1, d2)\n",
    "fluid = Fluid(density)\n",
    "calculator = FlowCalculator(venturi, fluid, delta_p)\n",
    "visualizer = Visualizer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "b27035b7-536b-4419-a99d-e21fe39ab9d7",
   "metadata": {},
   "outputs": [],
   "source": [
    "v1, v2 = calculator.calculate_velocity()\n",
    "flow_rate = calculator.calculate_flow_rate()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "1c9e3c5d-ea52-4eff-a703-2170442ace8f",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2026-04-04 09:03:08.364 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.365 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.366 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.367 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.368 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.368 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.435 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.638 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
      "2026-04-04 09:03:08.639 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "st.write(f\"Inlet Velocity: {v1:.2f} m/s\")\n",
    "st.write(f\"Throat Velocity: {v2:.2f} m/s\")\n",
    "st.write(f\"Flow Rate: {flow_rate:.4f} m³/s\")\n",
    "\n",
    "#Plot\n",
    "fig = visualizer.plot(v1, v2)\n",
    "st.pyplot(fig)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "375172b3-20b8-4efc-8b52-209a033286ae",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f0eef90a-ab3a-4041-8daa-18bfded004ea",
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
