import json
import subprocess
import sys
from pathlib import Path

import streamlit as st

def render_post_card(index: int, text: str) -> None:
    st.markdown(
        f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E0DFDC;
            border-radius: 12px;
            padding: 1rem 1rem 1.25rem 1rem;
            margin-top: 0.75rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.06);
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.9rem;
            ">
                <div style="
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    background: #0A66C2;
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 700;
                    font-size: 1rem;
                ">
                    SP
                </div>
                <div>
                    <div style="
                        font-weight: 600;
                        color: #1D2226;
                        font-size: 1rem;
                        line-height: 1.2;
                    ">
                        Signal Post Engine
                    </div>
                    <div style="
                        color: #666666;
                        font-size: 0.85rem;
                        line-height: 1.2;
                    ">
                        Generated LinkedIn Post · Post {index}
                    </div>
                </div>
            </div>
            <div style="
                font-size: 1rem;
                line-height: 1.65;
                color: #1D2226;
                white-space: pre-wrap;
            ">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="Signal Post Engine",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .stButton > button {
        background-color: #0A66C2;
        color: white;
        border: none;
        border-radius: 999px;
        padding: 0.65rem 1.25rem;
        font-weight: 600;
    }

    .stButton > button:hover {
        background-color: #004182;
        color: white;
    }

    div[data-testid="stVerticalBlock"] div:has(> div[data-testid="stMarkdownContainer"]) {
        border-radius: 12px;
    }

    div[data-testid="stExpander"] {
        background: white;
        border-radius: 12px;
        border: 1px solid #E0DFDC;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

OUTPUT_PATH = Path("data/outputs/generated_posts.json")
TREND_BRIEF_PATH = Path("data/trends/trend_brief.md")


def load_trend_brief() -> str:
    if TREND_BRIEF_PATH.exists():
        return TREND_BRIEF_PATH.read_text(encoding="utf-8")
    return """- AI agents are moving from demos to real operating workflows
- Small teams are replacing manual coordination with system-level automation
- Lightweight internal tools are replacing bloated enterprise software
- Reliability and workflow design are becoming bigger differentiators than raw model capability
- Teams using AI for triage, summarization, and drafting are compressing execution cycles
"""


def load_generated_posts() -> list[dict]:
    if not OUTPUT_PATH.exists():
        return []
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def run_generation() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [sys.executable, "src/generate_posts.py"],
            capture_output=True,
            text=True,
            check=True,
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() or e.stdout.strip() or "Unknown error"
        return False, error_message


def next_post(total_posts: int) -> None:
    if total_posts == 0:
        return
    st.session_state.carousel_index = (st.session_state.carousel_index + 1) % total_posts


def prev_post(total_posts: int) -> None:
    if total_posts == 0:
        return
    st.session_state.carousel_index = (st.session_state.carousel_index - 1) % total_posts


if "carousel_index" not in st.session_state:
    st.session_state.carousel_index = 0


st.title("⚡ Signal Post Engine")
st.markdown(
    """
Generate **high-signal LinkedIn posts** for a B2B SaaS audience using:

- a curated style guide extracted from strong posts  
- recent trend inputs  
- a structured generation pipeline focused on specificity, credibility, and operational detail
"""
)

if st.button("Generate New Posts", type="primary", use_container_width=False):
    with st.spinner("Generating a fresh batch..."):
        success, message = run_generation()

    if success:
        st.session_state.carousel_index = 0
        st.success("Fresh posts generated successfully.")
    else:
        st.error(f"Generation failed: {message}")

posts = load_generated_posts()

st.markdown("## Generated Posts")

if posts:
    total_posts = len(posts)
    current_index = min(st.session_state.carousel_index, total_posts - 1)
    current_post = posts[current_index].get("post", "No post content available.")

    nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])

    with nav_col1:
        st.button(
            "← Previous",
            on_click=prev_post,
            args=(total_posts,),
            use_container_width=True,
        )

    with nav_col2:
        selected = st.selectbox(
            "Post",
            options=list(range(total_posts)),
            index=current_index,
            format_func=lambda i: f"Post {i + 1}",
            label_visibility="collapsed",
        )
        st.session_state.carousel_index = selected
        current_index = selected
        current_post = posts[current_index].get("post", "No post content available.")

    with nav_col3:
        st.button(
            "Next →",
            on_click=next_post,
            args=(total_posts,),
            use_container_width=True,
        )

    render_post_card(current_index + 1, current_post)

else:
    st.warning("No posts generated yet. Click “Generate New Posts” to create a batch.")

trend_items = [
    line.strip().lstrip("-").strip()
    for line in load_trend_brief().splitlines()
    if line.strip()
]

trend_html = "".join(
    f"""
    <div style="
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        padding: 0.7rem 0;
        border-top: {'1px solid #E0DFDC' if i > 0 else 'none'};
    ">
        <div style="
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #0A66C2;
            margin-top: 0.45rem;
            flex-shrink: 0;
        "></div>
        <div style="
            color: #1D2226;
            font-size: 1rem;
            line-height: 1.55;
        ">
            {item}
        </div>
    </div>
    """
    for i, item in enumerate(trend_items)
)

st.markdown("## Weekly Signals")
st.markdown(
    f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E0DFDC;
        border-radius: 12px;
        padding: 1.1rem 1.25rem 1rem 1.25rem;
        margin-top: 0.5rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
    ">
        <div style="
            font-weight: 600;
            color: #1D2226;
            font-size: 1rem;
            margin-bottom: 0.2rem;
        ">
            Weekly Signals
        </div>
        <div style="
            color: #666666;
            font-size: 0.9rem;
            margin-bottom: 0.8rem;
        ">
            Recent themes influencing this batch of generated posts
        </div>
        {trend_html}
    </div>
    """,
    unsafe_allow_html=True,
)