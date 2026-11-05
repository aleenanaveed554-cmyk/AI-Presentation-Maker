import streamlit as st
from presentation_generator import generate_presentation
from ppt_builder import create_pptx

st.set_page_config(
    page_title="AI Presentation Maker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(91, 33, 182, 0.28), transparent 35%),
        radial-gradient(circle at bottom right, rgba(37, 99, 235, 0.22), transparent 35%),
        #070b1a;
    color: white;
}

.block-container {
    max-width: 1200px;
    padding-top: 3rem;
}

/* Hero */
.hero {
    text-align: center;
    padding: 55px 20px 35px 20px;
}

.badge {
    display: inline-block;
    padding: 9px 18px;
    border-radius: 30px;
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.35);
    color: #c7d2fe;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 58px;
    line-height: 1.1;
    font-weight: 800;
    margin: 0;
    background: linear-gradient(
        90deg,
        #ffffff,
        #c4b5fd,
        #93c5fd
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    max-width: 700px;
    margin: 20px auto;
    color: #aab3cf;
    font-size: 18px;
    line-height: 1.7;
}

/* Cards */
.card {
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 25px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.card h3 {
    color: #f8fafc;
    margin-bottom: 10px;
}

.small {
    color: #94a3b8;
    font-size: 14px;
}

/* Slide preview */
.slide-card {
    background: linear-gradient(135deg, #111827, #172554);
    border: 1px solid rgba(129, 140, 248, 0.25);
    border-radius: 20px;
    padding: 30px;
    min-height: 230px;
    margin-bottom: 18px;
}

.slide-number {
    color: #a5b4fc;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.slide-title {
    font-size: 28px;
    font-weight: 800;
    color: white;
    margin: 10px 0 18px;
}

.slide-content {
    color: #cbd5e1;
    line-height: 1.8;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    border: 1px solid rgba(129, 140, 248, 0.3);
}

div[data-testid="stDownloadButton"] button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    min-height: 52px;
    font-weight: 800;
}

/* Inputs */
div[data-baseweb="input"],
div[data-baseweb="select"] {
    border-radius: 12px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# Hero section
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="badge">✨ AI-POWERED PRESENTATION CREATOR</div>

    <h1>AI Presentation Maker</h1>

    <p>
        Transform any topic into a professional, well-structured
        PowerPoint presentation in seconds using artificial intelligence.
    </p>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# Main settings
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### 🎯 Create Your Presentation")
st.markdown(
    '<p class="small">Enter your topic and customize your presentation.</p>',
    unsafe_allow_html=True
)

topic = st.text_input(
    "Presentation Topic",
    placeholder="e.g. Artificial Intelligence in Education"
)

col1, col2, col3 = st.columns(3)

with col1:
    slide_count = st.slider(
        "Number of Slides",
        min_value=3,
        max_value=15,
        value=7
    )

with col2:
    theme = st.selectbox(
        "Design Theme",
        [
            "Modern Dark",
            "Professional Blue",
            "Purple Gradient",
            "Minimal White",
            "Academic",
            "Technology"
        ]
    )

with col3:
    language = st.selectbox(
        "Language",
        [
            "English",
            "Urdu",
            "Roman Urdu"
        ]
    )

st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# Generate button
# -----------------------------
if st.button("🚀 Create Presentation", use_container_width=True):

    if not topic.strip():
        st.warning("Please enter a presentation topic.")
        st.stop()

    with st.spinner("🤖 AI is creating your presentation..."):

        try:
            slides = generate_presentation(
                topic=topic,
                slide_count=slide_count,
                theme=theme,
                language=language
            )

            st.session_state["slides"] = slides
            st.session_state["topic"] = topic
            st.session_state["theme"] = theme

        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()


# -----------------------------
# Preview
# -----------------------------
if "slides" in st.session_state:

    slides = st.session_state["slides"]

    st.markdown("""
    <div class="card">
        <h3>📑 Presentation Preview</h3>
        <p class="small">
            Review the AI-generated slides before downloading.
        </p>
    </div>
    """, unsafe_allow_html=True)

    for index, slide in enumerate(slides):

        title = slide.get("title", "Untitled Slide")
        points = slide.get("points", [])

        points_html = ""

        for point in points:
            points_html += f"<li>{point}</li>"

        st.markdown(
            f"""
            <div class="slide-card">
                <div class="slide-number">
                    Slide {index + 1}
                </div>

                <div class="slide-title">
                    {title}
                </div>

                <div class="slide-content">
                    <ul>
                        {points_html}
                    </ul>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------
    # Generate PPTX
    # -------------------------
    try:

        ppt_file = create_pptx(
            slides=slides,
            topic=st.session_state["topic"],
            theme=st.session_state["theme"]
        )

        st.markdown("### 📥 Download")

        st.download_button(
            label="⬇️ Download PowerPoint Presentation",
            data=ppt_file,
            file_name="AI_Presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Could not create PowerPoint file: {e}")


# -----------------------------
# Footer
# -----------------------------
st.markdown("""
<div style="
text-align:center;
margin-top:60px;
padding:25px;
color:#64748b;
font-size:13px;
">
AI Presentation Maker • Built with Python + Streamlit + AI
</div>
""", unsafe_allow_html=True)
