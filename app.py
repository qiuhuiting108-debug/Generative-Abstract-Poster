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
# GENERATE SHAPE
# -------------------------------
def spiky_blob(x_center, y_center, radius=1.0, wobble=0.15, spikes=5, n_points=300):
    """Generate a wobbly circular blob with pointed edges."""
    angles = np.linspace(0, 2 * np.pi, n_points)
    spike_pattern = 1 + 0.3 * np.sin(spikes * angles + random.random() * 2 * np.pi)
    radii = radius * (1 + wobble * np.random.randn(n_points)) * spike_pattern
    x = x_center + radii * np.cos(angles)
    y = y_center + radii * np.sin(angles)
    return x, y

# -------------------------------
# GENERATE COLOR PALETTE
# -------------------------------
def random_palette(n=6):
    """Generate a smooth color palette."""
    base_colors = [
        (0.94, 0.78, 0.85, 1.0),  # pink
        (0.90, 0.75, 0.95, 1.0),  # lilac
        (0.95, 0.85, 0.90, 1.0),  # rose
        (0.98, 0.88, 0.65, 1.0),  # light orange
        (0.80, 0.75, 0.95, 1.0),  # lavender
        (0.98, 0.85, 0.75, 1.0),  # peach
        (0.85, 0.78, 0.92, 1.0),  # pastel violet
    ]
    random.shuffle(base_colors)
    return base_colors[:n]

# -------------------------------
# GENERATE POSTER
# -------------------------------
def generate_poster(title, subtitle, n_hearts, palette, max_wobble, alpha_range,
                    size_range, bg_color, seed=None):
    """Draw a Solar Bloom style poster with soft petals."""
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.axis("off")
    ax.set_facecolor(bg_color)

    for _ in range(n_hearts):
        color = random.choice(palette)
        alpha = random.uniform(*alpha_range)
        radius = random.uniform(*size_range)
        spikes = random.randint(4, 8)
        x_center = random.uniform(-6, 6)
        y_center = random.uniform(-6, 6)
        x, y = spiky_blob(x_center, y_center, radius=radius, wobble=max_wobble, spikes=spikes)
        ax.fill(x, y, color=color, alpha=alpha, ec="none")

    # text
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

n_hearts = st.sidebar.slider("Number of Hearts", 3, 20, 8)
n_colors = st.sidebar.slider("Palette Colors", 3, 10, 6)
max_wobble = st.sidebar.slider("Max Wobble", 0.0, 0.5, 0.25, 0.01)
alpha_min, alpha_max = st.sidebar.slider("Transparency (Alpha)", 0.0, 1.0, (0.25, 0.6))
size_min, size_max = st.sidebar.slider("Heart Size (Radius)", 0.1, 0.6, (0.15, 0.45))
bg_color = st.sidebar.color_picker("Background Color", "#ffffff")

# -------------------------------
# GENERATION SETTINGS
# -------------------------------
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

palette = random_palette(n_colors)
fig = generate_poster(
    title=title,
    subtitle=subtitle,
    n_hearts=n_hearts,
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
    file_name="generative_poster_final.png",
    mime="image/png"
)
