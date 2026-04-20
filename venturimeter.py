import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

#Core Function
def area(d):
    return np.pi * (d/2)**2 #Area of circular pipe section
    #rho: fluid density
    
def velocity(d1, d2, dp, rho): #dp : Pressure diffrence(P1 - P2)
    A1 = area(d1) #Area of d1(Inlet Diameter)
    A2 = area(d2) #Area of d2(Throat Diameter)

    v2 = np.sqrt((2*dp) / (rho*((A1 / A2)**2 - 1))) #v2 : Velocity at throat (Bernoulli's Eq + Continuity Eq)
    v1 = (A2 / A1)*v2 #v1 : Velocity at inlet (Continuity eq : A1v1 = A2v2)

    return v1, v2 

#Venturi shape
def venturishape(d1, d2): #linespace : creates pipe length
    x = np.linspace(0, 10, 200) #Create x axis (Length of pipe)

    y = np.piecewise( #Piecewise: Splits pipe into region
        x,
        [x < 3, (x >= 3) & (x <= 7), x > 7], 
        [
            lambda x: d1 / 2, #Inlet
            lambda x: d1 / 2 - (d1 - d2) / 2 * ((x - 3) / 4), #Converging section
            lambda x: d1 / 2, #Outlet
        ],
    )
    return x, y

#Pressure colour
def pressurecolour(x):
    if 3 <= x <= 7:
        return "red"   #low pressure : Diameter decreases : Velocity increases : Pressure decrease
    else:
        return "blue"  #high pressure : Velocity decreases : pressure increases

#Animation
def animate(d1, d2, v1, v2):
    x, y = venturishape(d1, d2)

    fig, ax = plt.subplots()
    placeholder = st.empty()

    particles = np.linspace(0, 10, 30)

    for frame in range(80):
        ax.clear()

        # Pipe walls
        ax.plot(x, y, color="black")
        ax.plot(x, -y, color="black")

        #Pressure shading
        for i in range(len(x)-1):
            color = "lightblue" if x[i] < 3 or x[i] > 7 else "lightcoral"
            ax.fill_between([x[i], x[i+1]], y[i], -y[i], color=color, alpha=0.2)

        #Particle motion
        for i in range(len(particles)):
            pos = particles[i]

            if pos < 3:
                pos += v1 * 0.02
            elif 3 <= pos <= 7:
                pos += v2 * 0.02
            else:
                pos += v1 * 0.02

            if pos > 10:
                pos = 0

            particles[i] = pos
            ax.plot(pos, 0, "o", color=pressurecolour(pos))

        ax.set_xlim(0, 10)
        ax.set_ylim(-d1, d1)
        ax.set_title("Venturi Flow Simulation")

        placeholder.pyplot(fig)
        time.sleep(0.05)

#Velocity Graph
def plot_velocity_graph(v1, v2):
    fig, ax = plt.subplots()

    labels = ['Inlet', 'Throat']
    values = [v1, v2]

    bars = ax.bar(labels, values)

    # Color coding
    bars[0].set_color('blue')
    bars[1].set_color('red')

    # Values on bars
    for i, v in enumerate(values):
        ax.text(i, v + 0.05, f"{v:.2f}", ha='center', fontweight='bold')

    ax.set_ylabel("Velocity (m/s)")
    ax.set_title("Inlet vs Throat Velocity")
    ax.set_ylim(0, max(values) * 1.3)

    return fig

#UI
menu = st.sidebar.selectbox("Select Section", ["Simulation", "Notes", "Quiz"])
if menu == "Simulation":
    st.title("Venturi Meter Flow Simulation")
    
    col1, col2 = st.columns([1, 2])
    #Controls
    with col1:
        st.subheader("Controls")
        d1 = st.slider("Inlet Diameter", 0.2, 1.0, 0.5)
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
        dp = st.slider("Pressure Difference", 100, 5000, 1000)
        rho = st.slider("Fluid Density", 500, 1500, 1000)
        
        v1, v2 = velocity(d1, d2, dp, rho)
        
        st.metric("Inlet Velocity", f"{v1:.2f} m/s")
        st.metric("Throat Velocity", f"{v2:.2f} m/s")
        
        st.markdown("### 🔵 High Pressure | 🔴 Low Pressure")
        
        if st.button("Start Simulation"):
            animate(d1, d2, v1, v2)
            
            #Simulation
            
            with col2:
                st.subheader("Velocity Graph")
                
                fig = plot_velocity_graph(v1, v2)
                st.pyplot(fig)
        
#Notes Section
elif menu =="Notes":
    st.header("Venturi Meter Notes")
    
    tab1, tab2, tab3 = st.tabs(["Concept", "Derivation", "Key Insights"])
    
    with tab1:
        st.subheader("What is a Venturi Meter?")
        
        st.markdown("""Venturimeter is a flow meter device or instrument that is used to measure the flow rate (discharge) in a pipe. The venturi meter is used in the water supply industry and It works on the basis of the Bernoulli theorem. The venturi meter is invented by Clemans Herchel who was an American Hydraulic engineer.
""")
        st.markdown("### Venturi Meter")
        
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/3d/Venturi_tube_diagram.svg")
        
        st.markdown("""
### Venturi Meter Types:
There are four different types of venturi tubes and those are:

-Classic venturi tube or A standard long-form.
-A modified short form where the outlet cone is shortened.
-An eccentric form to handle mixed phases or to minimize the build-up of heavy materials.
-A rectangular form used in the ductwork

### Venturi Meter Construction:
Venturi meter has been divided into three parts such as:

1. Converging Part
2. Throat Diameter and
3. Diverging Side
""")
        st.info("Remember: Velocity ↑ ⇒ Pressure ↓ (Bernoulli Principle)")
        
        with tab2:
            
            st.subheader("Step-by-Step Derivation")
            st.markdown("### 1. Continuity Equation")
            st.latex(r"A_1 v_1 = A_2 v_2")
            st.markdown("""
This means flow is conserved:
- If area decreases → velocity must increase
""")
            st.markdown("### 2. Bernoulli’s Equation")
            st.latex(r"P_1 + \frac{1}{2}\rho v_1^2 = P_2 + \frac{1}{2}\rho v_2^2")
            
            st.markdown("### 3. Rearranging")
            st.latex(r"P_1 - P_2 = \frac{1}{2}\rho (v_2^2 - v_1^2)")
            
            st.markdown("### 4. Substitute using Continuity")
            st.latex(r"v_1 = \frac{A_2}{A_1} v_2")
            
            st.markdown("### 5. Final Formula")
            st.latex(r"v_2 = \sqrt{\frac{2\Delta P}{\rho\left(\left(\frac{A_1}{A_2}\right)^2 - 1\right)}}")
            
            st.success("This is the formula used!")

#Quiz Section
elif menu == "quiz":
    st.header("Quiz")
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "attempted" not in st.session_state:
        st.session_state.attempted = 0
    if "weak_topics" not in st.session_state:
        st.session_state.weak_topics = []
        
    #Question Bank
    quiz_data = {
        "Easy": [
            {
                "q": "Where is velocity maximum?",
                "options": ["Inlet", "Throat", "Outlet"],
                "answer": "Throat",
                "topic": "Concept"
            },
            {
                "q": "Pressure is lowest at?",
                "options": ["Inlet", "Throat", "Outlet"],
                "answer": "Throat",
                "topic": "Concept"
            }
        ],
        "Medium": [
            {
                "q": "Which equation ensures flow conservation?",
                "options": ["Bernoulli", "Continuity", "Newton's Law"],
                "answer": "Continuity",
                "topic": "Theory"
            },
            {
                "q": "If diameter decreases, velocity will?",
                "options": ["Decrease", "Increase", "Remain same"],
                "answer": "Increase",
                "topic": "Concept"
            }
        ],
        "Hard": [
            {
                "q": "If pressure difference increases, velocity will?",
                "options": ["Decrease", "Increase", "Remain same"],
                "answer": "Increase",
                "topic": "Application"
            },
            {
                "q": "Velocity depends on which factors?",
                "options": ["Pressure difference & density", "Only diameter", "Only pressure"],
                "answer": "Pressure difference & density",
                "topic": "Formula"
            }
        ]
    }
    difficulty = st.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
    questions = quiz_data[difficulty]
    #quiz loop
    for i, q in enumerate(questions):
        st.subheader(f"Q{i+1}: {q['q']}")
        user_ans = st.radio(f"Select answer {i}", q["options"], key=f"{difficulty}_{i}")
        
        if st.button(f"Submit Q{i+1}", key=f"btn_{difficulty}_{i}"):
            st.session_state.attempted += 1
            
            if user_ans == q["answer"]:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {q['answer']}")
                st.session_state.weak_topics.append(q["topic"])

#scoreboard
st.subheader("Score Board")

st.metric("Score", st.session_state.score)
st.metric("Attempted", st.session_state.attempted)

if st.session_state.attempted > 0:
    accuracy = (st.session_state.score / st.session_state.attempted) * 100
    st.metric("Accuracy", f"{accuracy:.2f}%")

#Weak topic analysis
st.subheader("Weak Topic Analysis")

if st.session_state.weak_topics:
    weak_summary = {}

    for topic in st.session_state.weak_topics:
        if topic in weak_summary:
            weak_summary[topic] += 1
        else:
            weak_summary[topic] = 1

    st.write("You need to focus on these topics:")

    for topic, count in weak_summary.items():
        st.warning(f"{topic} (mistakes: {count})")

else:
    st.success("Great! No weak topics so far")


if st.button("Reset Quiz"):
    st.session_state.score = 0
    st.session_state.attempted = 0
    st.session_state.weak_topics = []
    st.experimental_rerun()
