import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import math

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title="Generative Poster - Solar Bloom", layout="centered")

# -------------------------------
# 1. DEFINE SPIKY BLOB SHAPE
# -------------------------------
def spiky_blob(x_center, y_center, radius=1.0, wobble=0.15, spikes=5, n_points=300):
    """
    Generate a wobbly circular blob with pointed, spiky edges.
    """
    angles = np.linspace(0, 2 * np.pi, n_points)
    spike_pattern = 1 + 0.3 * np.sin(spikes * angles + random.random() * 2 * np.pi)
    radii = radius * (1 + wobble * np.random.randn(n_points)) * spike_pattern
    x = x_center + radii * np.cos(angles)
    y = y_center + radii * np.sin(angles)
    return x, y

# -------------------------------
# 2. DEFINE COLOR PALETTE (SOFT WARM COLORS)
# -------------------------------
def sunset_palette():
    """
    Softer warm-pastel palette to match the target example image.
    """
    return [
        (0.98, 0.85, 0.75, 0.45),  # light peach
        (0.94, 0.78, 0.85, 0.45),  # soft pink
        (0.90, 0.75, 0.95, 0.45),  # lilac
        (0.95, 0.85, 0.90, 0.45),  # rose
        (0.98, 0.88, 0.65, 0.45),  # cream orange
    ]

# -------------------------------
# 3. MAIN POSTER GENERATOR
# -------------------------------
def generate_solar_bloom(seed=None, n_arms=12, n_layers=5,
                         radius_base=2.0, wobble_min=0.05, wobble_max=0.25):
    """
    Generate a poster with layered, radial, petal-like spiky blobs.
    """
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor("white")  # make background white and clean

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
            ax.fill(x, y, color=colors[(arm + layer) % len(colors)], alpha=0.45)

    # central bloom core
    x, y = spiky_blob(center_x, center_y, radius=2.5, wobble=0.1, spikes=7)
    ax.fill(x, y, color=colors[0], alpha=0.45)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    # title text (top-left)
    ax.text(-9.5, 9.5, "Week2 • Arts & Advanced Big Data",
            fontsize=14, weight='bold', ha="left", va="top")
    ax.text(-9.5, 8.8, "Generative Poster – Solar Bloom",
            fontsize=11, style='italic', ha="left", va="top")

    return fig

# -------------------------------
# 4. STREAMLIT INTERFACE
# -------------------------------
st.title("🌸 Generative Poster – Solar Bloom")
st.subheader("Week 2 • Arts & Advanced Big Data")

# parameters (you can keep these fixed)
seed = 4701     # Fixed seed for the same visual result as your example
arms = 12       # Number of arms / petals
layers = 5      # Number of layers

if st.button("Generate Poster"):
    fig = generate_solar_bloom(seed=seed, n_arms=arms, n_layers=layers)
    st.pyplot(fig)
