import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(layout="wide")

#Class 1: VenturiMeter
class VenturiMeter:
    def __init__(self, d1, d2):
        self.d1 = d1 #Inlet Diameter
        self.d2 = d2 #Outlet Diameter
    
    def area(self,d):
        return np.pi * (d/2)**2 #Area of circular pipe section
    
    def get_areas(self):
        return self.area(self.d1), self.area(self.d2) #Gets Inlet Area(A1) & Outlet Area(A2)

    def shape(self): #Geometry of Venturi Meter
        x = np.linspace(0, 10, 400) #x : Pipe Length
        y = np.piecewise( #y : Pipe radius
            x,
            [x < 3, (x >= 3) & (x <= 7), x > 7],
            [
                lambda x: self.d1/2,                                                            #Region 1: Inlet
                lambda x: self.d2/2 + (self.d1 - self.d2)/2 * (1 + np.cos(np.pi*(x-3)/4))/2,    #Region 2: Throat
                lambda x: self.d1/2                                                             #Region 3: Outlet
            ]
        )
        return x, y

#Class 2: Fluid
class Fluid:
    def __init__(self, rho):
        self.rho = rho
        
#Class 3: FluidCalculator
class FluidCalculator:
    def __init__(self, venturi, fluid, dp):
        self.venturi = venturi
        self.fluid = fluid
        self.dp = dp

    def velocity(self):
        A1, A2 = self.venturi.get_areas()
        rho = self.fluid.rho

        v2 = np.sqrt((2*self.dp) / (rho*((A1/A2)**2 - 1))) #Throat velocity
        v1 = (A2/A1) * v2 #Inlet velocity

        return v1, v2

    def pressure(self, x, v1, v2): #Pressure distrubition
        p = []
        for xi in x:
            if xi < 3 or xi > 7:
                v = v1
            else:
                v = v2
            p.append(0.5 * self.fluid.rho * (v1**2 - v**2))
        return np.array(p)

#Class 4: Simulation
class Simulation:
    def __init__(self, venturi, flow):
        self.venturi = venturi
        self.flow = flow

    def animate(self, v1, v2):
        x, y = self.venturi.shape()
        pressure = self.flow.pressure(x, v1, v2)

        placeholder = st.empty()
        
        n = 2000
        px = np.random.uniform(0, 10, n)
        py = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2, n)

        for frame in range(200):
            fig, ax = plt.subplots(figsize=(18,6))

            # Pipe
            ax.plot(x, y, color='black', linewidth=2)
            ax.plot(x, -y, color='black', linewidth=2)

            # Pressure gradient
            norm = (pressure - pressure.min())/(pressure.max()-pressure.min())

            for i in range(len(x)-1):
                ax.fill_between([x[i], x[i+1]],
                                y[i], -y[i],
                                color=plt.cm.coolwarm(norm[i]),
                                alpha=0.25)

            for i in range(n):
                xi = px[i]
                yi = py[i]

                r = np.interp(xi, x, y)
                if abs(yi) > r:
                    py[i] = np.random.uniform(-r, r)
                    
                if xi < 3 or xi > 7:
                    vx = v1
                else:
                    vx = v2

                px[i] += vx * 0.04

                if px[i] > 10:
                    px[i] = 0
                    py[i] = np.random.uniform(-self.venturi.d1/2, self.venturi.d1/2)

            ax.scatter(px, py, s=1, color='white', alpha=0.6)

            ax.set_xlim(0, 10)
            ax.set_ylim(-self.venturi.d1, self.venturi.d1)
            ax.axis('off')

            ax.set_title("Flowing Water Through Venturi", fontsize=18)

            plt.tight_layout()
            placeholder.pyplot(fig)
            time.sleep(0.01)
            
    def velocity_graph(self, v1):
        x, y = self.venturi.shape()
        
        # Inlet area
        A1 = self.venturi.area(self.venturi.d1)
        velocity = []
        for i in range(len(x)):
            radius = y[i]
            A = np.pi * radius**2   # local area
            v = (A1 * v1) / A       # continuity equation
            velocity.append(v)
            
            velocity = np.array(velocity)
            
            fig, ax = plt.subplots(figsize=(12,5))
            
            ax.plot(x, velocity, linewidth=3)
            
            # Highlight regions
            ax.axvline(3, linestyle='--')
            ax.axvline(7, linestyle='--')
            ax.text(1.5, max(velocity)*0.9, "Inlet", ha='center')
            ax.text(5, max(velocity)*0.95, "Throat", ha='center')
            ax.text(8.5, max(velocity)*0.9, "Outlet", ha='center')
            ax.set_title("Velocity Distribution in Venturi Meter")
            ax.set_xlabel("Length of Pipe")
            ax.set_ylabel("Velocity (m/s)")
            ax.grid(True, linestyle='--', alpha=0.5)
    return fig
#UI
menu = st.sidebar.selectbox("Select Section", ["Simulation", "Notes", "Quiz"])
if menu == "Simulation":
    st.title("Venturi Meter Flow Simulation")
    
    col1, col2 = st.columns([1, 2])
    #Controls
    with col1:
        st.subheader("Controls")
        d1 = st.slider("Inlet Diameter", 0.3, 1.0, 0.6)
        d2 = st.slider("Throat Diameter", 0.1, 0.5, 0.2)
        dp = st.slider("Pressure Difference", 100, 5000, 1000)
        rho = st.slider("Fluid Density", 500, 1500, 1000)

        venturi = VenturiMeter(d1, d2)
        fluid = Fluid(rho)
        flow = FlowCalculator(venturi, fluid, dp)
        sim = Simulation(venturi, flow)
        
        v1, v2 = flow.velocity()
        
        st.metric("Inlet Velocity", f"{v1:.2f}")
        st.metric("Throat Velocity", f"{v2:.2f}")
        if st.button("Start Flow"):
            sim.animate(v1, v2)
    with col2:
        st.pyplot(sim.graph(v1, v2))
             
#Notes Section
elif menu =="Notes":
    st.header("Venturi Meter Notes")
    
    tab1, tab2= st.tabs(["Concept", "Derivation"])
    
    with tab1:
        st.subheader("What is a Venturi Meter?")
        
        st.markdown("""Venturimeter is a flow meter device or instrument that is used to measure the flow rate in a pipe. The venturi meter is used in the water supply industry and It works on the basis of the Bernoulli theorem. The venturi meter is invented by Clemans Herchel who was an American Hydraulic engineer.
""")
        st.markdown("### Venturi Meter")
        
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
elif menu == "Quiz":
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
                "Q": "Velocity depends on which factors?",
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
        
        if st.button(f"Submit", key=f"btn_{difficulty}_{i}"):
            st.session_state.attempted += 1
            
            if user_ans == q["answer"]:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {q['answer']}")
                st.session_state.weak_topics.append(q["topic"])
                
    # Scoreboard
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
            #Reset button
    if st.button("Reset Quiz"):
        st.session_state.score = 0
        st.session_state.attempted = 0
        st.session_state.weak_topics = []
        st.rerun()
