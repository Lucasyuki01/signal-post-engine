# ⚡ Signal Post Engine

An LLM-powered content generation system that produces high-signal LinkedIn posts for B2B SaaS audiences — trained on a manually curated dataset of top-performing content.

🔗 **[Live Demo → signal-post-engine-lyn.streamlit.app](https://signal-post-engine-lyn.streamlit.app/)**

---

## 🎯 The problem

Most AI-generated LinkedIn content fails for the same reasons:

- Generic language with no operational specificity
- Abstract insights that don't reflect real execution
- No grounding in how experienced operators actually write

This tool solves that by combining a manually curated style guide, real-time trend awareness, and strict prompt constraints that actively prevent low-quality patterns.

---

## 🧠 How it works

The system runs a structured 3-stage pipeline before generating a single word:

```
Curated post dataset
       ↓
Style guide extraction  →  "how top performers write"
       ↓
Trend brief             →  "what's relevant right now"
       ↓
Constrained prompt engine
       ↓
Generated posts
```

**Stage 1 — Style learning:** A style guide is extracted from the manually curated dataset of high-performing B2B SaaS posts, capturing sentence structure, hook patterns, and writing rhythm.

**Stage 2 — Trend awareness:** A trend brief is built from recent signals to ensure posts are grounded in current context rather than generic evergreen content.

**Stage 3 — Constrained generation:** The prompt engine applies strict constraints to the OpenAI model — blocking filler language, vague abstractions, and other common AI content failure modes.

---

## ✨ Features

- Click **Generate New Posts** for a fresh batch each run
- Every generation uses a new combination of style + trend signals
- Outputs are grounded in operational specificity, not generic advice
- Streamlit UI for quick iteration and review

---

## 🛠 Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/Lucasyuki01/signal-post-engine.git
cd signal-post-engine
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Add your OpenAI API key:

```bash
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-..."
```

Then run:

```bash
streamlit run app.py
```

---

## 🗂 Project Structure

```
signal-post-engine/
├── app.py                  # Streamlit UI entry point
├── src/
│   └── generate_posts.py   # Generation pipeline
├── prompts/                # Prompt templates and constraints
├── data/
│   └── creators/           # Manually curated post dataset
└── requirements.txt
```

---

## 🔭 Planned improvements

- Post scoring and ranking by predicted engagement
- A/B hook testing across generation runs
- Feedback loop from real engagement data
- Async generation pipeline for higher throughput

---

## 💡 Key insight

The bottleneck in AI content generation is not the model — it's structure, constraints, and grounding in real execution. A GPT-4 with weak prompting produces worse output than a smaller model with well-designed constraints.

---

## 👨‍💻 Author

**Lucas Yuki Nishimoto**
[github.com/Lucasyuki01](https://github.com/Lucasyuki01) · [lucasnishimoto.dev](https://lucasnishimoto.dev)
