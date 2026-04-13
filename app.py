import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Quantum Bloch Sphere Explorer",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main-title {
    font-size: 2rem;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.subtitle {
    color: #6b7280;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.state-card {
    background: linear-gradient(135deg, #f5f7ff 0%, #fff5f8 100%);
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.ket-display {
    font-size: 2.5rem;
    font-weight: 600;
    text-align: center;
    color: #4f46e5;
    letter-spacing: 2px;
    padding: 1rem;
    background: white;
    border-radius: 12px;
    border: 1px solid #e0e7ff;
    margin-bottom: 1rem;
}

.gate-info {
    background: #f0f9ff;
    border-left: 3px solid #0ea5e9;
    border-radius: 0 8px 8px 0;
    padding: 0.75rem 1rem;
    font-size: 0.875rem;
    color: #0c4a6e;
    margin-top: 0.75rem;
    line-height: 1.6;
}

.metric-box {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
}

.metric-label {
    font-size: 0.75rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1f2937;
}

.history-chip {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 99px;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    font-size: 0.75rem;
    font-weight: 500;
    color: #374151;
    margin: 2px;
}

.stButton > button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.measure-result {
    padding: 0.75rem 1rem;
    border-radius: 10px;
    font-weight: 500;
    text-align: center;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)


def complex_norm_sq(c):
    return c.real**2 + c.imag**2


def apply_gate(alpha, beta, gate):
    sq2 = 1 / np.sqrt(2)
    gates = {
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
        "H": np.array([[sq2, sq2], [sq2, -sq2]], dtype=complex),
        "S": np.array([[1, 0], [0, 1j]], dtype=complex),
        "T": np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex),
    }
    state = np.array([alpha, beta], dtype=complex)
    new_state = gates[gate] @ state
    return new_state[0], new_state[1]


def state_to_bloch(alpha, beta):
    a = abs(alpha)
    b = abs(beta)
    theta = 2 * np.arccos(min(1.0, a))
    phi = np.angle(beta) - np.angle(alpha) if abs(alpha) > 1e-9 else 0
    return theta, phi


def draw_bloch_sphere(theta, phi):
    u = np.linspace(0, 2 * np.pi, 60)
    v = np.linspace(0, np.pi, 40)
    x_sphere = np.outer(np.cos(u), np.sin(v))
    y_sphere = np.outer(np.sin(u), np.sin(v))
    z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))

    bx = np.sin(theta) * np.cos(phi)
    by = np.sin(theta) * np.sin(phi)
    bz = np.cos(theta)

    t_arrow = np.linspace(0, 1, 30)
    ax_x = bx * t_arrow
    ax_y = by * t_arrow
    ax_z = bz * t_arrow

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=x_sphere, y=y_sphere, z=z_sphere,
        opacity=0.08,
        colorscale=[[0, '#a5b4fc'], [1, '#818cf8']],
        showscale=False,
        hoverinfo='skip'
    ))

    for lat in np.linspace(-np.pi/2, np.pi/2, 5):
        lx = np.cos(lat) * np.cos(u)
        ly = np.cos(lat) * np.sin(u)
        lz = np.full_like(u, np.sin(lat))
        fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz, mode='lines',
            line=dict(color='rgba(99,102,241,0.15)', width=1), hoverinfo='skip', showlegend=False))

    for lon in np.linspace(0, np.pi, 6):
        lx = np.sin(v) * np.cos(lon)
        ly = np.sin(v) * np.sin(lon)
        lz = np.cos(v)
        fig.add_trace(go.Scatter3d(x=lx, y=ly, z=lz, mode='lines',
            line=dict(color='rgba(99,102,241,0.15)', width=1), hoverinfo='skip', showlegend=False))

    axis_len = 1.3
    for axi in [
        dict(x=[0,axis_len],y=[0,0],z=[0,0],name='X'),
        dict(x=[0,0],y=[0,axis_len],z=[0,0],name='Y'),
        dict(x=[0,0],y=[0,0],z=[0,axis_len],name='Z'),
    ]:
        fig.add_trace(go.Scatter3d(
            x=axi['x'],y=axi['y'],z=axi['z'],mode='lines+text',
            line=dict(color='rgba(107,114,128,0.4)',width=1.5),
            text=['',axi['name']],textfont=dict(size=10,color='#9ca3af'),
            hoverinfo='skip',showlegend=False))

    labels = [
        (0,0,1.22,'|0⟩'),(0,0,-1.22,'|1⟩'),
        (1.22,0,0,'|+⟩'),(-1.22,0,0,'|−⟩'),
        (0,1.22,0,'|+i⟩'),(0,-1.22,0,'|−i⟩'),
    ]
    for lx,ly,lz,lt in labels:
        fig.add_trace(go.Scatter3d(x=[lx],y=[ly],z=[lz],mode='text',
            text=[lt],textfont=dict(size=11,color='#6366f1'),
            hoverinfo='skip',showlegend=False))

    fig.add_trace(go.Scatter3d(
        x=ax_x, y=ax_y, z=ax_z, mode='lines',
        line=dict(color='#4f46e5', width=5),
        hoverinfo='skip', showlegend=False, name='State vector'))

    fig.add_trace(go.Cone(
        x=[bx], y=[by], z=[bz],
        u=[bx*0.15], v=[by*0.15], w=[bz*0.15],
        colorscale=[[0,'#4f46e5'],[1,'#4f46e5']],
        showscale=False, sizemode='absolute', sizeref=0.12,
        hoverinfo='skip'))

    fig.add_trace(go.Scatter3d(
        x=[bx], y=[by], z=[bz], mode='markers',
        marker=dict(size=9, color='#ec4899', symbol='circle'),
        hovertemplate=f'θ={np.degrees(theta):.1f}°<br>φ={np.degrees(phi):.1f}°<extra>State point</extra>',
        name='|ψ⟩'))

    fig.add_trace(go.Scatter3d(
        x=[0,bx], y=[0,0], z=[0,0], mode='lines',
        line=dict(color='rgba(100,100,100,0.2)', width=1, dash='dash'),
        hoverinfo='skip', showlegend=False))

    fig.update_layout(
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=''),
            bgcolor='rgba(0,0,0,0)',
            aspectmode='cube',
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False,
    )
    return fig


def draw_probability_chart(p0, p1):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['|0⟩', '|1⟩'],
        y=[p0*100, p1*100],
        marker_color=['#6366f1', '#ec4899'],
        marker_line_width=0,
        width=0.45,
        hovertemplate='%{y:.1f}%<extra></extra>'
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 105], title='Probability (%)', ticksuffix='%',
                   gridcolor='rgba(0,0,0,0.05)', zeroline=False),
        xaxis=dict(tickfont=dict(size=16, family='Inter')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=10, r=10, t=10, b=10),
        height=200,
        bargap=0.4,
    )
    return fig


GATE_INFO = {
    "X": "**X gate (Pauli-X / NOT gate):** Flips |0⟩ → |1⟩ and |1⟩ → |0⟩. Equivalent to a classical NOT gate. Rotates the Bloch sphere 180° around the X-axis. Matrix: [[0,1],[1,0]]",
    "Y": "**Y gate (Pauli-Y):** Applies both a bit-flip and phase-flip. Maps |0⟩ → i|1⟩ and |1⟩ → −i|0⟩. Rotates 180° around the Y-axis. Matrix: [[0,−i],[i,0]]",
    "Z": "**Z gate (Pauli-Z / phase-flip):** Leaves |0⟩ unchanged but maps |1⟩ → −|1⟩. Doesn't change measurement probability — only phase. Matrix: [[1,0],[0,−1]]",
    "H": "**H gate (Hadamard):** Creates superposition! |0⟩ → (|0⟩+|1⟩)/√2 and |1⟩ → (|0⟩−|1⟩)/√2. This is the most important gate for quantum algorithms. Matrix: (1/√2)[[1,1],[1,−1]]",
    "S": "**S gate (Phase gate):** Applies a 90° phase shift to |1⟩. Maps |1⟩ → i|1⟩ while |0⟩ stays unchanged. Matrix: [[1,0],[0,i]]",
    "T": "**T gate (π/8 gate):** Applies a 45° phase shift. Maps |1⟩ → e^(iπ/4)|1⟩. Used heavily in fault-tolerant quantum computing. Matrix: [[1,0],[0,e^(iπ/4)]]",
}

if 'alpha' not in st.session_state:
    st.session_state.alpha = complex(1, 0)
    st.session_state.beta = complex(0, 0)
    st.session_state.gate_history = []
    st.session_state.last_gate_info = "Start: qubit is in |0⟩ state. Apply gates using the sidebar to transform it!"
    st.session_state.measure_result = None

st.markdown('<h1 class="main-title">⚛️ Quantum Bloch Sphere Explorer</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Visualize qubits, apply quantum gates, and explore superposition in real time</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎛️ Quantum Gates")
    st.caption("Click a gate to apply it to the current qubit state")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("X  (NOT)", use_container_width=True, type="primary"):
            st.session_state.alpha, st.session_state.beta = apply_gate(st.session_state.alpha, st.session_state.beta, "X")
            st.session_state.gate_history.append("X")
            st.session_state.last_gate_info = GATE_INFO["X"]
            st.session_state.measure_result = None
        if st.button("Z  (phase)", use_container_width=True):
            st.session_state.alpha, st.session_state.beta = apply_gate(st.session_state.alpha, st.session_state.beta, "Z")
            st.session_state.gate_history.append("Z")
            st.session_state.last_gate_info = GATE_INFO["Z"]
            st.session_state.measure_result = None
        if st.button("S  gate", use_container_width=True):
            st.session_state.alpha, st.session_state.beta = apply_gate(st.session_state.alpha, st.session_state.beta, "S")
            st.session_state.gate_history.append("S")
            st.session_state.last_gate_info = GATE_INFO["S"]
            st.session_state.measure_result = None
    with col2:
        if st.button("Y  gate", use_container_width=True):
            st.session_state.alpha, st.session_state.beta = apply_gate(st.session_state.alpha, st.session_state.beta, "Y")
            st.session_state.gate_history.append("Y")
            st.session_state.last_gate_info = GATE_INFO["Y"]
            st.session_state.measure_result = None
        if st.button("H  (super)", use_container_width=True, type="primary"):
            st.session_state.alpha, st.session_state.beta = apply_gate(st.session_state.alpha, st.session_state.beta, "H")
            st.session_state.gate_history.append("H")
            st.session_state.last_gate_info = GATE_INFO["H"]
            st.session_state.measure_result = None
        if st.button("T  gate", use_container_width=True):
            st.session_state.alpha, st.session_state.beta = apply_gate(st.session_state.alpha, st.session_state.beta, "T")
            st.session_state.gate_history.append("T")
            st.session_state.last_gate_info = GATE_INFO["T"]
            st.session_state.measure_result = None

    st.divider()

    if st.button("🔄 Reset to |0⟩", use_container_width=True):
        st.session_state.alpha = complex(1, 0)
        st.session_state.beta = complex(0, 0)
        st.session_state.gate_history = []
        st.session_state.last_gate_info = "State reset to |0⟩. Apply gates to explore!"
        st.session_state.measure_result = None

    st.divider()
    st.markdown("## 📐 Measure Qubit")
    st.caption("Collapses superposition to a definite state")
    if st.button("⚡ Measure", use_container_width=True, type="secondary"):
        p0 = complex_norm_sq(st.session_state.alpha)
        result = "|0⟩" if np.random.random() < p0 else "|1⟩"
        st.session_state.measure_result = result
        if result == "|0⟩":
            st.session_state.alpha = complex(1, 0)
            st.session_state.beta = complex(0, 0)
        else:
            st.session_state.alpha = complex(0, 0)
            st.session_state.beta = complex(1, 0)
        st.session_state.gate_history.append("M")
        st.session_state.last_gate_info = f"Measured! State collapsed to {result}. Quantum superposition ends on observation."

    st.divider()
    st.markdown("## 📚 About This App")
    st.caption("Built for Module 2 – Quantum Computing. Demonstrates qubits, Bloch sphere representation, Dirac notation, and single-qubit gate operations as covered in the syllabus.")

alpha = st.session_state.alpha
beta = st.session_state.beta
p0 = complex_norm_sq(alpha)
p1 = complex_norm_sq(beta)
theta, phi = state_to_bloch(alpha, beta)

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("### 🌐 Bloch Sphere")
    st.caption("The state vector (blue arrow) points to |0⟩ at north pole, |1⟩ at south pole, and superpositions on the surface")
    st.plotly_chart(draw_bloch_sphere(theta, phi), use_container_width=True, config={'displayModeBar': False})

with col_right:
    p0_pct = round(p0 * 100)
    p1_pct = round(p1 * 100)

    if p0_pct == 100:
        ket_label = "|0⟩"
    elif p1_pct == 100:
        ket_label = "|1⟩"
    elif p0_pct == 50:
        ket_label = "|+⟩ or |−⟩"
    else:
        ket_label = "|ψ⟩"

    st.markdown(f'<div class="ket-display">{ket_label}</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    m1.metric("P(|0⟩)", f"{p0_pct}%")
    m2.metric("P(|1⟩)", f"{p1_pct}%")
    m3.metric("Gates applied", len([g for g in st.session_state.gate_history if g != 'M']))

    st.markdown("### 📊 Measurement probabilities")
    st.plotly_chart(draw_probability_chart(p0, p1), use_container_width=True, config={'displayModeBar': False})

    if st.session_state.measure_result:
        color = "#ede9fe" if st.session_state.measure_result == "|0⟩" else "#fce7f3"
        tc = "#4f46e5" if st.session_state.measure_result == "|0⟩" else "#db2777"
        st.markdown(f'<div class="measure-result" style="background:{color};color:{tc}">⚡ Measured: {st.session_state.measure_result} — state collapsed!</div>', unsafe_allow_html=True)

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("### 🧮 Qubit state vector")
    norm_check = round(p0 + p1, 4)
    ar, ai = round(alpha.real, 4), round(alpha.imag, 4)
    br, bi = round(beta.real, 4), round(beta.imag, 4)
    ai_str = f"+{ai}i" if ai >= 0 else f"{ai}i"
    bi_str = f"+{bi}i" if bi >= 0 else f"{bi}i"
    st.code(f"|ψ⟩ = α|0⟩ + β|1⟩\n\nα = {ar}{ai_str}\nβ = {br}{bi_str}\n\n|α|² + |β|² = {norm_check} ✓\n\nθ = {round(np.degrees(theta), 2)}°\nφ = {round(np.degrees(phi), 2)}°", language=None)

with col_b:
    st.markdown("### 📖 Gate applied")
    if st.session_state.last_gate_info:
        st.markdown(f'<div class="gate-info">{st.session_state.last_gate_info}</div>', unsafe_allow_html=True)

    if st.session_state.gate_history:
        st.markdown("**Gate sequence:**")
        chips_html = " → ".join([f'<span class="history-chip">{g}</span>' for g in st.session_state.gate_history])
        st.markdown(chips_html, unsafe_allow_html=True)

st.divider()
st.markdown("### 🔬 Quick experiments — try these!")
exp_col1, exp_col2, exp_col3 = st.columns(3)
with exp_col1:
    st.info("**Create |+⟩ state**\nReset → Apply H\nResult: 50/50 superposition")
with exp_col2:
    st.info("**Phase kickback**\nReset → H → Z → H\nResult: same as X gate!")
with exp_col3:
    st.info("**Full rotation**\nApply X → X\nResult: back to |0⟩")

st.markdown("---")
st.caption("⚛️ Quantum Bloch Sphere Explorer · Built with Streamlit & Plotly · Module 2 – Quantum Computing")
