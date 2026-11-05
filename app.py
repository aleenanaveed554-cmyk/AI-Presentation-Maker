import streamlit as st
import os
import io
import json
import textwrap
from datetime import datetime

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="AI Presentation Studio",
    page_icon="🎞️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at bottom right, #581c87 0%, transparent 35%),
        #050816;
    color: white;
}

[data-testid="stSidebar"] {
    background: #0b1020;
    border-right: 1px solid #26314f;
}

.main-title {
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    margin-top: 15px;

    background: linear-gradient(
        90deg,
        #22d3ee,
        #6366f1,
        #c084fc,
        #f472b6
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #aab4cc;
    font-size: 18px;
    margin-bottom: 35px;
}

.card {
    background: rgba(15, 23, 42, 0.88);
    border: 1px solid #293553;
    border-radius: 22px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    margin-bottom: 15px;
}

.feature {
    background: linear-gradient(
        145deg,
        rgba(30,41,59,0.9),
        rgba(15,23,42,0.9)
    );

    border: 1px solid #293553;
    border-radius: 18px;
    padding: 22px;
    height: 160px;
}

.feature-icon {
    font-size: 35px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
}

.feature-text {
    color: #9ca9c5;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 12px;
    min-height: 45px;
    border: 1px solid #3b4a72;

    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );

    color: white;
    font-weight: 700;
}

div.stButton > button:hover {
    border-color: #22d3ee;
    box-shadow: 0 0 22px rgba(34,211,238,0.3);
}

.status {
    color: #4ade80;
    font-weight: 700;
}

.small {
    color: #8f9bb5;
    font-size: 13px;
}

.slide-preview {
    background: linear-gradient(
        135deg,
        #111827,
        #1e293b
    );

    border: 1px solid #334155;
    border-radius: 18px;
    padding: 25px;
    min-height: 180px;
}

.slide-number {
    color: #60a5fa;
    font-weight: 800;
}

.slide-title {
    font-size: 23px;
    font-weight: 800;
}

.slide-content {
    color: #b6c0d4;
    line-height: 1.7;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# SESSION STATE
# ==============================

if "presentation" not in st.session_state:
    st.session_state.presentation = None

if "generated" not in st.session_state:
    st.session_state.generated = False


# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.markdown("## 🎞️ AI Presentation Studio")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "✨ Create Presentation",
            "📑 My Presentation",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("### 🟢 System Status")

    st.markdown(
        '<p class="status">● System Ready</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="small">AI Presentation Studio v2.0</p>',
        unsafe_allow_html=True
    )


# ==============================
# DASHBOARD
# ==============================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">AI PRESENTATION STUDIO</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Create beautiful presentations with the power of AI'
        '</div>',
        unsafe_allow_html=True
    )

    # Stats

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🎞️ Presentations", "0")

    with c2:
        st.metric("📑 Slides", "0")

    with c3:
        st.metric("🤖 AI Status", "Ready")

    with c4:
        st.metric("⚡ Version", "2.0")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">✨ What You Can Create</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="feature">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI Generated Content</div>
            <div class="feature-text">
                Generate presentation structure and slide content automatically.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Beautiful Themes</div>
            <div class="feature-text">
                Choose modern, professional and creative presentation styles.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature">
            <div class="feature-icon">📥</div>
            <div class="feature-title">Export Ready</div>
            <div class="feature-text">
                Prepare your presentation for PowerPoint export.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Create My Presentation"):

        st.session_state.generated = False

        # Streamlit radio cannot directly change page,
        # so we provide navigation instruction.
        st.info(
            "Sidebar se '✨ Create Presentation' select karein."
        )


# ==============================
# CREATE PRESENTATION
# ==============================

elif page == "✨ Create Presentation":

    st.markdown(
        '<div class="main-title">CREATE PRESENTATION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Turn your idea into a professional presentation'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📝 Presentation Details</div>',
        unsafe_allow_html=True
    )

    topic = st.text_input(
        "Presentation Topic",
        placeholder="Example: Artificial Intelligence"
    )

    description = st.text_area(
        "Describe your presentation",
        placeholder=(
            "Example: Explain Artificial Intelligence, "
            "its applications, advantages and future."
        ),
        height=120
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        slides = st.number_input(
            "Number of Slides",
            min_value=3,
            max_value=30,
            value=8
        )

    with c2:

        language = st.selectbox(
            "Language",
            [
                "English",
                "Urdu",
                "Roman Urdu"
            ]
        )

    with c3:

        difficulty = st.selectbox(
            "Content Level",
            [
                "Beginner",
                "Intermediate",
                "Professional"
            ]
        )

    theme = st.selectbox(
        "🎨 Presentation Theme",
        [
            "Modern Dark",
            "Professional Blue",
            "Creative Gradient",
            "Minimal White",
            "Futuristic AI"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">⚙️ Advanced Options</div>',
        unsafe_allow_html=True
    )

    include_intro = st.checkbox(
        "Include Introduction Slide",
        value=True
    )

    include_conclusion = st.checkbox(
        "Include Conclusion Slide",
        value=True
    )

    include_questions = st.checkbox(
        "Include Q&A Slide",
        value=False
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ==========================
    # GENERATE
    # ==========================

    if st.button("✨ Generate Presentation", type="primary"):

        if not topic.strip():

            st.error("Please enter a presentation topic.")

        else:

            with st.spinner("Creating your presentation..."):

                # --------------------------------
                # DEMO CONTENT GENERATOR
                # --------------------------------

                slides_data = []

                slides_data.append({
                    "title": topic,
                    "content": (
                        f"A professional presentation about {topic}."
                    )
                })

                if include_intro:

                    slides_data.append({
                        "title": "Introduction",
                        "content": (
                            f"Introduction to {topic} and why this topic "
                            f"is important in today's world."
                        )
                    })

                remaining = int(slides) - 2

                if include_conclusion:
                    remaining -= 1

                if include_questions:
                    remaining -= 1

                if remaining < 1:
                    remaining = 1

                topics = [
                    "Overview",
                    "Key Concepts",
                    "How It Works",
                    "Main Features",
                    "Applications",
                    "Advantages",
                    "Challenges",
                    "Future",
                    "Important Examples",
                    "Impact"
                ]

                for i in range(remaining):

                    title = topics[i % len(topics)]

                    slides_data.append({
                        "title": title,
                        "content": (
                            f"Important information about {title} "
                            f"in the context of {topic}. "
                            f"This section explains the main ideas, "
                            f"examples and practical importance."
                        )
                    })

                if include_conclusion:

                    slides_data.append({
                        "title": "Conclusion",
                        "content": (
                            f"Key takeaways from the presentation about "
                            f"{topic}."
                        )
                    })

                if include_questions:

                    slides_data.append({
                        "title": "Questions & Answers",
                        "content": (
                            "Thank you for listening. "
                            "Questions and discussion."
                        )
                    })

                # Limit slides
                slides_data = slides_data[:int(slides)]

                st.session_state.presentation = {
                    "topic": topic,
                    "description": description,
                    "language": language,
                    "level": difficulty,
                    "theme": theme,
                    "slides": slides_data,
                    "created": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }

                st.session_state.generated = True

            st.success("🎉 Presentation created successfully!")

    # ==========================
    # PREVIEW
    # ==========================

    if st.session_state.generated:

        presentation = st.session_state.presentation

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div class="section-title">👀 Presentation Preview</div>',
            unsafe_allow_html=True
        )

        for i, slide in enumerate(
            presentation["slides"]
        ):

            st.markdown(
                f"""
                <div class="slide-preview">

                    <div class="slide-number">
                        SLIDE {i + 1}
                    </div>

                    <div class="slide-title">
                        {slide["title"]}
                    </div>

                    <br>

                    <div class="slide-content">
                        {slide["content"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

        # ======================
        # DOWNLOAD JSON
        # ======================

        json_data = json.dumps(
            presentation,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            "📥 Download Presentation Data",
            data=json_data,
            file_name="presentation.json",
            mime="application/json"
        )


# ==============================
# MY PRESENTATION
# ==============================

elif page == "📑 My Presentation":

    st.markdown(
        '<div class="main-title">MY PRESENTATION</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View and manage your generated presentation'
        '</div>',
        unsafe_allow_html=True
    )

    if not st.session_state.presentation:

        st.info(
            "No presentation created yet."
        )

    else:

        presentation = st.session_state.presentation

        st.markdown(
            f"""
            <div class="card">

                <h2>
                    🎞️ {presentation["topic"]}
                </h2>

                <p class="small">
                    Created: {presentation["created"]}
                </p>

                <p>
                    <b>Language:</b> {presentation["language"]}
                </p>

                <p>
                    <b>Level:</b> {presentation["level"]}
                </p>

                <p>
                    <b>Theme:</b> {presentation["theme"]}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📑 Slides")

        for i, slide in enumerate(
            presentation["slides"]
        ):

            with st.expander(
                f"Slide {i + 1}: {slide['title']}"
            ):

                st.write(
                    slide["content"]
                )

        json_data = json.dumps(
            presentation,
            indent=4,
            ensure_ascii=False
        )

        st.download_button(
            "📥 Download Presentation",
            data=json_data,
            file_name="AI_Presentation.json",
            mime="application/json"
        )


# ==============================
# SETTINGS
# ==============================

elif page == "⚙️ Settings":

    st.markdown(
        '<div class="main-title">SETTINGS</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Customize your AI Presentation Studio'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown("### 🎨 Interface")

    dark_mode = st.toggle(
        "Dark interface",
        value=True
    )

    animations = st.toggle(
        "Enable animations",
        value=True
    )

    st.markdown("### 🤖 AI Settings")

    creativity = st.slider(
        "AI Creativity",
        0.0,
        1.0,
        0.7
    )

    st.markdown("### 📑 Presentation Defaults")

    default_language = st.selectbox(
        "Default Language",
        [
            "English",
            "Urdu",
            "Roman Urdu"
        ]
    )

    default_theme = st.selectbox(
        "Default Theme",
        [
            "Modern Dark",
            "Professional Blue",
            "Creative Gradient",
            "Minimal White",
            "Futuristic AI"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("💾 Save Settings"):

        st.success(
            "Settings saved successfully!"
        )


# ==============================
# FOOTER
# ==============================

st.markdown("""
<br><br>

<div style="
text-align:center;
color:#68738e;
padding:20px;
">

🎞️ AI Presentation Studio  
<br>
Create • Design • Present

</div>
""", unsafe_allow_html=True)
