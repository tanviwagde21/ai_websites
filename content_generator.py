# content_generator.py

import os, json
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Load .env
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Paths
blueprint_path = Path("output/blueprint.json")
content_path = Path("output/content.json")

# Read the blueprint.json
with open(blueprint_path, "r") as f:
    blueprint = json.load(f)

print("Loaded blueprint for project:", blueprint["project_name"])

# Function to generate text for a component
def gen_text_for_component(component, context=""):
    prompt = f"""
    Generate content for a website component: {component}.
    Context: {context}.
    Return JSON with suitable fields (like title, subtitle, description, labels).
    Only return JSON, no explanations.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")  # fast & cheap model
    response = model.generate_content(prompt)

    text = response.text.strip()
    if text.startswith("```"):
        text = "\n".join(text.splitlines()[1:-1])  # clean markdown fences
    return json.loads(text)

# Loop over all pages and components
content = {}
for page, comps in blueprint["components"].items():
    content[page] = {}
    for comp in comps:
        try:
            print(f"🔹 Generating content for {page} -> {comp}")
            comp_text = gen_text_for_component(comp, blueprint["style"])
            content[page][comp] = comp_text
        except Exception as e:
            print("❌ Error generating for", comp, ":", e)
            content[page][comp] = {"error": str(e)}

# Save the generated content
with open(content_path, "w") as f:
    json.dump(content, f, indent=2)

print("✅ Saved generated content to", content_path)
