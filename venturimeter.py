import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

# ---------------- CORE FUNCTIONS ----------------

def area(d):
    return np.pi * (d/2)**2

def velocity(d1, d2, dp, rho):
    A1 = area(d1)
    A2 = area(d2)

    v2 = np.sqrt((2*dp) / (rho*((A1 / A2)**2 - 1)))
    v1 = (A2 / A1)*v2

    return v1, v2


# ---------------- VENTURI SHAPE ----------------

def venturishape(d1, d2):
    x = np.linspace(0, 10, 200)

    y = np.piecewise(
        x,
        [x < 3, (x >= 3) & (x <= 7), x > 7],
        [
            lambda x: d1 / 2,
            lambda x: d1 / 2 - (d1 - d2) / 2 * ((x - 3) / 4),
            lambda x: d1 / 2,
        ],
    )
    return x, y


# ---------------- PRESSURE COLOR ----------------

def pressurecolour(x):
    return "red" if 3 <= x <= 7 else "blue"


# ---------------- ANIMATION (NON-BLOCKING) ----------------

def animate(d1, d2, v1, v2):
    x, y = venturishape(d1, d2)
    placeholder = st.empty()

    if "particles" not in st.session_state:
        st.session_state.particles = np.linspace(0, 10, 30)

    particles = st.session_state.particles

    fig, ax = plt.subplots()

    # Pipe
    ax.plot(x, y, color="black")
    ax.plot(x, -y, color="black")

    # Pressure shading
    for i in range(len(x)-1):
        color = "lightblue" if x[i] < 3 or x[i] > 7 else "lightcoral"
        ax.fill_between([x[i], x[i+1]], y[i], -y[i], color=color, alpha=0.2)

    # Particle motion (single frame)
    for i in range(len(particles)):
        pos = particles[i]

        if pos < 3:
            vel = v1
        elif pos <= 7:
            vel = v2
        else:
            vel = v1

        pos += vel * 0.1

        if pos > 10:
            pos = 0

        particles[i] = pos
        ax.plot(pos, 0, "o", color=pressurecolour(pos), markersize=8)

    ax.set_xlim(0, 10)
    ax.set_ylim(-d1, d1)
    ax.set_title("Venturi Flow Simulation")

    placeholder.pyplot(fig)
    plt.close(fig)


# ---------------- VELOCITY GRAPH ----------------

def plot_velocity_graph(v1, v2):
    fig, ax = plt.subplots()

    labels = ['Inlet', 'Throat']
    values = [v1, v2]

    bars = ax.bar(labels, values)
    bars[0].set_color('blue')
    bars[1].set_color('red')

    for i, v in enumerate(values):
        ax.text(i, v + 0.05, f"{v:.2f}", ha='center', fontweight='bold')

    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Inlet vs Throat Velocity")
    ax.set_ylim(0, max(values) * 1.3)

    return fig


# ---------------- UI ----------------

st.title(" Venturi Meter Flow Simulation")

col1, col2 = st.columns([1, 2])

# -------- CONTROLS --------
with col1:
    st.subheader("🎛 Controls")

    d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
    d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
    dp = st.slider("Pressure Difference", 100, 5000, 1000)
    rho = st.slider("Fluid Density", 500, 1500, 1000)

    v1, v2 = velocity(d1, d2, dp, rho)

    st.metric("Inlet Velocity", f"{v1:.2f} m/s")
    st.metric("Throat Velocity", f"{v2:.2f} m/s")

    st.markdown("### 🔵 High Pressure | 🔴 Low Pressure")

# -------- SIMULATION --------
with col2:
    st.subheader(" Simulation")

    animate(d1, d2, v1, v2)

    time.sleep(0.05)
    st.rerun()

    st.subheader("📊 Velocity Graph")

    if st.button("Show Velocity Graph"):
        fig = plot_velocity_graph(v1, v2)
        st.pyplot(fig)


# ---------------- NOTES ----------------

st.header("📘 Venturi Meter Notes")

tab1, tab2, tab3 = st.tabs(["Concept", "Derivation", "Key Insights"])

with tab1:
    st.markdown("""
- Narrow pipe → velocity increases  
- Velocity increase → pressure decreases  
- Based on Bernoulli Principle  
""")

with tab2:
    st.latex(r"A_1 v_1 = A_2 v_2")
    st.latex(r"P_1 + \frac{1}{2}\rho v_1^2 = P_2 + \frac{1}{2}\rho v_2^2")
    st.latex(r"v_2 = \sqrt{\frac{2\Delta P}{\rho((A_1/A_2)^2 - 1)}}")

with tab3:
    st.markdown("""
👉 Diameter ↓ → Velocity ↑ → Pressure ↓  
👉 Flow remains continuous  
""")


# ---------------- QUIZ ----------------

st.header("🧠 Quiz")

if "score" not in st.session_state:
    st.session_state.score = 0
if "attempted" not in st.session_state:
    st.session_state.attempted = 0
if "weak_topics" not in st.session_state:
    st.session_state.weak_topics = []
if "answered" not in st.session_state:
    st.session_state.answered = set()


quiz_data = {
    "Easy": [
        {"q": "Where is velocity maximum?", "options": ["Inlet", "Throat", "Outlet"], "answer": "Throat", "topic": "Concept"},
        {"q": "Pressure is lowest at?", "options": ["Inlet", "Throat", "Outlet"], "answer": "Throat", "topic": "Concept"}
    ],
    "Medium": [
        {"q": "Which equation ensures flow conservation?", "options": ["Bernoulli", "Continuity", "Newton"], "answer": "Continuity", "topic": "Theory"},
        {"q": "If diameter decreases, velocity will?", "options": ["Decrease", "Increase", "Same"], "answer": "Increase", "topic": "Concept"}
    ],
    "Hard": [
        {"q": "If pressure difference increases, velocity will?", "options": ["Decrease", "Increase", "Same"], "answer": "Increase", "topic": "Application"},
        {"q": "Velocity depends on?", "options": ["Pressure & density", "Only diameter", "Only pressure"], "answer": "Pressure & density", "topic": "Formula"}
    ]
}

difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])
questions = quiz_data[difficulty]

for i, q in enumerate(questions):
    st.subheader(f"Q{i+1}: {q['q']}")
    user_ans = st.radio("Choose:", q["options"], key=f"{difficulty}_{i}")

    submitted = st.button(f"Submit Q{i+1}", key=f"btn_{difficulty}_{i}")

    if submitted and i not in st.session_state.answered:
        st.session_state.attempted += 1

        if user_ans == q["answer"]:
            st.success("Correct!")
            st.session_state.score += 1
        else:
            st.error(f"Wrong! Correct: {q['answer']}")
            st.session_state.weak_topics.append(q["topic"])

        st.session_state.answered.add(i)


# -------- SCORE --------

st.subheader("📊 Score Board")

st.metric("Score", st.session_state.score)
st.metric("Attempted", st.session_state.attempted)

if st.session_state.attempted > 0:
    acc = (st.session_state.score / st.session_state.attempted) * 100
    st.metric("Accuracy", f"{acc:.2f}%")


# -------- WEAK TOPICS --------

st.subheader("📉 Weak Topic Analysis")

if st.session_state.weak_topics:
    summary = {}
    for t in st.session_state.weak_topics:
        summary[t] = summary.get(t, 0) + 1

    for t, c in summary.items():
        st.warning(f"{t} (mistakes: {c})")
else:
    st.success("No weak topics 🎉")


# -------- RESET --------

if st.button("Reset Quiz"):
    st.session_state.score = 0
    st.session_state.attempted = 0
    st.session_state.weak_topics = []
    st.session_state.answered = set()
    st.rerun()
