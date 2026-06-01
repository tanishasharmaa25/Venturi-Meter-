# 🌊 Venturi Meter Flow Simulation

An interactive Venturi Meter Flow Simulation developed using **Object-Oriented Programming (OOP) in Python** and deployed with **Streamlit**. The project combines fluid mechanics theory with real-time visualization to help students understand the relationship between pressure, velocity, and flow rate in a Venturi meter.

---

## 📌 Overview

Traditional Venturi meter calculations are often limited to static equations and numerical outputs. This project transforms those calculations into an interactive learning experience through simulations, visualizations, theory notes, and quizzes.

The application models incompressible fluid flow using:

- Bernoulli's Equation
- Continuity Equation
- Reynolds Number Analysis

Users can modify fluid properties, pipe dimensions, and pressure differences to observe real-time changes in flow behavior.

---

## ✨ Features

### 🔬 Interactive Flow Simulation
- Adjustable inlet diameter and throat diameter
- Variable pressure difference
- Multiple fluid presets
- Real-time flow calculations

### 📊 Dynamic Visualizations
- Velocity distribution graph
- Pressure distribution graph
- Venturi meter cross-section visualization
- Particle-based flow animation

### 📚 Learning Module
- Theory notes
- Formula reference sheet
- Fluid mechanics concepts

### 📝 Quiz System
- Multiple-choice questions
- Instant feedback
- Performance tracking

### 🧩 Object-Oriented Programming Concepts
- Encapsulation
- Abstraction
- Composition
- `@property`
- `@classmethod`
- Input validation
- Modular class design

---

## 🧮 Physics Implemented

### Continuity Equation

A₁V₁ = A₂V₂

### Bernoulli's Equation

P₁ + ½ρV₁² = P₂ + ½ρV₂²

### Reynolds Number

Re = ρVD/μ

Flow classification:

| Reynolds Number | Flow Regime |
|---------------|-------------|
| Re < 2300 | Laminar |
| 2300 ≤ Re ≤ 4000 | Transitional |
| Re > 4000 | Turbulent |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming Language |
| Streamlit | Web Application Framework |
| NumPy | Numerical Computation |
| Matplotlib | Data Visualization |
| Plotly | Interactive Graphs |
| OOP | System Design and Architecture |

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/venturi-meter-simulation.git
cd venturi-meter-simulation
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```


## 🎯 Educational Objectives

This project was developed as part of the **Object-Oriented Programming Course** for the **B.Tech Mathematics & Computing Program at UPES**.

The simulation aims to provide an intuitive understanding of:

- Venturi Effect
- Pressure-Velocity Relationship
- Flow Acceleration
- Reynolds Number
- Engineering Visualization
- Object-Oriented Design

---

## 📈 Sample Simulation Results

| Parameter | Value |
|-----------|--------|
| Fluid | Water (20°C) |
| Density | 998.2 kg/m³ |
| Viscosity | 1.002 × 10⁻³ Pa·s |
| Inlet Diameter | 0.10 m |
| Throat Diameter | 0.05 m |
| Pressure Difference | 5000 Pa |
| Inlet Velocity | 0.69 m/s |
| Throat Velocity | 2.78 m/s |
| Flow Rate | 5.45 L/s |
| Reynolds Number | ~69000 |
| Flow Regime | Turbulent |

---

## 🔮 Future Enhancements

- Incorporation of discharge coefficient (Cd)
- Friction and energy loss calculations
- Compressible flow modelling
- Advanced turbulence modelling
- Cloud deployment
- Enhanced 3D visualizations

## 👩‍💻 Author

**Tanisha Sharma**  
B.Tech Mathematics & Computing  
University of Petroleum and Energy Studies (UPES)

---

## 📄 License

This project is intended for educational and academic purposes.
