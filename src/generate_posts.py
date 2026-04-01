import os
import json
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def load_style_guide():
    with open("data/creators/style_guide.md", "r", encoding="utf-8") as f:
        return f.read()


def load_trend_brief():
    trend_path = Path("data/trends/trend_brief.md")
    if trend_path.exists():
        return trend_path.read_text(encoding="utf-8")
    return "No trend data available."


def load_prompt():
    with open("prompts/generate_posts_prompt.md", "r", encoding="utf-8") as f:
        return f.read()


def generate_posts():
    style_guide = load_style_guide()
    trends = load_trend_brief()
    prompt = load_prompt()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": f"STYLE GUIDE:\n{style_guide}\n\nTREND BRIEF:\n{trends}",
            },
        ],
        temperature=0.55,
    )

    content = response.choices[0].message.content
    posts = json.loads(content)

    output_dir = Path("data/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / "generated_posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print("Posts generated successfully.")


if __name__ == "__main__":
    generate_posts()