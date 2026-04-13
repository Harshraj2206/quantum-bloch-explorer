import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Quantum Explorer", page_icon="⚛️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #07090f !important;
    color: #e2e8f0 !important;
}
.main .block-container { padding: 2rem 3rem !important; max-width: 1200px !important; }
#MainMenu, footer, header, .stDeployButton { visibility: hidden; }

.hero { text-align: center; padding: 2.5rem 0 2rem; }
.hero h1 {
    font-size: 2.8rem; font-weight: 600; letter-spacing: -0.5px;
    background: linear-gradient(135deg, #818cf8, #38bdf8, #34d399);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0 0 0.5rem;
}
.hero p { color: #475569; font-size: 1rem; margin: 0; }

.card {
    background: #0d1117; border: 1px solid #1e2636;
    border-radius: 18px; padding: 1.5rem; margin-bottom: 1rem;
}
.card-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; color: #334155; margin-bottom: 1rem;
}

.ket {
    font-family: 'Georgia', serif; font-size: 3.2rem; font-weight: 600;
    text-align: center; padding: 1.2rem 0;
    background: linear-gradient(135deg, #818cf8, #38bdf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1;
}

.stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 1rem; }
.stat {
    background: #111827; border: 1px solid #1e2636; border-radius: 12px;
    padding: 0.85rem; text-align: center;
}
.stat-val { font-size: 1.4rem; font-weight: 600; color: #e2e8f0; line-height: 1; margin-bottom: 3px; }
.stat-key { font-size: 0.65rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; }

.prob-bar-wrap { margin-bottom: 0.75rem; }
.prob-label { display: flex; justify-content: space-between; font-size: 0.8rem; color: #64748b; margin-bottom: 5px; }
.prob-track { height: 8px; background: #1e2636; border-radius: 99px; overflow: hidden; }
.prob-fill-0 { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #6366f1, #818cf8); transition: width 0.6s cubic-bezier(0.4,0,0.2,1); }
.prob-fill-1 { height: 100%; border-radius: 99px; background: linear-gradient(90deg, #ec4899, #f472b6); transition: width 0.6s cubic-bezier(0.4,0,0.2,1); }

.gate-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 1rem; }
.gate-info-box {
    background: #111827; border-left: 3px solid #818cf8; border-radius: 0 10px 10px 0;
    padding: 0.85rem 1rem; font-size: 0.82rem; color: #94a3b8; line-height: 1.6;
}
.gate-info-box strong { color: #c7d2fe; }

.history-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 0.75rem; align-items: center; }
.chip {
    font-size: 0.7rem; font-weight: 600; padding: 3px 10px;
    border-radius: 99px; border: 1px solid #1e2636;
    background: #111827; color: #64748b; font-family: monospace;
}
.chip-arrow { color: #334155; font-size: 0.65rem; }
.chip-last { border-color: #6366f1; color: #818cf8; background: #1e1b4b; }
.chip-m { border-color: #ec4899; color: #f472b6; background: #1f0a16; }

.measure-result {
    text-align: center; padding: 0.85rem; border-radius: 12px;
    font-size: 1rem; font-weight: 500; margin-top: 0.75rem;
}

.amp-block {
    font-family: monospace; font-size: 0.82rem; color: #64748b;
    background: #111827; border-radius: 10px; padding: 1rem; line-height: 2;
}
.amp-block span { color: #a5b4fc; }

.experiment-card {
    background: #0d1117; border: 1px solid #1e2636; border-radius: 14px;
    padding: 1rem 1.2rem; height: 100%;
}
.experiment-card h4 { font-size: 0.82rem; font-weight: 600; color: #c7d2fe; margin: 0 0 0.4rem; }
.experiment-card p { font-size: 0.75rem; color: #475569; margin: 0; line-height: 1.5; }
.experiment-card code { color: #38bdf8; font-size: 0.72rem; }

div[data-testid="stButton"] > button {
    background: #111827 !important; color: #94a3b8 !important;
    border: 1px solid #1e2636 !important; border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.85rem !important;
    font-weight: 500 !important; padding: 0.5rem 0.75rem !important;
    transition: all 0.2s !important; width: 100% !important;
}
div[data-testid="stButton"] > button:hover {
    background: #1e1b4b !important; border-color: #6366f1 !important;
    color: #a5b4fc !important; transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button:active { transform: scale(0.97) !important; }
.reset-btn > button { border-color: #1e2636 !important; color: #475569 !important; }
.measure-btn > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    border-color: transparent !important; color: #fff !important;
    font-weight: 600 !important;
}
.measure-btn > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
</style>
""", unsafe_allow_html=True)


# ── Quantum math ──────────────────────────────────────────────
def norm_sq(c): return c.real**2 + c.imag**2

def apply_gate(a, b, g):
    s2 = 1/np.sqrt(2)
    M = {"X": [[0,1],[1,0]], "Y": [[0,-1j],[1j,0]], "Z": [[1,0],[0,-1]],
         "H": [[s2,s2],[s2,-s2]], "S": [[1,0],[0,1j]], "T": [[1,0],[0,np.exp(1j*np.pi/4)]]}
    v = np.array([a, b], dtype=complex)
    r = np.array(M[g], dtype=complex) @ v
    return r[0], r[1]

def state_to_bloch(a, b):
    th = 2*np.arccos(min(1.0, abs(a)))
    ph = np.angle(b) - np.angle(a) if abs(a) > 1e-9 else 0.0
    return th, ph


# ── Bloch sphere ──────────────────────────────────────────────
def bloch_figure(theta, phi):
    bx = np.sin(theta)*np.cos(phi)
    by = np.sin(theta)*np.sin(phi)
    bz = np.cos(theta)

    u = np.linspace(0, 2*np.pi, 72)
    v = np.linspace(0, np.pi,   48)
    sx = np.outer(np.cos(u), np.sin(v))
    sy = np.outer(np.sin(u), np.sin(v))
    sz = np.outer(np.ones(72), np.cos(v))

    fig = go.Figure()

    # sphere shell
    fig.add_trace(go.Surface(x=sx, y=sy, z=sz, opacity=0.06,
        colorscale=[[0,"#6366f1"],[1,"#38bdf8"]], showscale=False, hoverinfo="skip",
        lighting=dict(ambient=1), lightposition=dict(x=0,y=0,z=0)))

    # latitude & longitude grid lines
    for lat in np.linspace(-np.pi/2, np.pi/2, 7):
        cx = np.cos(lat)*np.cos(u); cy = np.cos(lat)*np.sin(u); cz = np.full_like(u, np.sin(lat))
        fig.add_trace(go.Scatter3d(x=cx, y=cy, z=cz, mode="lines", hoverinfo="skip", showlegend=False,
            line=dict(color="rgba(99,102,241,0.12)", width=1)))
    for lon in np.linspace(0, np.pi, 7):
        lx = np.sin(v)*np.cos(lon); ly = np.sin(v)*np.sin(lon); lz = np.cos(v)
        fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz, mode="lines", hoverinfo="skip", showlegend=False,
            line=dict(color="rgba(99,102,241,0.12)", width=1)))

    # equator ring highlight
    fig.add_trace(go.Scatter3d(x=np.cos(u), y=np.sin(u), z=np.zeros_like(u), mode="lines",
        hoverinfo="skip", showlegend=False, line=dict(color="rgba(99,102,241,0.3)", width=2)))

    # axes
    for ax, col, lbl in [([1.35,0,0],[0,0,0],""), ([0,1.35,0],[0,0,0],""), ([0,0,1.35],[0,0,0],"")]:
        fig.add_trace(go.Scatter3d(x=[0,ax[0]], y=[0,ax[1]], z=[0,ax[2]], mode="lines",
            hoverinfo="skip", showlegend=False, line=dict(color="rgba(148,163,184,0.15)", width=1.5)))

    # pole & equator labels
    for lx,ly,lz,lt,fc in [
        (0,0,1.22,"|0⟩","#818cf8"), (0,0,-1.22,"|1⟩","#f472b6"),
        (1.22,0,0,"|+⟩","#38bdf8"), (-1.22,0,0,"|−⟩","#38bdf8"),
    ]:
        fig.add_trace(go.Scatter3d(x=[lx],y=[ly],z=[lz], mode="text",
            text=[lt], textfont=dict(size=12, color=fc), hoverinfo="skip", showlegend=False))

    # state vector line
    t = np.linspace(0, 1, 60)
    fig.add_trace(go.Scatter3d(x=bx*t, y=by*t, z=bz*t, mode="lines",
        line=dict(color="#818cf8", width=6), hoverinfo="skip", showlegend=False))

    # arrowhead cone
    fig.add_trace(go.Cone(x=[bx], y=[by], z=[bz], u=[bx*0.001], v=[by*0.001], w=[bz*0.001],
        sizemode="absolute", sizeref=0.18, anchor="tip",
        colorscale=[[0,"#818cf8"],[1,"#818cf8"]], showscale=False, hoverinfo="skip"))

    # state point glow
    fig.add_trace(go.Scatter3d(x=[bx], y=[by], z=[bz], mode="markers",
        marker=dict(size=10, color="#f472b6",
                    line=dict(color="#fda4af", width=2)),
        hovertemplate=f"θ = {np.degrees(theta):.1f}°<br>φ = {np.degrees(phi):.1f}°<extra>|ψ⟩</extra>",
        showlegend=False))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
            bgcolor="rgba(0,0,0,0)", aspectmode="cube",
            camera=dict(eye=dict(x=1.4, y=1.4, z=0.9))
        ),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0),
        height=420, showlegend=False,
    )
    return fig


# ── Gate metadata ─────────────────────────────────────────────
GATES = {
    "X": {"label":"X  — NOT",   "color":"#6366f1",
          "info":"<strong>Pauli-X (NOT gate)</strong> — flips |0⟩↔|1⟩. Rotates 180° around X-axis. The quantum equivalent of a classical NOT."},
    "Y": {"label":"Y  gate",    "color":"#8b5cf6",
          "info":"<strong>Pauli-Y</strong> — bit-flip + phase-flip. Maps |0⟩→i|1⟩ and |1⟩→−i|0⟩. Rotates 180° around Y-axis."},
    "Z": {"label":"Z  — Phase", "color":"#3b82f6",
          "info":"<strong>Pauli-Z (phase-flip)</strong> — leaves |0⟩ unchanged, maps |1⟩→−|1⟩. Rotates 180° around Z-axis. No change to probabilities."},
    "H": {"label":"H  — Super", "color":"#06b6d4",
          "info":"<strong>Hadamard</strong> — creates perfect superposition. |0⟩→(|0⟩+|1⟩)/√2. The most important gate in quantum computing."},
    "S": {"label":"S  gate",    "color":"#10b981",
          "info":"<strong>S (Phase gate)</strong> — 90° phase rotation. Maps |1⟩→i|1⟩. Equal to two T gates applied together."},
    "T": {"label":"T  gate",    "color":"#f59e0b",
          "info":"<strong>T (π/8 gate)</strong> — 45° phase rotation. Maps |1⟩→e^(iπ/4)|1⟩. Essential for universal fault-tolerant quantum computing."},
}


# ── Session state ─────────────────────────────────────────────
if "alpha" not in st.session_state:
    st.session_state.alpha   = complex(1, 0)
    st.session_state.beta    = complex(0, 0)
    st.session_state.history = []
    st.session_state.info    = "Qubit is in <strong>|0⟩</strong> — the ground state. Apply a gate from the panel below to transform it."
    st.session_state.measured = None


# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>⚛ Quantum Bloch Explorer</h1>
  <p>Visualise qubits · Apply quantum gates · Explore superposition</p>
</div>
""", unsafe_allow_html=True)


# ── Derived state ─────────────────────────────────────────────
alpha = st.session_state.alpha
beta  = st.session_state.beta
p0    = norm_sq(alpha)
p1    = norm_sq(beta)
p0pct = round(p0 * 100)
p1pct = round(p1 * 100)
theta, phi = state_to_bloch(alpha, beta)

if p0pct == 100:   ket = "|0⟩"
elif p1pct == 100: ket = "|1⟩"
elif p0pct == 50:  ket = "(|0⟩+|1⟩)/√2"
else:              ket = "|ψ⟩"

gate_count = len([g for g in st.session_state.history if g != "M"])


# ── Layout: two columns ───────────────────────────────────────
col_sphere, col_panel = st.columns([5, 4], gap="large")

with col_sphere:
    st.markdown('<div class="card"><div class="card-label">Bloch Sphere  ·  drag to rotate</div>', unsafe_allow_html=True)
    st.plotly_chart(bloch_figure(theta, phi), use_container_width=True,
                    config={"displayModeBar": False, "scrollZoom": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_panel:

    # KET + stats
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Current State</div>
      <div class="ket">{ket}</div>
      <div class="stat-grid">
        <div class="stat"><div class="stat-val">{p0pct}%</div><div class="stat-key">P(|0⟩)</div></div>
        <div class="stat"><div class="stat-val">{p1pct}%</div><div class="stat-key">P(|1⟩)</div></div>
        <div class="stat"><div class="stat-val">{gate_count}</div><div class="stat-key">Gates</div></div>
      </div>
      <div class="prob-bar-wrap">
        <div class="prob-label"><span>|0⟩</span><span>{p0pct}%</span></div>
        <div class="prob-track"><div class="prob-fill-0" style="width:{p0pct}%"></div></div>
      </div>
      <div class="prob-bar-wrap">
        <div class="prob-label"><span>|1⟩</span><span>{p1pct}%</span></div>
        <div class="prob-track"><div class="prob-fill-1" style="width:{p1pct}%"></div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Gate info box
    st.markdown(f"""
    <div class="card">
      <div class="card-label">Gate Info</div>
      <div class="gate-info-box">{st.session_state.info}</div>
    """, unsafe_allow_html=True)

    if st.session_state.history:
        chips = ""
        for i, g in enumerate(st.session_state.history):
            is_last = (i == len(st.session_state.history)-1)
            cls = "chip-m" if g == "M" else ("chip-last" if is_last else "chip")
            chips += f'<span class="{cls} chip">{g}</span>'
            if i < len(st.session_state.history)-1:
                chips += '<span class="chip-arrow">›</span>'
        st.markdown(f'<div class="history-wrap">{chips}</div>', unsafe_allow_html=True)

    if st.session_state.measured:
        c = "#1e1b4b" if st.session_state.measured == "|0⟩" else "#1f0a16"
        tc = "#818cf8" if st.session_state.measured == "|0⟩" else "#f472b6"
        st.markdown(f'<div class="measure-result" style="background:{c};color:{tc}">⚡ Collapsed → {st.session_state.measured}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── Gate buttons ──────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-label">Apply a Gate</div>', unsafe_allow_html=True)

g1, g2, g3, g4, g5, g6 = st.columns(6, gap="small")
gate_cols = [g1, g2, g3, g4, g5, g6]

for col, (gname, gmeta) in zip(gate_cols, GATES.items()):
    with col:
        if st.button(gmeta["label"], key=f"btn_{gname}"):
            st.session_state.alpha, st.session_state.beta = apply_gate(
                st.session_state.alpha, st.session_state.beta, gname)
            st.session_state.history.append(gname)
            st.session_state.info = gmeta["info"]
            st.session_state.measured = None
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# ── Measure + Reset row ───────────────────────────────────────
m_col, r_col = st.columns([3, 1], gap="small")

with m_col:
    st.markdown('<div class="measure-btn">', unsafe_allow_html=True)
    if st.button("⚡  Measure  —  collapse the qubit state", key="measure"):
        result = "|0⟩" if np.random.random() < p0 else "|1⟩"
        st.session_state.measured = result
        if result == "|0⟩":
            st.session_state.alpha, st.session_state.beta = complex(1,0), complex(0,0)
        else:
            st.session_state.alpha, st.session_state.beta = complex(0,0), complex(1,0)
        st.session_state.history.append("M")
        st.session_state.info = f"Measured → <strong>{result}</strong>. Superposition collapsed. The qubit is now in a definite state."
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with r_col:
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    if st.button("↺  Reset  |0⟩", key="reset"):
        st.session_state.alpha   = complex(1, 0)
        st.session_state.beta    = complex(0, 0)
        st.session_state.history = []
        st.session_state.info    = "Reset to <strong>|0⟩</strong>. Apply gates to explore quantum superposition."
        st.session_state.measured = None
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ── Amplitudes ────────────────────────────────────────────────
ar = round(alpha.real, 4); ai = round(alpha.imag, 4)
br = round(beta.real, 4);  bi = round(beta.imag, 4)
ai_s = f"+{ai}i" if ai >= 0 else f"{ai}i"
bi_s = f"+{bi}i" if bi >= 0 else f"{bi}i"
norm = round(p0 + p1, 4)

st.markdown(f"""
<div class="card" style="margin-top:0.5rem">
  <div class="card-label">State Vector Amplitudes</div>
  <div class="amp-block">
    |ψ⟩ = α|0⟩ + β|1⟩<br>
    α = <span>{ar}{ai_s}</span> &nbsp;&nbsp; β = <span>{br}{bi_s}</span><br>
    |α|² + |β|² = <span>{norm}</span>  ✓ &nbsp;&nbsp; θ = <span>{round(np.degrees(theta),1)}°</span> &nbsp; φ = <span>{round(np.degrees(phi),1)}°</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Try these experiments ─────────────────────────────────────
st.markdown('<div class="card-label" style="margin-top:1rem">Try these experiments</div>', unsafe_allow_html=True)
e1, e2, e3 = st.columns(3, gap="small")
for col, title, steps, result in [
    (e1, "Perfect superposition", "Reset → H", "50/50 chance on measurement"),
    (e2, "Phase identity", "Reset → H → Z → H", "Same result as X gate!"),
    (e3, "Full rotation", "Reset → X → X", "Back to |0⟩ — full 360°"),
]:
    with col:
        st.markdown(f"""
        <div class="experiment-card">
          <h4>{title}</h4>
          <p><code>{steps}</code><br>{result}</p>
        </div>""", unsafe_allow_html=True)

st.markdown('<p style="text-align:center;color:#1e293b;font-size:0.75rem;margin-top:2.5rem">⚛ Quantum Bloch Explorer · Module 2 Quantum Computing</p>', unsafe_allow_html=True)
