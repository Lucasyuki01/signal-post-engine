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


def render_post_card(index: int, text: str) -> None:
    with st.container(border=True):
        st.markdown(f"### Post {index}")
        st.markdown(text)


st.title("⚡ Signal Post Engine")
st.markdown(
    """
Generate **high-signal LinkedIn posts** for a B2B SaaS audience using:

- a curated style guide extracted from strong posts
- recent trend inputs
- a structured generation pipeline focused on specificity, credibility, and operational detail
"""
)

with st.sidebar:
    st.header("Configuration")
    st.markdown("**Industry**")
    st.info("Tech")

    st.markdown("**Topic Focus**")
    st.info("How small teams use AI to compete with larger companies")

    st.markdown("**Pipeline**")
    st.write("1. Trend brief")
    st.write("2. Style guide")
    st.write("3. Post generation")

hero_left, hero_right = st.columns([2, 1])

with hero_left:
    st.subheader("What this demo does")
    st.write(
        "This workflow generates fresh LinkedIn posts designed to feel practical, operator-led, "
        "and grounded in real execution rather than generic AI content."
    )

with hero_right:
    if st.button("Generate New Posts", type="primary", use_container_width=True):
        with st.spinner("Generating a fresh batch..."):
            success, message = run_generation()

        if success:
            st.success("Fresh posts generated successfully.")
        else:
            st.error(f"Generation failed: {message}")

st.divider()

with st.expander("Trend Brief", expanded=True):
    st.markdown(load_trend_brief())

posts = load_generated_posts()

st.subheader("Generated Posts")

if posts:
    for index, post in enumerate(posts, start=1):
        render_post_card(index, post.get("post", "No post content available."))
else:
    st.warning("No posts generated yet. Click “Generate New Posts” to create a batch.")