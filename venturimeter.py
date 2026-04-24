import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# ---------------- CORE FUNCTIONS ---------------- #

def area(d):
    return np.pi * (d / 2) ** 2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2 * dp) / (rho * ((A1 / A2) ** 2 - 1)))
    v1 = (A2 / A1) * v2

    return v1, v2


# ---------------- VENTURI SHAPE ---------------- #

def venturishape(d1, d2):
    x = np.linspace(0, 10, 300)

    y = np.piecewise(
        x,
        [x < 3, (x >= 3) & (x <= 7), x > 7],
        [
            lambda x: d1 / 2,
            lambda x: d1 / 2 - (d1 - d2) / 2 * ((x - 3) / 4),
            lambda x: d2 / 2 + (d1 - d2) / 2 * ((x - 7) / 3),
        ],
    )
    return x, y


# ---------------- REALISTIC FLOW ANIMATION ---------------- #

def animate(d1, d2, v1, v2):
    x, y = venturishape(d1, d2)
    placeholder = st.empty()

    # Multiple fluid streamlines
    stream_y = np.linspace(-d1 / 2 * 0.8, d1 / 2 * 0.8, 12)
    particles = [np.linspace(0, 10, 25) for _ in stream_y]

    for frame in range(200):
        fig, ax = plt.subplots(figsize=(22, 8))

        # Pipe walls
        ax.plot(x, y, color="black", linewidth=2)
        ax.plot(x, -y, color="black", linewidth=2)

        # Smooth pressure gradient
        pressure = np.interp(x, [0, 3, 7, 10], [1, 0.3, 0.3, 1])
        for i in range(len(x) - 1):
            ax.fill_between(
                [x[i], x[i + 1]],
                y[i], -y[i],
                color=plt.cm.coolwarm(pressure[i]),
                alpha=0.5
            )

        # Flow simulation (streamlines)
        for j, line in enumerate(particles):
            for i in range(len(line)):
                pos = line[i]

                # Velocity variation
                if pos < 3:
                    vel = v1
                elif 3 <= pos <= 7:
                    vel = v2
                else:
                    vel = v1

                pos += vel * 0.03

                if pos > 10:
                    pos = 0

                line[i] = pos

                # Compression at throat
                y_pos = stream_y[j] * (d2 / d1 if 3 <= pos <= 7 else 1)

                ax.plot(
                    pos,
                    y_pos,
                    'o',
                    color=plt.cm.coolwarm(vel / max(v1, v2)),
                    markersize=4
                )

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1, d1)
        ax.axis('off')

        ax.set_title(
            "Realistic Venturi Flow (Velocity ↑ at Throat, Pressure ↓)",
            fontsize=18
        )

        plt.tight_layout()
        placeholder.pyplot(fig, use_container_width=True)

        time.sleep(0.01)


# ---------------- IMPROVED VELOCITY GRAPH ---------------- #

def plot_velocity_graph(d1, d2, v1, v2):
    x = np.linspace(0, 10, 200)

    velocity_profile = np.piecewise(
        x,
        [x < 3, (x >= 3) & (x <= 7), x > 7],
        [
            lambda x: v1,
            lambda x: v1 + (v2 - v1) * ((x - 3) / 4),
            lambda x: v2 - (v2 - v1) * ((x - 7) / 3),
        ],
    )

    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(x, velocity_profile, linewidth=3)

    ax.set_title("Velocity Distribution Along Venturi Meter")
    ax.set_xlabel("Position Along Pipe")
    ax.set_ylabel("Velocity (m/s)")
    ax.grid()

    return fig


# ---------------- UI ---------------- #

menu = st.sidebar.selectbox("Select Section", ["Simulation", "Notes", "Quiz"])

# ---------------- SIMULATION ---------------- #

if menu == "Simulation":
    st.title("Venturi Meter Flow Simulation")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Controls")

        d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
        dp = st.slider("Pressure Difference", 100, 5000, 1000)
        rho = st.slider("Fluid Density", 500, 1500, 1000)

        v1, v2 = velocity(d1, d2, dp, rho)

        st.metric("Inlet Velocity", f"{v1:.2f} m/s")
        st.metric("Throat Velocity", f"{v2:.2f} m/s")

        st.markdown("🔵 High Pressure | 🔴 Low Pressure")

        if st.button("Start Simulation"):
            animate(d1, d2, v1, v2)

    with col2:
        st.subheader("Velocity Graph")
        fig = plot_velocity_graph(d1, d2, v1, v2)
        st.pyplot(fig)


# ---------------- NOTES ---------------- #

elif menu == "Notes":
    st.header("Venturi Meter Notes")

    st.markdown("""
A Venturi meter measures flow rate using Bernoulli’s principle.

### Key Idea:
- Velocity ↑ ⇒ Pressure ↓
- Area ↓ ⇒ Velocity ↑

### Important Equations:

Continuity:
A₁v₁ = A₂v₂

Bernoulli:
P₁ + ½ρv₁² = P₂ + ½ρv₂²

Final velocity:
v₂ = √(2ΔP / ρ((A₁/A₂)² - 1))
""")


# ---------------- QUIZ ---------------- #

elif menu == "Quiz":
    st.header("Quiz")

    if "score" not in st.session_state:
        st.session_state.score = 0
        st.session_state.attempted = 0

    questions = [
        ("Where is velocity maximum?", "Throat"),
        ("Where is pressure minimum?", "Throat"),
        ("If diameter decreases, velocity?", "Increase"),
    ]

    for i, (q, ans) in enumerate(questions):
        user = st.text_input(f"{i+1}. {q}")
        if st.button(f"Submit {i}"):
            st.session_state.attempted += 1
            if user.lower() == ans.lower():
                st.success("Correct")
                st.session_state.score += 1
            else:
                st.error(f"Wrong. Answer: {ans}")

    st.subheader("Score")
    st.write(f"{st.session_state.score} / {st.session_state.attempted}")
