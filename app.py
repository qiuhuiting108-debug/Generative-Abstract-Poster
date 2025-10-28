import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import io
import math

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Generative Poster – Streamlit Cloud Edition", layout="wide")

# -------------------------------
# SHAPE FUNCTION
# -------------------------------
def spiky_blob(x_center, y_center, radius=1.0, wobble=0.15, spikes=6, n_points=300):
    """Generate a wobbly circular blob with soft, spiky edges."""
    angles = np.linspace(0, 2 * np.pi, n_points)
    spike_pattern = 1 + 0.25 * np.sin(spikes * angles + random.random() * 2 * np.pi)
    radii = radius * (1 + wobble * np.random.randn(n_points)) * spike_pattern
    x = x_center + radii * np.cos(angles)
    y = y_center + radii * np.sin(angles)
    return x, y

# -------------------------------
# COLOR PALETTE
# -------------------------------
def smooth_palette(n=6):
    """Generate a pastel pink-purple-orange palette."""
    base_colors = [
        (0.95, 0.76, 0.89, 0.5),
        (0.89, 0.72, 0.95, 0.5),
        (0.98, 0.84, 0.70, 0.5),
        (0.92, 0.85, 0.95, 0.5),
        (0.97, 0.88, 0.75, 0.5),
        (0.88, 0.75, 0.92, 0.5),
    ]
    random.shuffle(base_colors)
    return base_colors[:n]

# -------------------------------
# GENERATE POSTER
# -------------------------------
def generate_dense_poster(title, subtitle, n_shapes, palette, max_wobble,
                          alpha_range, size_range, bg_color, seed=None):
    """Dense pastel Solar Bloom style poster."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor(bg_color)

    for _ in range(n_shapes * 5):  # denser than before
        color = random.choice(palette)
        alpha = random.uniform(*alpha_range)
        radius = random.uniform(*size_range)
        wobble = random.uniform(0.0, max_wobble)
        spikes = random.randint(4, 9)

        # tighter central clustering
        x_center = random.gauss(0, 3)
        y_center = random.gauss(0, 3)

        x, y = spiky_blob(x_center, y_center, radius, wobble, spikes)
        ax.fill(x, y, color=color, alpha=alpha, ec="none")

    # Add titles
    ax.text(-9, 9, title, fontsize=28, weight='bold', ha='left', va='top', color='black')
    ax.text(-9, 8, subtitle, fontsize=18, style='italic', ha='left', va='top', color='black')

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    return fig

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
st.sidebar.header("🎨 Generative Poster Settings")

title = st.sidebar.text_input("Title", "Generative Poster")
subtitle = st.sidebar.text_input("Subtitle", "Streamlit Cloud Edition")

n_shapes = st.sidebar.slider("Number of Hearts", 5, 20, 8)
n_colors = st.sidebar.slider("Palette Colors", 3, 10, 6)
max_wobble = st.sidebar.slider("Max Wobble", 0.0, 0.5, 0.25, 0.01)
alpha_min, alpha_max = st.sidebar.slider("Transparency (Alpha)", 0.2, 1.0, (0.25, 0.6))
size_min, size_max = st.sidebar.slider("Heart Size (Radius)", 0.1, 0.8, (0.2, 0.45))
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")

st.sidebar.subheader("Generation")
if "random_seed" not in st.session_state:
    st.session_state.random_seed = 4701

if st.sidebar.button("New Random Layout"):
    st.session_state.random_seed = random.randint(0, 9999)

st.sidebar.write("Current Seed:", st.session_state.random_seed)

# -------------------------------
# MAIN DISPLAY
# -------------------------------
st.title(f"🌸 {title}")
st.subheader(subtitle)

palette = smooth_palette(n_colors)
fig = generate_dense_poster(
    title=title,
    subtitle=subtitle,
    n_shapes=n_shapes,
    palette=palette,
    max_wobble=max_wobble,
    alpha_range=(alpha_min, alpha_max),
    size_range=(size_min, size_max),
    bg_color=bg_color,
    seed=st.session_state.random_seed
)

st.pyplot(fig)

# -------------------------------
# DOWNLOAD BUTTON
# -------------------------------
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
st.sidebar.download_button(
    label="💾 Download Poster (PNG)",
    data=buf.getvalue(),
    file_name="generative_poster_dense.png",
    mime="image/png"
)
