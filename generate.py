
import os
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_KEY = os.environ["GEMINI_API_KEY"]

URL = url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

prompt = """
You are the head writer of ASTRA HAWK ANIME STUDIO.

Create one original 90-120 second anime episode in English.

MAIN CHARACTER:
- Name: Astra Hawk
- Female, 18 years old
- Blonde, medium-length hair
- Falcon tattoo on her left arm
- Consistent anime character design

REQUIREMENTS:
1. Create 12-15 connected scenes.
2. Each scene should last approximately 8 seconds.
3. Include detailed visual descriptions.
4. Include camera movements and character actions.
5. Include English dialogue and narration.
6. Make the story exciting and original.
7. Give the episode a meaningful conclusion.
8. Do not write "To be continued".

Return ONLY valid JSON in this format:
{
  "title": "Episode title",
  "description": "YouTube description",
  "scenes": [
    {
      "scene": 1,
      "duration": 8,
      "visual": "Visual description",
      "camera": "Camera direction",
      "dialogue": "English dialogue",
      "video_prompt": "Detailed anime video prompt"
    }
  ]
}
"""

payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }],
    "generationConfig": {
        "temperature": 0.8,
        "responseMimeType": "application/json"
    }
}

request = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    },
    method="POST"
)

with urllib.request.urlopen(request, timeout=120) as response:
    result = json.loads(response.read().decode("utf-8"))

text = result["candidates"][0]["content"]["parts"][0]["text"]
story = json.loads(text)

Path("output").mkdir(exist_ok=True)

date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

with open(f"output/episode-{date}.json", "w",
          encoding="utf-8") as file:
    json.dump(story, file, indent=2, ensure_ascii=False)

print("ASTRA HAWK EPISODE CREATED!")
print("Title:", story["title"])
print("Scenes:", len(story["scenes"]))
