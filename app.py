import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Generative Poster - Streamlit Cloud Edition", layout="wide")

# -------------------------------
# FUNCTION: HEART SHAPE
# -------------------------------
def heart_shape(x_center, y_center, size=1.0, wobble=0.2, n_points=300):
    """Generate a heart-like shape with random edge wobble."""
    t = np.linspace(0, 2 * np.pi, n_points)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    x, y = x / 17.0, y / 17.0  # normalize
    x = x_center + size * (x + wobble * np.random.randn(n_points))
    y = y_center + size * (y + wobble * np.random.randn(n_points))
    return x, y

# -------------------------------
# FUNCTION: RANDOM COLOR PALETTE
# -------------------------------
def random_palette(n=5):
    """Generate a random RGB color palette."""
    palette = []
    for _ in range(n):
        palette.append((random.random(), random.random(), random.random()))
    return palette

# -------------------------------
# FUNCTION: GENERATE POSTER
# -------------------------------
def generate_poster(title, subtitle, n_hearts, palette, max_wobble,
                    alpha_range, size_range, bg_color, seed=None):
    """Draws a generative poster with heart-shaped blobs."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor(bg_color)

    for _ in range(n_hearts):
        color = random.choice(palette)
        alpha = random.uniform(*alpha_range)
        size = random.uniform(*size_range)
        wobble = random.uniform(0.0, max_wobble)
        x, y = heart_shape(random.uniform(-1, 1) * 8,
                           random.uniform(-1, 1) * 8,
                           size=size, wobble=wobble)
        ax.fill(x, y, color=color, alpha=alpha, ec="none")

    # text labels
    ax.text(-9, 9, title, fontsize=28, weight='bold', ha='left', va='top', color='black')
    ax.text(-9, 8, subtitle, fontsize=18, style='italic', ha='left', va='top', color='black')

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    return fig

# -------------------------------
# SIDEBAR CONTROLS
# -------------------------------
st.sidebar.header("🎨 Generative Poster Settings")

# text inputs
title = st.sidebar.text_input("Title", "Generative Poster")
subtitle = st.sidebar.text_input("Subtitle", "Streamlit Cloud Edition")

# sliders
n_hearts = st.sidebar.slider("Number of Hearts", 3, 20, 8)
n_colors = st.sidebar.slider("Palette Colors", 3, 10, 6)
max_wobble = st.sidebar.slider("Max Wobble", 0.0, 0.5, 0.25, 0.01)
alpha_min, alpha_max = st.sidebar.slider("Transparency (Alpha)", 0.0, 1.0, (0.25, 0.6))
size_min, size_max = st.sidebar.slider("Heart Size (Radius)", 0.1, 0.6, (0.15, 0.45))
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")

# generation buttons
st.sidebar.subheader("Generation")
if "random_seed" not in st.session_state:
    st.session_state.random_seed = random.randint(0, 9999)

if st.sidebar.button("New Random Layout"):
    st.session_state.random_seed = random.randint(0, 9999)

st.sidebar.write("Current Seed:", st.session_state.random_seed)

# -------------------------------
# MAIN DISPLAY
# -------------------------------
st.title(f"🌞 {title}")
st.subheader(subtitle)

fig = generate_poster(
    title=title,
    subtitle=subtitle,
    n_hearts=n_hearts,
    palette=random_palette(n_colors),
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
    file_name="generative_poster_streamlit.png",
    mime="image/png"
)
