import re
import  backend.AI as AI
import json

class Baffle:
    def __init__(self, title, field, gaps, recommendations):
        self.title = title
        self.field = field
        self.gaps = gaps
        self.recommendations = recommendations

    def __repr__(self):
        return f"Baffle(title={self.title}, field={self.field}, gaps={self.gaps}, recommendations={self.recommendations})"
    
    @classmethod
    def from_json(cls, json_data):
        """
        Populates a Baffle object from a JSON-formatted string or dictionary.
        """
        if isinstance(json_data, str):
            json_data = json.loads(json_data)  # Parse string into dictionary
        return cls(
            title=json_data.get("title", ""),
            field=json_data.get("field", []),
            gaps=json_data.get("gaps", []),
            recommendations=json_data.get("recommendations", "")
        )


def create_baffles(topic, loop):
    baffles = []
    titles = []
    loop = int(loop)

    for i in range(loop):
        prompt_input = AI.create_prompt(AI.summarize_topic(topic), titles)
        baffle_data = AI.groq_request(prompt_input)

        if baffle_data:
            try:
                baffle = Baffle.from_json(baffle_data)
                if baffle and baffle.title and baffle.title not in titles:
                    titles.append(baffle.title)
                    baffles.append(baffle)
            except Exception as e:
                print(f"Error creating baffle from data: {e}")

        print(f"Titles so far: {titles}")

    return baffles

def create_baffle_with_field(field):
    """
    Generate a single Baffle instance that matches the given field.
    """
    titles = []  # Track titles to avoid duplicates

    # Generate a baffle using the field as part of the topic
    prompt_input = AI.create_prompt(field, titles)
    baffle_data = AI.groq_request(prompt_input)

    if baffle_data:
        try:
            baffle = Baffle.from_json(baffle_data)
            if baffle and baffle.title and baffle.title not in titles:
                titles.append(baffle.title)
                return baffle
        except Exception as e:
            print(f"Error creating baffle from data: {e}")

    # Return None if no valid baffle was created
    return None