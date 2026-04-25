"""
╔══════════════════════════════════════════════════════════╗
║    VENTURI METER FLOW SIMULATION                         ║
║    Semester 2 — Object Oriented Programming in Python    ║
║    Run: streamlit run app.py                             ║
╚══════════════════════════════════════════════════════════╝
"""
 
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import time
 
# ─────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Venturi Meter Simulation",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ─────────────────────────────────────────────────────────────────
#  GLOBAL STYLING
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');
 
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
 
  /* Sidebar */
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f1e 0%, #0d1b2a 100%);
    border-right: 1px solid #1e3a5f;
  }
  section[data-testid="stSidebar"] * { color: #e0e8f0 !important; }
  section[data-testid="stSidebar"] .stSelectbox label { color: #7db8e0 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.1em; }
 
  /* Main background */
  .stApp { background: #060d18; }
  .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
 
  /* Page title banner */
  .page-banner {
    background: linear-gradient(135deg, #0d1b2a 0%, #0a2540 50%, #0d1b2a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.4rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
  }
  .page-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0066cc, #00aaff, #0066cc);
  }
  .page-banner h1 {
    color: #e8f4fd !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.3rem 0 !important;
    letter-spacing: 0.02em;
  }
  .page-banner p {
    color: #5a8fa8 !important;
    font-size: 0.85rem !important;
    margin: 0 !important;
    font-family: 'Space Mono', monospace;
  }
 
  /* Metric cards */
  .metric-grid { display: flex; gap: 12px; margin: 1rem 0; flex-wrap: wrap; }
  .metric-box {
    flex: 1;
    min-width: 120px;
    background: #0d1b2a;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
  }
  .metric-box .m-label {
    color: #4a7fa0;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-family: 'Space Mono', monospace;
    display: block;
    margin-bottom: 0.4rem;
  }
  .metric-box .m-value {
    color: #00ccff;
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    display: block;
  }
  .metric-box .m-unit {
    color: #3a6080;
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
  }
 
  /* Section headings */
  .sec-heading {
    color: #7db8e0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.18em !important;
    margin: 1.4rem 0 0.6rem 0 !important;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid #1a3550;
  }
 
  /* Notes cards */
  .note-card {
    background: #0a1628;
    border: 1px solid #1a3550;
    border-left: 3px solid #0077cc;
    border-radius: 8px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 1rem;
    color: #c8dce8 !important;
    line-height: 1.75;
    font-size: 0.93rem;
  }
  .note-card h3 {
    color: #4db8ff !important;
    font-family: 'Space Mono', monospace;
    font-size: 0.95rem;
    margin-top: 0;
    margin-bottom: 0.6rem;
  }
  .note-card ul { padding-left: 1.4rem; margin: 0.4rem 0; }
  .note-card li { margin-bottom: 0.3rem; color: #a8c8e0; }
 
  /* Formula box */
  .formula-box {
    background: #060e1a;
    border: 1px solid #0a4080;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    margin: 0.8rem 0;
    text-align: center;
  }
 
  /* Info/highlight pill */
  .info-pill {
    display: inline-block;
    background: #0a2540;
    border: 1px solid #0066cc;
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    color: #4db8ff;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    margin: 0.2rem;
  }
 
  /* Quiz cards */
  .quiz-q {
    background: #0a1628;
    border: 1px solid #1a3550;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1.2rem;
  }
  .quiz-q .q-num {
    color: #0077cc;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.4rem;
  }
  .quiz-q .q-text {
    color: #c8dce8;
    font-size: 1rem;
    font-weight: 500;
    margin-bottom: 0;
  }
 
  /* Score board */
  .scoreboard {
    background: linear-gradient(135deg, #061020, #0a1f35);
    border: 1px solid #1a4070;
    border-radius: 12px;
    padding: 1.4rem;
    margin-top: 1.2rem;
  }
  .score-title {
    color: #4db8ff;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    margin-bottom: 1rem;
  }
 
  /* Difficulty badge */
  .badge-easy   { background:#0a2810; color:#4dcc88; border:1px solid #1a6030; border-radius:20px; padding:2px 12px; font-size:0.75rem; font-family:'Space Mono',monospace; }
  .badge-medium { background:#1a1a00; color:#cccc00; border:1px solid #606000; border-radius:20px; padding:2px 12px; font-size:0.75rem; font-family:'Space Mono',monospace; }
  .badge-hard   { background:#200a0a; color:#ff6666; border:1px solid #660000; border-radius:20px; padding:2px 12px; font-size:0.75rem; font-family:'Space Mono',monospace; }
 
  /* Override streamlit elements */
  .stSlider > div > div { background: #1a3550 !important; }
  .stSelectbox > div > div { background: #0d1b2a !important; border-color: #1e3a5f !important; }
  div[data-testid="stMarkdownContainer"] p { color: #a8c8e0; }
  h1, h2, h3 { color: #c8dce8 !important; }
  .stTabs [data-baseweb="tab"] { color: #4a7fa0 !important; font-family: 'Space Mono', monospace; font-size: 0.78rem; }
  .stTabs [aria-selected="true"] { color: #00aaff !important; border-bottom-color: #00aaff !important; }
  .stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)
 
 
# ═════════════════════════════════════════════════════════════════
#  CLASS 1 — VenturiMeter
#  Handles all geometry: pipe shape, area at any cross-section
# ═════════════════════════════════════════════════════════════════
class VenturiMeter:
    """
    Represents the geometric profile of a Venturi meter.
 
    The pipe is divided into three zones:
      [0, 3)      → Inlet   : constant radius = d1/2
      [3, 7]      → Throat  : smooth cosine transition from d1/2 → d2/2 → d1/2
      (7, 10]     → Outlet  : constant radius = d1/2
 
    Physical length is normalised to 10 units for visualisation.
    """
 
    # Zone boundaries (normalised pipe units)
    INLET_END   = 3.0
    THROAT_MID  = 5.0
    OUTLET_START = 7.0
    PIPE_LENGTH  = 10.0
 
    def __init__(self, d1: float, d2: float):
        """
        Args:
            d1: Inlet (and outlet) diameter [m]
            d2: Throat diameter [m]  — must be < d1
        """
        if d2 >= d1:
            raise ValueError("Throat diameter must be smaller than inlet diameter.")
        self.d1 = d1
        self.d2 = d2
 
    # ── Geometric helpers ────────────────────────────────────────
    @staticmethod
    def area_from_diameter(d: float) -> float:
        """Cross-sectional area of a circle: A = π(d/2)² [m²]"""
        return np.pi * (d / 2) ** 2
 
    def radius_at(self, x: np.ndarray) -> np.ndarray:
        """
        Return pipe radius at every position x using smooth cosine blending.
 
        In the throat zone the radius varies as:
            r(x) = r2 + (r1 - r2) * (1 + cos(π*(x-3)/2)) / 2   [converging half]
            r(x) = r2 + (r1 - r2) * (1 - cos(π*(x-5)/2)) / 2   [diverging half]
        This guarantees C1 continuity (no kinks at zone boundaries).
        """
        r1 = self.d1 / 2
        r2 = self.d2 / 2
        x = np.asarray(x, dtype=float)
        r = np.empty_like(x)
 
        # Inlet region
        mask_in = x < self.INLET_END
        r[mask_in] = r1
 
        # Converging region  [3 → 5]
        mask_conv = (x >= self.INLET_END) & (x <= self.THROAT_MID)
        t = (x[mask_conv] - self.INLET_END) / (self.THROAT_MID - self.INLET_END)
        r[mask_conv] = r2 + (r1 - r2) * (1 + np.cos(np.pi * t)) / 2
 
        # Diverging region  [5 → 7]
        mask_div = (x > self.THROAT_MID) & (x <= self.OUTLET_START)
        t = (x[mask_div] - self.THROAT_MID) / (self.OUTLET_START - self.THROAT_MID)
        r[mask_div] = r2 + (r1 - r2) * (1 - np.cos(np.pi * t)) / 2
 
        # Outlet region
        mask_out = x > self.OUTLET_START
        r[mask_out] = r1
 
        return r
 
    def area_at(self, x: np.ndarray) -> np.ndarray:
        """Cross-sectional area A(x) = π·r(x)² [m²]"""
        return np.pi * self.radius_at(x) ** 2
 
    def get_shape(self, n: int = 500):
        """Return (x, radius) arrays for the full pipe profile."""
        x = np.linspace(0, self.PIPE_LENGTH, n)
        return x, self.radius_at(x)
 
    @property
    def A1(self) -> float:
        """Inlet area [m²]"""
        return self.area_from_diameter(self.d1)
 
    @property
    def A2(self) -> float:
        """Throat (minimum) area [m²]"""
        return self.area_from_diameter(self.d2)
 
    @property
    def beta(self) -> float:
        """Diameter ratio β = d2/d1"""
        return self.d2 / self.d1
 
    def __repr__(self):
        return (f"VenturiMeter(d1={self.d1*100:.1f}cm, "
                f"d2={self.d2*100:.1f}cm, β={self.beta:.3f})")
 
 
# ═════════════════════════════════════════════════════════════════
#  CLASS 2 — Fluid
#  Stores all physical properties of the working fluid
# ═════════════════════════════════════════════════════════════════
class Fluid:
    """
    Represents a fluid with its physical properties.
 
    Attributes:
        name     : Human-readable name
        rho      : Density [kg/m³]
        viscosity: Dynamic viscosity [Pa·s] (used for Re number)
        color    : Colour hint for visualisation
    """
 
    # Common fluid presets (density, viscosity)
    PRESETS = {
        "Water (20°C)":  (998.2,  1.002e-3, "#1a6eff"),
        "Water (60°C)":  (983.2,  0.467e-3, "#3388ff"),
        "Oil":           (850.0,  0.030,    "#cc8800"),
        "Air (20°C)":    (1.204,  1.82e-5,  "#88aacc"),
        "Mercury":       (13546., 1.53e-3,  "#aabbcc"),
        "Custom":        (1000.0, 1.0e-3,   "#44aaff"),
    }
 
    def __init__(self, name: str, rho: float, viscosity: float = 1e-3, color: str = "#1a6eff"):
        if rho <= 0:
            raise ValueError("Density must be positive.")
        self.name      = name
        self.rho       = rho
        self.viscosity = viscosity
        self.color     = color
 
    @classmethod
    def from_preset(cls, preset_name: str) -> "Fluid":
        """Factory method — create Fluid from a named preset."""
        if preset_name not in cls.PRESETS:
            raise ValueError(f"Unknown preset: {preset_name}")
        rho, mu, col = cls.PRESETS[preset_name]
        return cls(name=preset_name, rho=rho, viscosity=mu, color=col)
 
    def __repr__(self):
        return f"Fluid(name='{self.name}', ρ={self.rho} kg/m³)"
 
 
# ═════════════════════════════════════════════════════════════════
#  CLASS 3 — FlowCalculator
#  All physics: velocities, pressures, flow rate, Reynolds number
# ═════════════════════════════════════════════════════════════════
class FlowCalculator:
    """
    Applies Bernoulli's principle + continuity equation to compute
    all flow quantities for a given VenturiMeter, Fluid, and ΔP.
 
    Core equations:
      Continuity:  A1·v1 = A2·v2  →  v(x) = A1·v1 / A(x)
      Bernoulli:   P1 + ½ρv1² = P2 + ½ρv2²
      Flow rate:   Q = A2 · √(2ΔP / (ρ·((A1/A2)²−1)))
    """
 
    def __init__(self, venturi: VenturiMeter, fluid: Fluid, delta_p: float):
        """
        Args:
            venturi : VenturiMeter object
            fluid   : Fluid object
            delta_p : Differential pressure P1 − P2  [Pa]
        """
        if delta_p <= 0:
            raise ValueError("Pressure difference must be positive.")
        self.venturi = venturi
        self.fluid   = fluid
        self.delta_p = delta_p
 
        # Pre-compute core values once
        self._v1, self._v2 = self._compute_velocities()
 
    # ── Core calculations ─────────────────────────────────────────
    def _compute_velocities(self):
        """
        Solve for v2 from Bernoulli + continuity, then find v1.
 
        v2 = √( 2·ΔP / (ρ·((A1/A2)² − 1)) )
        v1 = (A2/A1) · v2
        """
        A1  = self.venturi.A1
        A2  = self.venturi.A2
        rho = self.fluid.rho
 
        ratio = (A1 / A2) ** 2 - 1
        v2 = np.sqrt((2 * self.delta_p) / (rho * ratio))
        v1 = (A2 / A1) * v2
        return v1, v2
 
    @property
    def v1(self) -> float:
        """Inlet velocity [m/s]"""
        return self._v1
 
    @property
    def v2(self) -> float:
        """Throat velocity [m/s]"""
        return self._v2
 
    @property
    def flow_rate(self) -> float:
        """Volumetric flow rate Q = A1·v1  [m³/s]"""
        return self.venturi.A1 * self._v1
 
    def velocity_profile(self, x: np.ndarray) -> np.ndarray:
        """
        Smooth velocity at every x position using continuity:
            v(x) = (A1 · v1) / A(x)
 
        Args:
            x: Position array [normalised pipe units]
        Returns:
            velocity array [m/s]
        """
        A_x = self.venturi.area_at(x)
        return (self.venturi.A1 * self._v1) / A_x
 
    def pressure_profile(self, x: np.ndarray) -> np.ndarray:
        """
        Pressure at every x from Bernoulli's equation:
            P(x) = P1 − ½ρ(v(x)² − v1²)
 
        Reference: P1 at inlet = 0 (relative pressure)
        Returns gauge pressure relative to inlet [Pa]
        """
        v_x = self.velocity_profile(x)
        # ΔP_x = ½ρ(v1² - v_x²)  → negative at throat (pressure drops)
        return 0.5 * self.fluid.rho * (self._v1**2 - v_x**2)
 
    def reynolds_number(self) -> float:
        """Re = ρ·v1·D1 / μ  (based on inlet conditions)"""
        return (self.fluid.rho * self._v1 * self.venturi.d1) / self.fluid.viscosity
 
    def flow_regime(self) -> str:
        re = self.reynolds_number()
        if re < 2300:  return "Laminar"
        elif re < 4000: return "Transitional"
        return "Turbulent"
 
    def __repr__(self):
        return (f"FlowCalculator(v1={self._v1:.3f} m/s, "
                f"v2={self._v2:.3f} m/s, Q={self.flow_rate*1000:.3f} L/s)")
 
 
# ═════════════════════════════════════════════════════════════════
#  CLASS 4 — Simulation
#  All visualisation: static plots + animated particle flow
# ═════════════════════════════════════════════════════════════════
class Simulation:
    """
    Handles all visual output for the Venturi meter simulation.
 
    Methods:
        velocity_graph()   — smooth velocity vs. position plot
        pressure_graph()   — pressure distribution plot
        combined_graph()   — side-by-side velocity + pressure
        animate()          — particle-based animated flow
    """
 
    # ── Colour scheme ─────────────────────────────────────────────
    PIPE_COLOR      = "#1a3a5a"
    PIPE_WALL_COLOR = "#0d2035"
    BG_COLOR        = "#060d18"
    GRID_COLOR      = "#0a1e30"
    TEXT_COLOR      = "#7db8e0"
    ACCENT_COLOR    = "#00aaff"
 
    def __init__(self, venturi: VenturiMeter, flow: FlowCalculator):
        self.venturi = venturi
        self.flow    = flow
 
    # ── Shared matplotlib style ───────────────────────────────────
    def _style_axes(self, fig, ax, title: str, xlabel: str, ylabel: str):
        """Apply consistent dark theme styling to any axes."""
        fig.patch.set_facecolor(self.BG_COLOR)
        ax.set_facecolor(self.BG_COLOR)
        ax.set_title(title, color=self.TEXT_COLOR, fontsize=13,
                     fontfamily="monospace", pad=12)
        ax.set_xlabel(xlabel, color=self.TEXT_COLOR, fontsize=10)
        ax.set_ylabel(ylabel, color=self.TEXT_COLOR, fontsize=10)
        ax.tick_params(colors=self.TEXT_COLOR, labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor("#0d2a40")
        ax.grid(True, color=self.GRID_COLOR, linewidth=0.7, linestyle="--", alpha=0.6)
 
    def _draw_pipe_outline(self, ax, x, radius, wall_frac=0.08):
        """Draw the venturi pipe outline on given axes."""
        wall = max(self.venturi.d1 * wall_frac, 0.008)
        ax.fill_between(x,  radius,  radius + wall, color="#0d2540", zorder=3)
        ax.fill_between(x, -radius, -radius - wall, color="#0d2540", zorder=3)
        ax.plot(x,  radius,     color="#1a4a70", linewidth=1.5, zorder=4)
        ax.plot(x, -radius,     color="#1a4a70", linewidth=1.5, zorder=4)
        ax.plot(x,  radius+wall, color="#0a3050", linewidth=0.8, zorder=4)
        ax.plot(x, -radius-wall, color="#0a3050", linewidth=0.8, zorder=4)
 
    # ── Plot 1: Velocity Graph ────────────────────────────────────
    def velocity_graph(self) -> plt.Figure:
        """
        Smooth velocity profile v(x) = A1·v1 / A(x).
        Colour-coded line: blue (slow) → red (fast).
        """
        x = np.linspace(0, 10, 600)
        r = self.venturi.radius_at(x)
        v = self.flow.velocity_profile(x)
 
        fig, ax = plt.subplots(figsize=(12, 4.5))
        self._style_axes(fig, ax,
                         "Velocity Distribution Along the Venturi Meter",
                         "Position along pipe (normalised)", "Velocity  (m/s)")
 
        # Colour-mapped line
        from matplotlib.collections import LineCollection
        points = np.array([x, v]).T.reshape(-1, 1, 2)
        segs   = np.concatenate([points[:-1], points[1:]], axis=1)
        norm   = Normalize(vmin=v.min(), vmax=v.max())
        lc     = LineCollection(segs, cmap="plasma", norm=norm, linewidth=3, zorder=5)
        lc.set_array(v)
        ax.add_collection(lc)
 
        # Fill under curve
        ax.fill_between(x, 0, v, alpha=0.12, color="#00aaff", zorder=2)
 
        # Zone markers
        for xv, lbl, side in [(1.5,"INLET","left"), (5.0,"THROAT","center"), (8.5,"OUTLET","right")]:
            ax.axvline(xv if lbl!="THROAT" else 5.0,
                       color="#1a4a70", linewidth=0.8, linestyle=":", zorder=3)
            ax.text(xv, v.max()*1.06, lbl,
                    ha=side, color="#4db8ff", fontsize=8,
                    fontfamily="monospace", alpha=0.85)
 
        ax.axvline(3, color="#1e3d5a", linewidth=1.2, linestyle="--")
        ax.axvline(7, color="#1e3d5a", linewidth=1.2, linestyle="--")
 
        ax.set_xlim(0, 10)
        ax.set_ylim(0, v.max() * 1.18)
 
        cbar = fig.colorbar(ScalarMappable(norm=norm, cmap="plasma"), ax=ax, pad=0.02)
        cbar.set_label("Velocity (m/s)", color=self.TEXT_COLOR, fontsize=9)
        cbar.ax.yaxis.set_tick_params(color=self.TEXT_COLOR, labelcolor=self.TEXT_COLOR)
 
        plt.tight_layout()
        return fig
 
    # ── Plot 2: Pressure Graph ────────────────────────────────────
    def pressure_graph(self) -> plt.Figure:
        """
        Pressure distribution P(x) = ½ρ(v1² − v(x)²) along the pipe.
        Pressure drops at the throat, partially recovers in diverging section.
        """
        x = np.linspace(0, 10, 600)
        P = self.flow.pressure_profile(x)
        P_kPa = P / 1000
 
        fig, ax = plt.subplots(figsize=(12, 4.5))
        self._style_axes(fig, ax,
                         "Pressure Distribution Along the Venturi Meter",
                         "Position along pipe (normalised)", "Gauge Pressure  (kPa)")
 
        ax.fill_between(x, P_kPa, 0,
                        where=(P_kPa >= 0), color="#0044aa", alpha=0.3, label="High pressure")
        ax.fill_between(x, P_kPa, 0,
                        where=(P_kPa < 0),  color="#aa2200", alpha=0.3, label="Low pressure")
        ax.plot(x, P_kPa, color="#00aaff", linewidth=2.5, zorder=5)
        ax.axhline(0, color="#1a4a70", linewidth=0.8, linestyle="--")
        ax.axvline(3, color="#1e3d5a", linewidth=1.2, linestyle="--")
        ax.axvline(7, color="#1e3d5a", linewidth=1.2, linestyle="--")
 
        for xv, lbl in [(1.5,"INLET"), (5.0,"THROAT"), (8.5,"OUTLET")]:
            ax.text(xv, P_kPa.max()*1.05, lbl,
                    ha="center", color="#4db8ff", fontsize=8, fontfamily="monospace")
 
        ax.legend(facecolor="#0a1628", edgecolor="#1a3550",
                  labelcolor=self.TEXT_COLOR, fontsize=9)
        ax.set_xlim(0, 10)
        plt.tight_layout()
        return fig
 
    # ── Plot 3: Pipe cross-section (static) ───────────────────────
    def pipe_diagram(self) -> plt.Figure:
        """
        Static coloured cross-section diagram of the venturi.
        Colour = velocity (blue→red gradient).
        """
        x = np.linspace(0, 10, 600)
        r = self.venturi.radius_at(x)
        v = self.flow.velocity_profile(x)
 
        norm  = Normalize(vmin=v.min(), vmax=v.max())
        cmap  = plt.cm.RdYlBu_r
 
        fig, ax = plt.subplots(figsize=(13, 4))
        fig.patch.set_facecolor(self.BG_COLOR)
        ax.set_facecolor(self.BG_COLOR)
 
        # Fluid fill (colour-mapped by velocity)
        for i in range(len(x) - 1):
            c = cmap(norm(v[i]))
            ax.fill_between([x[i], x[i+1]],
                            [-r[i], -r[i+1]],
                            [ r[i],  r[i+1]],
                            color=c, alpha=0.88, linewidth=0)
 
        # Centerline
        ax.axhline(0, color="white", linewidth=0.6, linestyle="--", alpha=0.25)
 
        # Pipe walls
        self._draw_pipe_outline(ax, x, r)
 
        # Annotations
        d1, d2 = self.venturi.d1, self.venturi.d2
        ax.annotate("", xy=(0, -d1/2), xytext=(0, d1/2),
                    arrowprops=dict(arrowstyle="<->", color="#4db8ff", lw=1.2))
        ax.text(-0.35, 0, f"D₁\n{d1*100:.1f}cm",
                color="#4db8ff", ha="center", va="center", fontsize=8, fontfamily="monospace")
 
        throat_r = self.venturi.radius_at(np.array([5.0]))[0]
        ax.annotate("", xy=(5.35, -throat_r), xytext=(5.35, throat_r),
                    arrowprops=dict(arrowstyle="<->", color="#ff8844", lw=1.2))
        ax.text(5.85, 0, f"D₂\n{d2*100:.1f}cm",
                color="#ff8844", ha="center", va="center", fontsize=8, fontfamily="monospace")
 
        # Velocity labels
        ax.text(1.5, 0, f"v₁ = {self.flow.v1:.2f} m/s",
                color="white", ha="center", va="center", fontsize=8.5,
                fontfamily="monospace", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#00005588", edgecolor="none"))
        ax.text(5.0, 0, f"v₂ = {self.flow.v2:.2f} m/s",
                color="white", ha="center", va="center", fontsize=8.5,
                fontfamily="monospace", fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.25", facecolor="#88000088", edgecolor="none"))
 
        # Colorbar
        sm = ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cb = fig.colorbar(sm, ax=ax, orientation="horizontal",
                          fraction=0.03, pad=0.02, aspect=45)
        cb.set_label("Velocity (m/s)", color=self.TEXT_COLOR, fontsize=9)
        cb.ax.xaxis.set_tick_params(color=self.TEXT_COLOR, labelcolor=self.TEXT_COLOR)
 
        ax.set_xlim(-0.6, 10.5)
        ax.set_ylim(-d1 * 0.85, d1 * 0.85)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title("Venturi Meter — Cross Section  (colour = velocity)",
                     color=self.TEXT_COLOR, fontsize=11, fontfamily="monospace", pad=10)
 
        plt.tight_layout()
        return fig
 
    # ── Animation ─────────────────────────────────────────────────
    def animate(self, n_particles: int = 1800, n_frames: int = 180):
        """
        Particle-based animated flow simulation.
 
        Physics:
          - Each particle moves at the LOCAL velocity v(x) = A1·v1/A(x)
          - Radial position scaled by parabolic laminar velocity profile:
                v_radial(r) = v_centerline · (1 - (r/R)²)
            → particles near the center advance faster
          - Small transverse Brownian noise for visual realism
          - Particles that exit are re-injected at x=0 with random y
        """
        x_p, r_shape = self.venturi.get_shape(800)
        placeholder  = st.empty()
        prog_bar     = st.progress(0, text="Simulating flow…")
 
        # ── Initialise particle positions ─────────────────────────
        d1  = self.venturi.d1
        px  = np.random.uniform(0, 10, n_particles)
        # Normalised radial positions in [-1, 1]
        pr  = np.random.uniform(-0.95, 0.95, n_particles)
        # Map pr to actual y using local pipe radius
        py  = pr * np.interp(px, x_p, r_shape)
 
        norm     = Normalize(vmin=self.flow.v1, vmax=self.flow.v2 * 1.02)
        cmap_p   = plt.cm.plasma
        pressure = self.flow.pressure_profile(x_p)
        p_norm   = Normalize(vmin=pressure.min(), vmax=pressure.max())
 
        dt       = 0.018   # time step per frame
 
        for frame in range(n_frames):
            # ── Update particle positions ──────────────────────────
            # Local radius and centreline velocity for each particle
            R_local  = np.interp(px, x_p, r_shape)         # pipe radius at px
            v_centre = self.flow.velocity_profile(px)       # centreline velocity
 
            # Laminar radial factor: faster at centre, slower at wall
            r_frac   = np.clip(np.abs(py) / (R_local + 1e-9), 0, 1)
            v_local  = v_centre * (1 - 0.7 * r_frac**2)   # parabolic profile
 
            # Advance + small vertical drift
            px += v_local * dt
            py += np.random.normal(0, 0.003, n_particles)  # Brownian noise
 
            # ── Enforce pipe boundary ──────────────────────────────
            R_now    = np.interp(px, x_p, r_shape)
            outside  = np.abs(py) > R_now * 0.97
            py[outside] = np.sign(py[outside]) * R_now[outside] * np.random.uniform(0.1, 0.8, outside.sum())
 
            # ── Re-inject particles that exited ───────────────────
            exited   = px > 10
            px[exited] = 0
            py[exited] = np.random.uniform(-d1/2 * 0.9, d1/2 * 0.9, exited.sum())
 
            # ── Draw ──────────────────────────────────────────────
            fig, ax = plt.subplots(figsize=(14, 5))
            fig.patch.set_facecolor(self.BG_COLOR)
            ax.set_facecolor(self.BG_COLOR)
 
            # Background pressure gradient
            for i in range(len(x_p) - 1):
                p_val = (pressure[i] - pressure.min()) / (pressure.max() - pressure.min() + 1e-9)
                c = plt.cm.coolwarm_r(p_val * 0.6 + 0.2)
                ax.fill_between([x_p[i], x_p[i+1]],
                                [-r_shape[i], -r_shape[i+1]],
                                [ r_shape[i],  r_shape[i+1]],
                                color=c, alpha=0.18, linewidth=0)
 
            # Particle colours — velocity-mapped
            v_vis    = self.flow.velocity_profile(px)
            colors_p = cmap_p(norm(v_vis))
 
            # Particle size — larger at throat (more energetic)
            v_norm_sz = norm(v_vis)
            sizes     = 1.5 + v_norm_sz * 5
 
            ax.scatter(px, py, c=colors_p, s=sizes, alpha=0.75, linewidths=0, zorder=5)
 
            # Pipe walls
            self._draw_pipe_outline(ax, x_p, r_shape)
            ax.axhline(0, color="white", linewidth=0.4, linestyle="--", alpha=0.15)
 
            # Labels
            ax.text(1.5,  d1*0.72, "HIGH P  /  LOW v",
                    color="#4488cc", ha="center", fontsize=7.5, fontfamily="monospace", alpha=0.7)
            ax.text(5.0,  self.venturi.d2/2 * 1.2 + d1*0.08, "LOW P  /  HIGH v",
                    color="#ff6644", ha="center", fontsize=7.5, fontfamily="monospace", alpha=0.85)
            ax.text(8.5,  d1*0.72, "PRESSURE RECOVERY",
                    color="#4488cc", ha="center", fontsize=7.5, fontfamily="monospace", alpha=0.6)
 
            ax.set_title(f"Live Flow Simulation  —  Frame {frame+1}/{n_frames}  "
                         f"|  Q = {self.flow.flow_rate*1000:.3f} L/s  "
                         f"|  v₂ = {self.flow.v2:.2f} m/s",
                         color=self.TEXT_COLOR, fontsize=10, fontfamily="monospace")
 
            ax.set_xlim(-0.1, 10.1)
            ax.set_ylim(-d1 * 0.82, d1 * 0.82)
            ax.set_aspect("equal")
            ax.axis("off")
 
            plt.tight_layout()
            placeholder.pyplot(fig)
            plt.close(fig)
 
            prog_bar.progress((frame + 1) / n_frames,
                              text=f"Frame {frame+1}/{n_frames}")
            time.sleep(0.04)
 
        prog_bar.empty()
        placeholder.empty()
        st.success("✅ Animation complete!")
 
 
# ═════════════════════════════════════════════════════════════════
#  QUIZ DATA
# ═════════════════════════════════════════════════════════════════
QUIZ_BANK = {
    "Easy": [
        {
            "q": "Where is fluid velocity maximum in a Venturi meter?",
            "options": ["Inlet", "Throat", "Outlet", "Same everywhere"],
            "answer": "Throat",
            "topic": "Concept",
            "explain": "By continuity A₁v₁ = A₂v₂. The throat has smallest area → highest velocity."
        },
        {
            "q": "Where is static pressure lowest in a Venturi meter?",
            "options": ["Inlet", "Throat", "Outlet", "All equal"],
            "answer": "Throat",
            "topic": "Concept",
            "explain": "Bernoulli: high velocity ↔ low pressure. Throat has max velocity → min pressure."
        },
        {
            "q": "What does a Venturi meter measure?",
            "options": ["Temperature", "Viscosity", "Flow rate", "Density"],
            "answer": "Flow rate",
            "topic": "Application",
            "explain": "Venturi meters measure volumetric flow rate using the measured pressure difference."
        },
        {
            "q": "Which physical law is the basis of Venturi meter operation?",
            "options": ["Newton's Law", "Bernoulli's Equation", "Ohm's Law", "Hooke's Law"],
            "answer": "Bernoulli's Equation",
            "topic": "Theory",
            "explain": "Bernoulli's equation relates pressure and velocity — the core physics of the Venturi."
        },
    ],
    "Medium": [
        {
            "q": "If the throat diameter is halved (keeping inlet same), what happens to throat velocity?",
            "options": ["Doubles", "Halves", "Quadruples", "Unchanged"],
            "answer": "Quadruples",
            "topic": "Continuity",
            "explain": "A ∝ d², so halving d → A reduces by 4×. By continuity v₂ = (A₁/A₂)·v₁ → 4×."
        },
        {
            "q": "The continuity equation A₁v₁ = A₂v₂ assumes the fluid is:",
            "options": ["Compressible", "Incompressible", "Viscous", "Turbulent"],
            "answer": "Incompressible",
            "topic": "Theory",
            "explain": "Continuity in this form requires constant density (incompressible fluid)."
        },
        {
            "q": "If ΔP doubles, the throat velocity v₂ changes by a factor of:",
            "options": ["2", "4", "√2", "1/√2"],
            "answer": "√2",
            "topic": "Formula",
            "explain": "v₂ ∝ √(ΔP). So doubling ΔP gives v₂ × √2 ≈ 1.414."
        },
        {
            "q": "The discharge coefficient Cd accounts for:",
            "options": ["Pipe length", "Real fluid losses (viscosity, turbulence)", "Fluid colour", "Pipe material"],
            "answer": "Real fluid losses (viscosity, turbulence)",
            "topic": "Application",
            "explain": "Bernoulli assumes ideal flow. Cd < 1 corrects for friction and turbulence losses."
        },
    ],
    "Hard": [
        {
            "q": "The term (1 − β⁴) in the Venturi formula comes from:",
            "options": [
                "Accounting for non-zero inlet velocity",
                "Pipe friction factor",
                "Fluid compressibility",
                "Wall roughness correction"
            ],
            "answer": "Accounting for non-zero inlet velocity",
            "topic": "Derivation",
            "explain": "When deriving Q, both v₁ and v₂ appear. Substituting v₁=(A₂/A₁)v₂ gives the (1−β⁴) denominator."
        },
        {
            "q": "Reynolds number at the throat is ___ compared to inlet (same fluid):",
            "options": [
                "Lower, because diameter is smaller",
                "Higher, because velocity is higher",
                "Same, because mass flow is conserved",
                "Cannot be determined"
            ],
            "answer": "Higher, because velocity is higher",
            "topic": "Reynolds",
            "explain": "Re = ρvD/μ. At throat: v is much larger; D is smaller. Net effect: Re₂ > Re₁ for typical β."
        },
        {
            "q": "A Venturi meter recovers most of its pressure in the diverging section because:",
            "options": [
                "Fluid speeds up again",
                "The gradual angle prevents boundary layer separation",
                "Pipe diameter decreases again",
                "Temperature drops"
            ],
            "answer": "The gradual angle prevents boundary layer separation",
            "topic": "Design",
            "explain": "The ~7° diverging angle is deliberately gradual to keep flow attached, allowing kinetic energy to convert back to pressure."
        },
        {
            "q": "For β = 0.5, what is the velocity ratio v₂/v₁?",
            "options": ["2", "4", "0.5", "0.25"],
            "answer": "4",
            "topic": "Calculation",
            "explain": "v₂/v₁ = A₁/A₂ = (D₁/D₂)² = (1/0.5)² = 4."
        },
    ]
}
 
NOTES_CONTENT = {
    "What is a Venturi Meter?": {
        "icon": "📐",
        "color": "#0077cc",
        "body": """
A **Venturi meter** is a differential-pressure flow measurement device invented by
Clemens Herschel in 1887, based on principles described by Giovanni Battista Venturi (1797).
 
It measures the **volumetric flow rate** of a fluid in a pipe by forcing the fluid through a
carefully shaped constriction and measuring the resulting pressure difference.
 
**Key advantages:**
- No moving parts → highly reliable and low maintenance
- Low permanent pressure loss (85–90% pressure recovery)
- High accuracy: ±0.5–1% when properly installed
- Bidirectional flow capability
- Works with liquids, gases, and steam
""",
    },
    "Working Principle": {
        "icon": "⚙️",
        "color": "#00aa55",
        "body": """
The Venturi meter works on the combination of two fundamental laws:
 
**Step-by-step operation:**
1. Fluid enters the wide **inlet** at velocity v₁ and pressure P₁
2. The **converging cone** forces the fluid to accelerate
3. At the narrow **throat**, velocity is maximum (v₂) and pressure is minimum (P₂)
4. The **diverging cone** slows the fluid gradually, recovering most of the pressure
5. The pressure difference ΔP = P₁ − P₂ is measured by a manometer or pressure sensor
6. ΔP is used to calculate the flow rate Q using the Venturi formula
 
**Key insight:** The same volumetric flow (m³/s) must pass through a smaller area
→ it must travel faster. The energy that goes into speed comes from pressure.
""",
    },
    "Bernoulli's Equation": {
        "icon": "📊",
        "color": "#aa5500",
        "body": """
For steady, incompressible, inviscid flow along a streamline:
 
$$P_1 + \\frac{1}{2}\\rho v_1^2 = P_2 + \\frac{1}{2}\\rho v_2^2 = \\text{constant}$$
 
Each term represents **energy per unit volume** [Pa = J/m³]:
 
| Term | Name | Meaning |
|------|------|---------|
| P | Static pressure | "Squeezing" energy |
| ½ρv² | Dynamic pressure | Kinetic energy |
| Total | Stagnation pressure | Maximum if flow stopped |
 
**Key conclusion:** At the throat, v is maximum → dynamic pressure is maximum
→ static pressure P₂ must be **minimum**.
 
Rearranging:  ΔP = P₁ − P₂ = ½ρ(v₂² − v₁²)
""",
    },
    "Continuity Equation": {
        "icon": "🔄",
        "color": "#6600cc",
        "body": """
For an **incompressible fluid** (constant density), conservation of mass requires:
 
$$A_1 v_1 = A_2 v_2 = Q \\quad \\text{(volumetric flow rate)}$$
 
**Physical meaning:** What goes in must come out.
If the cross-section shrinks, the velocity must increase proportionally.
 
**Derived velocity ratio:**
$$\\frac{v_2}{v_1} = \\frac{A_1}{A_2} = \\left(\\frac{D_1}{D_2}\\right)^2 = \\frac{1}{\\beta^2}$$
 
**Example:** For β = D₂/D₁ = 0.5 → v₂/v₁ = 4 (throat velocity is 4× the inlet)
 
**Smooth velocity profile:** At any position x along the pipe:
$$v(x) = \\frac{A_1 \\cdot v_1}{A(x)}$$
This is the equation used in the simulation to draw the smooth velocity curve.
""",
    },
    "Venturi Flow Formula": {
        "icon": "📐",
        "color": "#0055aa",
        "body": """
Combining Bernoulli + Continuity and solving for flow rate:
 
**Ideal flow rate:**
$$Q_{ideal} = A_2 \\sqrt{\\frac{2\\,\\Delta P}{\\rho\\,(1 - \\beta^4)}}$$
 
**Actual flow rate** (corrected for real losses):
$$Q_{actual} = C_d \\cdot A_2 \\sqrt{\\frac{2\\,\\Delta P}{\\rho\\,(1 - \\beta^4)}}$$
 
**Throat velocity** (used in simulation):
$$v_2 = \\sqrt{\\frac{2\\,\\Delta P}{\\rho\\left(\\left(\\frac{A_1}{A_2}\\right)^2 - 1\\right)}}$$
 
Where:
- ΔP = P₁ − P₂ = differential pressure [Pa]
- ρ = fluid density [kg/m³]
- β = D₂/D₁ = diameter ratio
- Cᵈ = discharge coefficient (≈ 0.95–0.99 for turbulent flow)
""",
    },
    "Construction & Components": {
        "icon": "🔧",
        "color": "#aa0044",
        "body": """
**Three main sections:**
 
**1. Converging Cone (Inlet)**
- Half-angle ≈ 21°
- Smoothly accelerates the flow
- Connects full-bore inlet pipe to throat
- Pressure taps measure P₁ here
 
**2. Throat**
- Shortest section, minimum diameter D₂
- Maximum velocity, minimum pressure
- β = D₂/D₁ typically 0.30–0.75
- Pressure tap measures P₂ here
 
**3. Diverging Cone (Diffuser)**
- Half-angle ≈ 7° (deliberately gradual)
- Decelerates fluid, converts kinetic → pressure energy
- Recovers 85–90% of the pressure drop
- Steep angles cause separation → large permanent loss
 
**Why 7° diverging angle?**
A faster expansion causes boundary-layer **separation** (eddies),
wasting energy. The gentle 7° angle keeps flow **attached**, allowing
efficient pressure recovery.
""",
    },
    "Reynolds Number & Flow Regimes": {
        "icon": "🌀",
        "color": "#005533",
        "body": """
$$Re = \\frac{\\rho \\cdot v \\cdot D}{\\mu}$$
 
| Re | Regime | Characteristics |
|----|--------|-----------------|
| < 2,300 | **Laminar** | Smooth layers, parabolic profile |
| 2,300–4,000 | **Transitional** | Unstable, intermittent turbulence |
| > 4,000 | **Turbulent** | Chaotic mixing, flat velocity profile |
 
**Impact on Venturi meters:**
- Turbulent flow (Re > 10⁴): Cᵈ ≈ 0.98 (near constant — easy to use)
- Laminar flow: Cᵈ varies significantly with Re (harder to calibrate)
- Industrial Venturi meters are typically designed for turbulent flow
 
**Simulation note:** The animation shows a **laminar-like parabolic profile**
where particles near the centreline move faster than those near the wall.
This is physically correct for laminar flow.
""",
    },
    "Real-World Applications": {
        "icon": "🏭",
        "color": "#665500",
        "body": """
| Industry | Application |
|----------|-------------|
| **Water Treatment** | Measuring clean water flow in distribution networks |
| **Oil & Gas** | Metering crude oil and natural gas pipelines |
| **Power Plants** | Monitoring steam flow, coolant circuits |
| **HVAC Systems** | Measuring air flow in ventilation ducts |
| **Chemical Plants** | Flow control in process pipelines |
| **Medical** | Oxygen flow in ventilators (venturi principle) |
| **Automotive** | Carburetors (fuel-air mixing using venturi effect) |
| **Aerospace** | Pitot-venturi airspeed measurement in aircraft |
 
**Compared to other flow meters:**
 
| Feature | Venturi | Orifice Plate | Turbine |
|---------|---------|---------------|---------|
| Accuracy | ±0.5–1% | ±1–2% | ±0.5% |
| Pressure loss | Low (10–15%) | High (60%) | Medium |
| Moving parts | None | None | Yes |
| Cost | High | Low | Medium |
""",
    },
}
 
 
# ═════════════════════════════════════════════════════════════════
#  STREAMLIT APP — MAIN ENTRY POINT
# ═════════════════════════════════════════════════════════════════
 
# ── Sidebar navigation ────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 1rem;">
      <div style="font-family:'Space Mono',monospace; font-size:1.3rem; color:#00aaff; font-weight:700;">💧 VENTURI</div>
      <div style="font-family:'Space Mono',monospace; font-size:0.6rem; color:#2a6a8a; letter-spacing:0.25em; margin-top:4px;">FLOW SIMULATION</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    menu = st.selectbox(
        "NAVIGATE",
        ["🔬 Simulation", "📚 Notes", "🧠 Quiz"],
        label_visibility="visible"
    )
    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Space Mono',monospace; font-size:0.62rem; color:#1a4060; text-align:center; line-height:1.8;">
      Semester 2 · OOP Project<br>
      Python · Streamlit<br>
      Bernoulli + Continuity
    </div>
    """, unsafe_allow_html=True)
 
 
# ═════════════════════════════════════════════════════════════════
#  SECTION 1 — SIMULATION
# ═════════════════════════════════════════════════════════════════
if menu == "🔬 Simulation":
 
    st.markdown("""
    <div class="page-banner">
      <h1>💧 Venturi Meter Flow Simulation</h1>
      <p>Adjust parameters · Observe physics · Animate particle flow</p>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Input controls ────────────────────────────────────────────
    ctrl_col, main_col = st.columns([1, 2.4])
 
    with ctrl_col:
        st.markdown('<p class="sec-heading">Fluid</p>', unsafe_allow_html=True)
 
        fluid_choice = st.selectbox("Fluid preset", list(Fluid.PRESETS.keys()), index=0)
        if fluid_choice == "Custom":
            rho_val = st.number_input("Density (kg/m³)", 1.0, 20000.0, 1000.0, step=10.0)
            fluid = Fluid("Custom", rho_val)
        else:
            fluid = Fluid.from_preset(fluid_choice)
 
        st.markdown('<p class="sec-heading">Meter Geometry</p>', unsafe_allow_html=True)
        d1 = st.slider("Inlet diameter D₁ (m)", 0.10, 1.00, 0.50, step=0.01, format="%.2f")
        d2 = st.slider("Throat diameter D₂ (m)", 0.05, d1 - 0.01,
                       min(0.20, d1 - 0.05), step=0.01, format="%.2f")
 
        st.markdown('<p class="sec-heading">Operating Condition</p>', unsafe_allow_html=True)
        dp = st.slider("Pressure difference ΔP (Pa)", 100, 50000, 3000, step=100)
 
        # ── Build objects ──────────────────────────────────────────
        try:
            venturi = VenturiMeter(d1, d2)
            flow    = FlowCalculator(venturi, fluid, dp)
            sim     = Simulation(venturi, flow)
            ok      = True
        except Exception as e:
            st.error(f"Error: {e}")
            ok = False
 
        if ok:
            beta = venturi.beta
            if 0.30 <= beta <= 0.75:
                st.success(f"β = {beta:.3f} ✓ (recommended 0.30–0.75)")
            else:
                st.warning(f"β = {beta:.3f} ⚠ outside recommended range")
 
            # Key metrics
            re   = flow.reynolds_number()
            reg  = flow.flow_regime()
            reg_color = {"Laminar": "#00cc66", "Transitional": "#ffaa00", "Turbulent": "#ff4444"}[reg]
 
            st.markdown(f"""
            <div class="metric-grid">
              <div class="metric-box">
                <span class="m-label">v₁  inlet</span>
                <span class="m-value">{flow.v1:.3f}</span>
                <span class="m-unit">m/s</span>
              </div>
              <div class="metric-box">
                <span class="m-label">v₂  throat</span>
                <span class="m-value">{flow.v2:.3f}</span>
                <span class="m-unit">m/s</span>
              </div>
            </div>
            <div class="metric-grid">
              <div class="metric-box">
                <span class="m-label">Flow rate Q</span>
                <span class="m-value">{flow.flow_rate*1000:.3f}</span>
                <span class="m-unit">L/s</span>
              </div>
              <div class="metric-box">
                <span class="m-label">Re number</span>
                <span class="m-value" style="font-size:1.1rem">{re:,.0f}</span>
                <span class="m-unit" style="color:{reg_color}">{reg}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)
 
            st.markdown('<p class="sec-heading">Animation</p>', unsafe_allow_html=True)
            n_frames = st.slider("Frames", 40, 300, 120, step=20)
            n_part   = st.slider("Particles", 500, 3000, 1500, step=250)
 
            run_anim = st.button("▶  Start Animation", use_container_width=True,
                                 type="primary")
 
    # ── Main visualisation panel ──────────────────────────────────
    with main_col:
        if ok:
            tab_cs, tab_vel, tab_pres = st.tabs(
                ["Cross-Section", "Velocity Profile", "Pressure Profile"]
            )
            with tab_cs:
                st.pyplot(sim.pipe_diagram(), use_container_width=True)
                st.caption(
                    "Colour gradient shows fluid velocity — blue = slow (inlet / outlet), "
                    "red = fast (throat).  Pipe walls in dark blue."
                )
            with tab_vel:
                st.pyplot(sim.velocity_graph(), use_container_width=True)
                st.caption(
                    "Smooth v(x) = A₁·v₁ / A(x) — derived from area variation, not hardcoded. "
                    "Colour from plasma colourmap (cool = slow, warm = fast)."
                )
            with tab_pres:
                st.pyplot(sim.pressure_graph(), use_container_width=True)
                st.caption(
                    "Gauge pressure P(x) = ½ρ(v₁² − v(x)²) relative to inlet.  "
                    "Pressure dips below zero (relative) at the throat."
                )
 
    # ── Animation (full-width below controls) ────────────────────
    if ok and run_anim:
        st.markdown("---")
        st.markdown('<p class="sec-heading">Particle Flow Animation</p>',
                    unsafe_allow_html=True)
        sim.animate(n_particles=n_part, n_frames=n_frames)
 
 
# ═════════════════════════════════════════════════════════════════
#  SECTION 2 — NOTES
# ═════════════════════════════════════════════════════════════════
elif menu == "📚 Notes":
 
    st.markdown("""
    <div class="page-banner">
      <h1>📚 Theory & Notes</h1>
      <p>Complete reference — concepts, derivations, and applications</p>
    </div>
    """, unsafe_allow_html=True)
 
    for topic, data in NOTES_CONTENT.items():
        with st.expander(f"{data['icon']}  {topic}", expanded=False):
            # Colour accent bar
            st.markdown(
                f'<div style="height:3px;background:{data["color"]};'
                f'border-radius:2px;margin-bottom:1rem;"></div>',
                unsafe_allow_html=True
            )
            # Render content (supports markdown + LaTeX via st.markdown)
            body = data["body"].strip()
            # Split out LaTeX blocks for st.latex
            st.markdown(body)
 
    # ── Formula quick-reference ───────────────────────────────────
    st.markdown("---")
    st.markdown('<p class="sec-heading">Formula Quick Reference</p>',
                unsafe_allow_html=True)
 
    f1, f2 = st.columns(2)
    with f1:
        with st.container(border=True):
            st.markdown("**Continuity Equation**")
            st.latex(r"A_1 v_1 = A_2 v_2 = Q")
            st.caption("Conservation of mass for incompressible flow")
        with st.container(border=True):
            st.markdown("**Ideal Flow Rate**")
            st.latex(r"Q = A_2\sqrt{\frac{2\,\Delta P}{\rho\,(1-\beta^4)}}")
            st.caption("β = D₂/D₁ is the diameter ratio")
        with st.container(border=True):
            st.markdown("**Reynolds Number**")
            st.latex(r"Re = \frac{\rho\,v\,D}{\mu}")
            st.caption("Ratio of inertial to viscous forces")
        with st.container(border=True):
            st.markdown("**Throat Area**")
            st.latex(r"A_2 = \frac{\pi D_2^2}{4}")
            st.caption("Cross-sectional area at the throat")
 
    with f2:
        with st.container(border=True):
            st.markdown("**Bernoulli's Equation**")
            st.latex(r"P_1 + \tfrac{1}{2}\rho v_1^2 = P_2 + \tfrac{1}{2}\rho v_2^2")
            st.caption("Energy conservation along a streamline")
        with st.container(border=True):
            st.markdown("**Velocity at Any Point**")
            st.latex(r"v(x) = \frac{A_1\,v_1}{A(x)}")
            st.caption("Smooth velocity from continuity equation")
        with st.container(border=True):
            st.markdown("**Pressure Head**")
            st.latex(r"h = \frac{\Delta P}{\rho\,g}")
            st.caption("Pressure expressed in metres of fluid")
        with st.container(border=True):
            st.markdown("**Diameter Ratio**")
            st.latex(r"\beta = \frac{D_2}{D_1}, \quad \text{recommended: } 0.3\leq\beta\leq 0.75")
            st.caption("Key geometric parameter of Venturi design")
 
 
# ═════════════════════════════════════════════════════════════════
#  SECTION 3 — QUIZ
# ═════════════════════════════════════════════════════════════════
elif menu == "🧠 Quiz":
 
    st.markdown("""
    <div class="page-banner">
      <h1>🧠 Concept Quiz</h1>
      <p>Test your understanding · Track weak topics · Improve accuracy</p>
    </div>
    """, unsafe_allow_html=True)
 
    # ── Session state initialisation ──────────────────────────────
    for key, default in [
        ("score", 0), ("attempted", 0),
        ("weak_topics", {}), ("answered", {}),
        ("current_diff", "Easy")
    ]:
        if key not in st.session_state:
            st.session_state[key] = default
 
    # ── Difficulty selector ───────────────────────────────────────
    diff_col, info_col = st.columns([1, 2])
    with diff_col:
        difficulty = st.selectbox(
            "Difficulty Level",
            ["Easy", "Medium", "Hard"],
            index=["Easy","Medium","Hard"].index(st.session_state.current_diff)
        )
        st.session_state.current_diff = difficulty
 
    badge_cls = {"Easy": "badge-easy", "Medium": "badge-medium", "Hard": "badge-hard"}
    badge_info = {"Easy": "4 questions · Core concepts",
                  "Medium": "4 questions · Formula application",
                  "Hard": "4 questions · Deep understanding"}
    with info_col:
        st.markdown(f"""
        <div style="padding:0.8rem 0">
          <span class="{badge_cls[difficulty]}">{difficulty}</span>
          <span style="color:#4a7fa0; font-size:0.85rem; margin-left:0.8rem;">
            {badge_info[difficulty]}
          </span>
        </div>
        """, unsafe_allow_html=True)
 
    st.markdown("---")
 
    questions = QUIZ_BANK[difficulty]
    correct_this_section = 0
 
    # ── Render questions ──────────────────────────────────────────
    for i, q in enumerate(questions):
        q_key  = f"{difficulty}_{i}"
        ans_key = f"ans_{q_key}"
        sub_key = f"sub_{q_key}"
 
        st.markdown(f"""
        <div class="quiz-q">
          <div class="q-num">Question {i+1} of {len(questions)}  ·  {q['topic']}</div>
          <div class="q-text">{q['q']}</div>
        </div>
        """, unsafe_allow_html=True)
 
        user_ans = st.radio(
            f"Select your answer for Q{i+1}",
            q["options"],
            key=ans_key,
            index=None,
            label_visibility="collapsed"
        )
 
        col_btn, col_res = st.columns([1, 3])
        with col_btn:
            submitted = st.button("Submit", key=sub_key, use_container_width=True)
 
        if submitted and user_ans is not None:
            if q_key not in st.session_state.answered:
                st.session_state.attempted += 1
                st.session_state.answered[q_key] = user_ans
                if user_ans == q["answer"]:
                    st.session_state.score += 1
                else:
                    topic = q["topic"]
                    st.session_state.weak_topics[topic] = \
                        st.session_state.weak_topics.get(topic, 0) + 1
 
        if q_key in st.session_state.answered:
            chosen = st.session_state.answered[q_key]
            if chosen == q["answer"]:
                st.success(f"✅  Correct! — {q['explain']}")
                correct_this_section += 1
            else:
                st.error(f"❌  Incorrect. Correct answer: **{q['answer']}**")
                st.info(f"💡 {q['explain']}")
 
        st.markdown("<div style='margin-bottom:0.8rem'></div>", unsafe_allow_html=True)
 
    st.markdown("---")
 
    # ── Score board ───────────────────────────────────────────────
    st.markdown('<p class="sec-heading">Score Board</p>', unsafe_allow_html=True)
 
    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(f"""
        <div class="metric-box" style="text-align:center">
          <span class="m-label">Score</span>
          <span class="m-value">{st.session_state.score}</span>
          <span class="m-unit">correct answers</span>
        </div>""", unsafe_allow_html=True)
    with sc2:
        st.markdown(f"""
        <div class="metric-box" style="text-align:center">
          <span class="m-label">Attempted</span>
          <span class="m-value">{st.session_state.attempted}</span>
          <span class="m-unit">questions total</span>
        </div>""", unsafe_allow_html=True)
    with sc3:
        acc = (st.session_state.score / st.session_state.attempted * 100) \
              if st.session_state.attempted > 0 else 0
        acc_color = "#00cc66" if acc >= 70 else "#ffaa00" if acc >= 40 else "#ff4444"
        st.markdown(f"""
        <div class="metric-box" style="text-align:center">
          <span class="m-label">Accuracy</span>
          <span class="m-value" style="color:{acc_color}">{acc:.1f}%</span>
          <span class="m-unit">overall</span>
        </div>""", unsafe_allow_html=True)
 
    # ── Weak topic analysis ───────────────────────────────────────
    st.markdown('<p class="sec-heading">Weak Topic Analysis</p>', unsafe_allow_html=True)
 
    if st.session_state.weak_topics:
        sorted_weak = sorted(st.session_state.weak_topics.items(),
                             key=lambda x: x[1], reverse=True)
        for topic, count in sorted_weak:
            bar_width = min(count / 5 * 100, 100)
            st.markdown(f"""
            <div style="margin-bottom:0.7rem">
              <div style="display:flex; justify-content:space-between; margin-bottom:3px">
                <span style="color:#c8dce8; font-size:0.88rem; font-family:'Space Mono',monospace">{topic}</span>
                <span style="color:#ff6644; font-size:0.82rem">{count} mistake{'s' if count>1 else ''}</span>
              </div>
              <div style="background:#0a1628; border-radius:4px; height:8px; overflow:hidden">
                <div style="background: linear-gradient(90deg, #cc2200, #ff6644);
                            width:{bar_width}%; height:100%; border-radius:4px;
                            transition:width 0.5s ease;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("**Suggested review:**")
        for topic, _ in sorted_weak[:2]:
            reviews = {
                "Concept":     "Re-read 'What is a Venturi Meter?' and 'Working Principle'",
                "Theory":      "Re-read 'Bernoulli's Equation' and 'Continuity Equation'",
                "Formula":     "Re-read 'Venturi Flow Formula' — study the derivation",
                "Application": "Re-read 'Real-World Applications' and 'Construction'",
                "Continuity":  "Re-read 'Continuity Equation' — work through area ratio examples",
                "Reynolds":    "Re-read 'Reynolds Number & Flow Regimes'",
                "Derivation":  "Re-read derivation in Notes — trace each algebraic step",
                "Calculation": "Practice β calculations: v₂/v₁ = (D₁/D₂)²",
                "Design":      "Re-read 'Construction & Components' — focus on cone angles",
            }
            hint = reviews.get(topic, "Review the Notes section for this topic")
            st.markdown(f"- **{topic}**: {hint}")
    else:
        if st.session_state.attempted > 0:
            st.success("🎉 No weak topics yet — excellent work!")
        else:
            st.info("Complete some questions to see your weak topic analysis.")
 
    # ── Reset button ──────────────────────────────────────────────
    st.markdown("---")
    if st.button("🔄  Reset Quiz", use_container_width=False):
        for key in ["score", "attempted", "weak_topics", "answered"]:
            del st.session_state[key]
        st.rerun()
 
