import os

# Setting up the API Key
os.environ["GROQ_API_KEY"] = "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"

from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def groq_request(input):

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input
            }
        ],
        response_format= {"type": "json_object"},
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    return json.loads(chat_completion.choices[0].message.content)


def create_prompt(topic):
    prompt = f"""
    Give me one problem that is about {topic}.

    Output must follow this format:
    title: title of the problem.
    field: field of the problem (if multiple fields, max of 3. list down in a bulleted format using "-")
    gaps: gaps to be solved
    recommendations: recommendations for output (3-5 sentences)

    Ensure that the problems are unique from eqch other. No duplicate titles or idea

    Output must be in this JSON format:

    {{
        "title": "",
        "field": [""],
        "gaps": [""],
        "recommendations": ""
    }}
    """

    return prompt



