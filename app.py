import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random, io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Generative Poster – Solar Bloom", layout="wide")

# -------------------------------
# SHAPE FUNCTION
# -------------------------------
def solar_bloom(xc, yc, base_radius=1.5, n_arms=8, wobble_min=0.05, wobble_max=0.25, n_points=300):
    """Generate a spiky, solar-bloom style blob."""
    angles = np.linspace(0, 2 * np.pi, n_points)
    wobble = np.random.uniform(wobble_min, wobble_max)
    r = base_radius * (1 + wobble * np.sin(n_arms * angles + random.random() * 2 * np.pi))
    x = xc + r * np.cos(angles)
    y = yc + r * np.sin(angles)
    return x, y

# -------------------------------
# COLOR PALETTE
# -------------------------------
def pastel_palette():
    """Pastel solar tones similar to your Week2 poster."""
    return [
        (0.97, 0.84, 0.72, 0.45),  # peach
        (0.96, 0.77, 0.84, 0.45),  # soft pink
        (0.88, 0.75, 0.92, 0.45),  # lilac
        (0.92, 0.85, 0.95, 0.45),  # lavender
        (0.98, 0.85, 0.65, 0.45),  # warm yellow
    ]

# -------------------------------
# GENERATE POSTER
# -------------------------------
def generate_poster(num_layers, seed, wobble_min, wobble_max, size_min, size_max):
    """Generate the dense solar bloom poster."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis("off")
    ax.set_facecolor("white")
    palette = pastel_palette()

    for _ in range(num_layers * 12):  # high density
        color = random.choice(palette)
        base_r = random.uniform(size_min, size_max) * 1.8  # enlarge flowers
        arms = random.randint(5, 10)
        x_c = random.gauss(0, 2)
        y_c = random.gauss(0, 2)
        x, y = solar_bloom(x_c, y_c, base_radius=base_r, n_arms=arms,
                           wobble_min=wobble_min, wobble_max=wobble_max)
        ax.fill(x, y, color=color, ec="none")

    # Title
    ax.text(-4.5, 4.8, "Week2 • Arts & Advanced Big Data", fontsize=16, weight='bold', ha='left', va='top')
    ax.text(-4.5, 4.3, "Generative Poster – Solar Bloom", fontsize=12, style='italic', ha='left', va='top')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    return fig

# -------------------------------
# INTERFACE
# -------------------------------
st.title("🎨 Generative Abstract Poster")
st.subheader("Week 9 • Arts & Advanced Big Data")

st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    style = st.selectbox("Style Preset", ["Solar Bloom (Default)"], index=0)
with col2:
    num_layers = st.slider("Number of Layers", 5, 20, 8)
with col3:
    seed_input = st.number_input("Random Seed", value=0, step=1)

st.markdown("### Parameters")
colL, colR = st.columns(2)
with colL:
    wobble_min = st.slider("Wobble Min", 0.0, 0.3, 0.05)
    size_min = st.slider("Blob Size Min", 0.1, 0.5, 0.15)
with colR:
    wobble_max = st.slider("Wobble Max", 0.0, 0.5, 0.25)
    size_max = st.slider("Blob Size Max", 0.1, 0.8, 0.35)

generate = st.button("🎨 Generate Poster")

# -------------------------------
# POSTER GENERATION
# -------------------------------
if generate:
    if seed_input == 0:
        seed = random.randint(1, 9999)
    else:
        seed = int(seed_input)
    fig = generate_poster(num_layers, seed, wobble_min, wobble_max, size_min, size_max)
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button(
        "💾 Download Poster (PNG)",
        data=buf.getvalue(),
        file_name="Solar_Bloom_Poster.png",
        mime="image/png"
    )
else:
    st.info("⬅️ Adjust the sliders and click **Generate Poster** to create your artwork.")
