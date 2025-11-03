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
        (0.98, 0.85, 0.72, 0.45),  # soft yellow
        (0.94, 0.78, 0.80, 0.45),  # pink
        (0.75, 0.82, 0.89, 0.45),  # light blue
        (0.89, 0.71, 0.82, 0.45),  # purple-pink
        (0.96, 0.78, 0.65, 0.45),  # peach
        (0.88, 0.79, 0.89, 0.45),  # lilac
    ]

# ---------- Generate poster ----------
def generate_poster(seed=None):
    if seed:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.axis("off")
    ax.set_facecolor("white")
    palette = pastel_palette()

    # draw blobs with outline (edgecolor)
    for i in range(80):
        color = random.choice(palette)
        ec_color = (0, 0, 0, 0.25)  # subtle gray outline
        r = random.uniform(1.5, 3.0)
        x, y = solar_blob(random.uniform(-3, 3), random.uniform(-3, 3),
                          base_r=r, wobble=random.uniform(0.1, 0.3))
        ax.fill(x, y, color=color, ec=ec_color, lw=0.5)

    # Title text
    ax.text(-6.5, 6.5, "Week2 • Arts & Advanced Big Data", fontsize=20, weight="bold", ha="left", va="top")
    ax.text(-6.5, 5.9, "Generative Poster – Solar Bloom", fontsize=14, style="italic", ha="left", va="top")

    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    return fig

# ---------- Sidebar Controls ----------
with st.sidebar:
    st.header("🎨 Parameters")
    seed = st.number_input("Random Seed (optional)", min_value=0, step=1)
    num_layers = st.slider("Number of Layers", 50, 150, 80)
    min_wobble = st.slider("Min Wobble", 0.05, 0.3, 0.1)
    max_wobble = st.slider("Max Wobble", 0.15, 0.4, 0.25)
    generate = st.button("🌸 Generate Poster")

# ---------- Main layout ----------
st.title("🎨 Generative Abstract Poster")
st.write("Week 2 • Arts & Advanced Big Data")

# ---------- Only show when clicked ----------
if generate:
    fig = generate_poster(seed if seed != 0 else None)
    st.pyplot(fig, use_container_width=True)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button("💾 Download Poster (PNG)",
                       data=buf.getvalue(),
                       file_name="Week2_SolarBloom_Outlined.png",
                       mime="image/png")
else:
    st.info("Adjust the sliders and click **Generate Poster** to create your artwork.")
