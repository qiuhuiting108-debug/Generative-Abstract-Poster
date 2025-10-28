import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Generative Poster - Solar Bloom", layout="wide")

# -------------------------------
# DEFINE FUNCTIONS
# -------------------------------

def spiky_blob(x_center, y_center, radius=1.0, wobble=0.15, spikes=5, n_points=300):
    """Generate a wobbly circular blob with pointed, spiky edges."""
    angles = np.linspace(0, 2 * np.pi, n_points)
    spike_pattern = 1 + 0.3 * np.sin(spikes * angles + random.random() * 2 * np.pi)
    radii = radius * (1 + wobble * np.random.randn(n_points)) * spike_pattern
    x = x_center + radii * np.cos(angles)
    y = y_center + radii * np.sin(angles)
    return x, y


def sunset_palette():
    """Soft warm tones like the Solar Bloom poster."""
    return [
        (0.98, 0.85, 0.75, 0.45),
        (0.94, 0.78, 0.85, 0.45),
        (0.90, 0.75, 0.95, 0.45),
        (0.95, 0.85, 0.90, 0.45),
        (0.98, 0.88, 0.65, 0.45)
    ]


def generate_solar_bloom(seed=4701, n_arms=12, n_layers=5,
                         radius_base=2.0, wobble_min=0.05, wobble_max=0.25, alpha=0.45):
    """Generate Solar Bloom style poster."""
    np.random.seed(seed)
    random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor("white")

    colors = sunset_palette()
    center_x, center_y = 0, 0

    for arm in range(n_arms):
        theta = 2 * np.pi * arm / n_arms
        for layer in range(1, n_layers + 1):
            distance = layer * 2.5
            x_center = center_x + distance * np.cos(theta)
            y_center = center_y + distance * np.sin(theta)
            radius = radius_base * random.uniform(0.7, 1.2)
            wobble = random.uniform(wobble_min, wobble_max)
            spikes = random.randint(4, 8)
            x, y = spiky_blob(x_center, y_center, radius, wobble, spikes)
            ax.fill(x, y, color=colors[(arm + layer) % len(colors)], alpha=alpha)

    x, y = spiky_blob(center_x, center_y, radius=2.5, wobble=0.1, spikes=7)
    ax.fill(x, y, color=colors[0], alpha=alpha)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    ax.text(-9.5, 9.5, "Week2 • Arts & Advanced Big Data",
            fontsize=14, weight='bold', ha="left", va="top")
    ax.text(-9.5, 8.8, "Generative Poster – Solar Bloom",
            fontsize=11, style='italic', ha="left", va="top")

    return fig


# -------------------------------
# STREAMLIT INTERFACE (INTERACTIVE)
# -------------------------------
st.sidebar.title("🎨 Solar Bloom Controls")

seed = st.sidebar.number_input("Random Seed", value=4701, step=1)
n_arms = st.sidebar.slider("Number of Arms", 4, 20, 12)
n_layers = st.sidebar.slider("Number of Layers", 1, 8, 5)
radius_base = st.sidebar.slider("Base Radius", 1.0, 3.0, 2.0, 0.1)
wobble_min = st.sidebar.slider("Min Wobble", 0.0, 0.2, 0.05, 0.01)
wobble_max = st.sidebar.slider("Max Wobble", 0.1, 0.5, 0.25, 0.01)
alpha = st.sidebar.slider("Transparency (Alpha)", 0.2, 0.8, 0.45, 0.05)

# Generate Poster
st.title("🌸 Generative Poster – Solar Bloom")
st.subheader("Week 2 • Arts & Advanced Big Data")

if st.button("Generate Poster"):
    fig = generate_solar_bloom(seed, n_arms, n_layers, radius_base, wobble_min, wobble_max, alpha)
    st.pyplot(fig)

    # Save PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    st.download_button(
        label="💾 Download Poster (PNG)",
        data=buf.getvalue(),
        file_name="solar_bloom_poster.png",
        mime="image/png"
    )
