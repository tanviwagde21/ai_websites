import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from schema import WebsiteBlueprint

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use available model
model = genai.GenerativeModel("models/gemini-2.5-flash")

TEMPLATE = """
You are an assistant that outputs ONLY valid JSON.
Keys required:
- project_name (string)
- pages (list of strings)
- components (object: page -> list of components)
- style (string)

Do NOT include any explanation, only JSON.
User request:
\"\"\"{user_prompt}\"\"\"
"""

def parse_prompt(user_prompt: str):
    prompt = TEMPLATE.format(user_prompt=user_prompt)
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Clean markdown fences
    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1])

    try:
        data = json.loads(text)
        blueprint = WebsiteBlueprint(**data)  # ✅ validate structure
        return blueprint
    except Exception as e:
        print("⚠️ Could not parse valid JSON:", e)
        print("Raw output:\n", text)
        return None
if __name__ == "__main__":
    bp = parse_prompt("Make a bakery website with menu, gallery, and contact page")
    if bp:
        json_data = bp.model_dump_json(indent=2)
        print("\nValidated JSON:\n", json_data)

        # ✅ Save to file
        output_path = "output/blueprint.json"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_data)
        print(f"\n✅ Saved blueprint to {output_path}")
