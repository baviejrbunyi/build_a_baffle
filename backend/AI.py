import os

# Setting up the API Key
os.environ["GROQ_API_KEY"] = "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"

from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def groq_request_JSON(input):

    prompt = """

    Remove "*" and "#" symbols from the generated content. Follow the given JSON format
    
    """

    input+=prompt

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input,
            }
        ],
        model="llama3-8b-8192",
    )

    response = chat_completion.choices[0].message.content

    try:
        response_json = json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}\nResponse Content: {response}")


    return response_json


prompt = """

Give me one problem that is about technology.

Output must follow this JSON format. do not add anything on the first part of the output. Just the JSON:

{

    "title": "title of the problem"
    "field": "field of the problem"
    "gaps": "gaps to be solved"
    "recommendations": "recommendations for output"

}

"""

response_json = groq_request_JSON(prompt)
print(response_json)