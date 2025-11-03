import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random, io

# ---------- Page setup ----------
st.set_page_config(page_title="Week 2 • Arts & Advanced Big Data", layout="wide")

# ---------- Blob function ----------
def solar_blob(xc, yc, base_r=1.0, wobble=0.25, spikes=150):
    ang = np.linspace(0, 2*np.pi, spikes)
    r = base_r * (1 + wobble * np.random.randn(spikes))
    x = xc + r * np.cos(ang)
    y = yc + r * np.sin(ang)
    return x, y

# ---------- Pastel Solar Bloom palette ----------
def pastel_palette():
    return [
        (0.98, 0.85, 0.72, 0.42),
        (0.94, 0.78, 0.80, 0.42),
        (0.75, 0.82, 0.89, 0.42),
        (0.89, 0.71, 0.82, 0.42),
        (0.96, 0.78, 0.65, 0.42),
        (0.88, 0.79, 0.89, 0.42),
    ]

# ---------- Generate Poster ----------
def generate_poster(num_layers, num_colors, min_r, max_r, min_wob, max_wob, seed=None):
    if seed:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.axis("off")
    ax.set_facecolor("white")
    palette = pastel_palette()[:num_colors]

    # draw blobs
    for i in range(num_layers):
        color = random.choice(palette)
        ec_color = (0, 0, 0, 0.25)
        r = random.uniform(min_r * 10, max_r * 10)
        x_center = random.uniform(-4, 4)
        y_center = random.uniform(-4, 4)
        wobble = random.uniform(min_wob, max_wob)
        x, y = solar_blob(x_center, y_center, base_r=r, wobble=wobble)
        ax.fill(x, y, color=color, ec=ec_color, lw=0.5)

    # Titles
    ax.text(-6.5, 6.5, "Week2 • Arts & Advanced Big Data",
            fontsize=20, weight="bold", ha="left", va="top")
    ax.text(-6.5, 5.9, "Generative Poster – Solar Bloom",
            fontsize=14, style="italic", ha="left", va="top")

    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    return fig

# ---------- Sidebar Controls ----------
with st.sidebar:
    st.header("🛠️ Controls")
    num_layers = st.slider("Number of Layers", 5, 100, 8)
    num_colors = st.slider("Number of Colors in Palette", 3, 6, 6)
    min_r = st.slider("Minimum Radius", 0.05, 0.3, 0.15)
    max_r = st.slider("Maximum Radius", 0.3, 0.6, 0.45)
    min_wob = st.slider("Min Wobble", 0.01, 0.2, 0.05)
    max_wob = st.slider("Max Wobble", 0.15, 0.4, 0.25)
    seed = st.number_input("Random Seed (optional)", min_value=0, step=1)
    generate = st.button("🎨 Generate Poster")

# ---------- Main layout ----------
st.title("🎨 Generative Abstract Poster")
st.write("Week 2 • Arts & Advanced Big Data")

# ---------- Generate ----------
if generate:
    fig = generate_poster(num_layers, num_colors, min_r, max_r, min_wob, max_wob, seed if seed != 0 else None)
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster (PNG)",
                       data=buf.getvalue(),
                       file_name="Week2_SolarBloom_Advanced.png",
                       mime="image/png")
else:
    st.info("Adjust the sliders and click **Generate Poster** to create your artwork.")
