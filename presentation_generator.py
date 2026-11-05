import json
import os
from groq import Groq


def generate_presentation(
    topic,
    slide_count,
    theme,
    language
):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is not configured."
        )

    client = Groq(api_key=api_key)

    prompt = f"""
You are a professional university presentation designer.

Create a PowerPoint presentation about:

TOPIC:
{topic}

NUMBER OF SLIDES:
{slide_count}

DESIGN THEME:
{theme}

LANGUAGE:
{language}

Requirements:

1. Create exactly {slide_count} slides.
2. Give every slide a clear professional title.
3. Give every slide 3 to 5 important bullet points.
4. Content should be educational and accurate.
5. Avoid unnecessary repetition.
6. Use concise presentation-friendly language.
7. Start with an introduction.
8. Include important concepts, examples or applications.
9. End with a conclusion.
10. Do not include speaker notes.
11. Do not use markdown.
12. Return ONLY valid JSON.

Use exactly this structure:

{{
    "slides": [
        {{
            "title": "Slide title",
            "points": [
                "Point 1",
                "Point 2",
                "Point 3",
                "Point 4"
            ]
        }}
    ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You create professional educational presentations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=5000
    )

    result = response.choices[0].message.content.strip()

    # Remove accidental markdown fences
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    data = json.loads(result)

    slides = data.get("slides", [])

    if not slides:
        raise ValueError("AI returned no slides.")

    return slides
