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
    loop = int(loop)

    for i in range(loop):
        baffle = Baffle.from_json(AI.groq_request(AI.create_prompt(topic)))
        baffles.append(baffle)
        

    return baffles

