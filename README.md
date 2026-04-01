# ⚡ Signal Post Engine

Generate high-signal LinkedIn posts for a B2B SaaS audience using structured LLM workflows.

---

## Overview

This project builds an end-to-end system that generates LinkedIn posts designed to compete with top-performing content.

Instead of producing generic AI content, the system focuses on:

- operational specificity
- real-world workflows
- credible insights
- structured writing patterns

The goal is to simulate how experienced operators write, not how generic AI outputs content.

---

## Demo

Click **Generate New Posts** to create a fresh batch of posts.

Each generation run produces new outputs based on:

- a learned style guide from high-performing posts
- a trend brief built from recent signals
- strict prompt constraints to avoid low-quality patterns

---

## Core Idea

Most AI-generated content fails because it is:

- generic  
- overly abstract  
- not grounded in execution  

This system solves that by combining:

1. Style Learning  
2. Trend Awareness  
3. Constrained Generation  

---

## Architecture

Data Collection → Style Guide Extraction → Trend Brief → Prompt Engine → Post Generation → UI

---

## Components

- Dataset (data/creators/)
- Style Guide (style_guide.md)
- Trend Brief (data/trends/)
- Prompt Engine (prompts/)
- Generation Script (src/generate_posts.py)
- UI (app.py)

---

## How to Run

1. Clone the repository  
2. Create a virtual environment  
3. Install dependencies  
4. Add your API key  
5. Run Streamlit app  

---

## Reflection & Scaling

Future improvements:

- Post scoring and ranking  
- A/B hook testing  
- Feedback loop from engagement  
- Async generation pipeline  

---

## Key Insight

The bottleneck in AI content is not generation.

It is structure, constraints, and grounding in real execution.
