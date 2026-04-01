import json
import os
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_posts():
    with open("data/creators/creator_posts.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_prompt():
    with open("prompts/style_guide_prompt.md", "r", encoding="utf-8") as f:
        return f.read()

def build_input(posts):
    texts = [p["post_text"] for p in posts]
    return "\n\n---\n\n".join(texts)

def generate_style_guide():
    posts = load_posts()
    prompt = load_prompt()
    content = build_input(posts)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    )

    style_guide = response.choices[0].message.content

    Path("data/creators").mkdir(parents=True, exist_ok=True)

    with open("data/creators/style_guide.md", "w", encoding="utf-8") as f:
        f.write(style_guide)

    print("Style guide generated!")

if __name__ == "__main__":
    generate_style_guide()