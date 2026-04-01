import json
import subprocess
import sys
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Signal Post Engine",
    page_icon="⚡",
    layout="wide",
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

    with st.container(border=True):
        st.markdown(f"### Post {current_index + 1}")
        st.markdown(current_post)

else:
    st.warning("No posts generated yet. Click “Generate New Posts” to create a batch.")

st.markdown("## Trend Brief")
st.markdown(load_trend_brief()) 