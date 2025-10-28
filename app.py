import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import math

st.set_page_config(page_title="Generative Poster - Solar Bloom", layout="centered")

def spiky_blob(x_center, y_center, radius=1.0, wobble=0.15, spikes=5, n_points=300):
    angles = np.linspace(0, 2 * np.pi, n_points)
    spike_pattern = 1 + 0.3 * np.sin(spikes * angles + random.random() * 2 * np.pi)
    radii = radius * (1 + wobble * np.random.randn(n_points)) * spike_pattern
    x = x_center + radii * np.cos(angles)
    y = y_center + radii * np.sin(angles)
    return x, y

def sunset_palette():
    return [
        (1.0, 0.85, 0.65, 0.6),
        (1.0, 0.75, 0.70, 0.6),
        (0.95, 0.60, 0.55, 0.6),
        (0.9, 0.75, 1.0, 0.5),
        (1.0, 0.9, 0.9, 0.6)
    ]

def generate_solar_bloom(seed=None, n_arms=8, n_layers=3,
                         radius_base=2.0, wobble_min=0.05, wobble_max=0.2):
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_facecolor("ivory")

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
            ax.fill(x, y, color=colors[(arm + layer) % len(colors)], alpha=0.6)

    x, y = spiky_blob(center_x, center_y, radius=2.5, wobble=0.1, spikes=7)
    ax.fill(x, y, color=colors[0], alpha=0.7)

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    ax.text(-9.5, 9.5, "Week2 • Arts & Advanced Big Data",
            fontsize=14, weight='bold', ha="left", va="top")
    ax.text(-9.5, 8.8, "Generative Poster – Solar Bloom",
            fontsize=11, style='italic', ha="left", va="top")

    return fig

# --- Streamlit UI ---
st.title("🌞 Generative Poster – Solar Bloom")
st.subheader("Week 2 • Arts & Advanced Big Data")

seed = st.number_input("Random Seed", value=77, step=1)
arms = st.slider("Number of Arms", 4, 12, 8)
layers = st.slider("Number of Layers", 1, 6, 3)

if st.button("Generate Poster"):
    fig = generate_solar_bloom(seed=seed, n_arms=arms, n_layers=layers)
    st.pyplot(fig)
