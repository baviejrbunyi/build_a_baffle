import os

# Setting up the API Key
os.environ["GROQ_API_KEY"] = "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"

from groq import Groq
import json

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def groq_request(input):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": input
            }],
            response_format={"type": "json_object"},
            model="gemma2-9b-it",
            stream=False,
            temperature=0.5,
        )

        response_content = chat_completion.choices[0].message.content

        # Validate the response
        try:
            response = json.loads(response_content)
            if "title" in response:
                return response
            else:
                print("Error: Missing 'title' in the response")
                return None
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            return None

    except Exception as e:
        print(f"Error in API request: {e}")
        return None

def create_prompt(topic, titles):
    prompt = f"""
    You will be given a narrative.
    Your task is to generate a single problem from that narrative with substance and actual benefit to the world.
    
    You will also be given a list of titles of problems that have already been created. Ensure the new problem's title does not duplicate any title in this list.

    Input: 
    Topic: {topic}
    List of previously generated titles: {titles if titles else "[]"}

    Output must be in this JSON format (only one object):
    {{
        "title": "A unique title",
        "field": ["Field 1", "Field 2", "Field 3"],
        "gaps": ["Gap 1", "Gap 2", "Gap 3"],
        "recommendations": "A short paragraph of 3-5 sentences with recommendations."
    }}

    Do not include any extra text or additional JSON objects.
    """

    return prompt


def summarize_topic(topic):
    # Ensure the topic is safely formatted as a string (if it's a list or object)
    topic_str = str(topic)

    # Create the summary with a properly formatted string
    summary = f"""
    You will be given a list of questions with answers.
    Your task is to create a narrative using those questions and answers.
    In a way, make these things connected with each other.

    Input: {topic_str}

    Output must be in a JSON format:

    {{
        "narrative" : "Your narrative here"
    }}
    """

    return summary
