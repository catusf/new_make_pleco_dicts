import json
from mako.template import Template
import os
import zipfile

# Prepare the directory for the project files
project_dir = "test"
os.makedirs(project_dir, exist_ok=True)

# JSON Data
json_data = [
    {
        "word": "apple",
        "part_of_speech": "noun",
        "meaning": "A fruit that is typically red, green, or yellow.",
        "example": "He ate an apple for breakfast.",
    },
    {
        "word": "run",
        "part_of_speech": "verb",
        "meaning": "To move swiftly on foot.",
        "example": "She runs every morning to stay fit.",
    },
]
json_path = os.path.join(project_dir, "data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)

# Mako Template for Text Output
text_template_content = """
% for entry in data:
${entry['word']}: ${entry['part_of_speech']} / ${entry['meaning']} Example: ${entry['example']}
% endfor
"""
text_template_path = os.path.join(project_dir, "dictionary_template.txt")
with open(text_template_path, "w", encoding="utf-8") as f:
    f.write(text_template_content.strip())

# Generate Text Output using Mako
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

text_template = Template(text_template_content)
text_output = text_template.render(data=data)
text_output_path = os.path.join(project_dir, "dictionary_output.txt")
with open(text_output_path, "w", encoding="utf-8") as f:
    f.write(text_output)
